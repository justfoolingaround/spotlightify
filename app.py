import asyncio
import pathlib
import sys
import time
from threading import Thread

import aiohttp
import orjson
import requests
import spotivents
from pynput.mouse import Button, Controller
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QApplication, QMenu, QSystemTrayIcon
from rich.console import Console
from rich.traceback import install
from spotipy import Spotify

from caching import CacheManager, ImageQueue, SongQueue
from definitions import ASSETS_DIR
from settings import default_themes
from settings.preferences import Preferences
from shortcuts import listener
from ui import SpotlightUI

install()


class SpotiventfulSpotfy(Spotify):
    def __init__(self, cookie, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.cookie = cookie
        self.loop = asyncio.new_event_loop()

        self.loop.create_task(self.start_spotivents())
        self.spotivents_thread = Thread(target=self.loop.run_forever, daemon=True)

    async def start_spotivents(self):

        self.session = aiohttp.ClientSession()
        self.auth = spotivents.SpotifyAuthenticator(self.session, self.cookie)
        self.client = spotivents.SpotifyClient(self.session, self.auth)
        self.controller = spotivents.SpotifyAPIControllerClient(self.session, self.auth)

        await self.client.run(is_blocking=False)

        while self.client.cluster is None:
            await asyncio.sleep(1.0)

        if self.client.cluster.active_device_id is None:
            for device_id, device in self.client.cluster.devices.items():
                if device.can_play:
                    return await self.controller.transfer_across_device(device_id)

    def run_coroutine_threadsafe(self, coroutine):
        future = asyncio.run_coroutine_threadsafe(coroutine, self.loop)
        return future.result()


class App:
    def __init__(self, session_path: pathlib.Path = None):

        self.console = Console()
        self.session_file = session_path or pathlib.Path("session.json")
        self.token_data = {}
        self.http_session = requests.Session()

        self.http_session.headers["User-Agent"] = "Lightify/1.0.0"

        self.app = QApplication([])
        self.app.setQuitOnLastWindowClosed(False)

        self.theme = default_themes["dark"]

        self.tray = None
        self.tray_menu = None
        self.action_open = None
        self.action_exit = None

        self.preferences = Preferences()

        self.spotlight = None
        self.spotify = None

        self.listener_thread = Thread(
            target=listener, daemon=True, args=(self.show_spotlight,)
        )
        self.song_queue = None
        self.image_queue = None
        self.cache_manager = None

    @property
    def session(self):
        if self.session_file.exists():
            return orjson.loads(self.session_file.read_bytes())

        return {}

    @session.setter
    def session(self, value):
        self.session_file.write_bytes(orjson.dumps(value))

    @property
    def access_token_data(self):

        if not self.token_data:
            cookie = self.session.get("cookie")

            if cookie is None:
                raise RuntimeError("Unable to fetch user cookie.")

            response = self.http_session.get(
                "https://open.spotify.com/get_access_token",
                cookies={"sp_dc": cookie},
                params={
                    "reason": "transport",
                    "productType": "web_player",
                },
            )
            response.raise_for_status()

            self.token_data = response.json()

        if self.token_data.get("accessTokenExpirationTimestampMs", 0) < (
            time.time() * 1000
        ):
            self.token_data.clear()
        else:
            return self.token_data

        return self.access_token_data

    def run(self):

        cookie = self.session.get("cookie")

        if cookie is None:
            cookie = self.console.input("Spotify web player cookie [sp_dc]: ")

        self.session = {"cookie": cookie}

        try:
            token = self.access_token_data["accessToken"]
        except Exception as _:
            self.console.print(
                f"Suffered an unexpected error server side while using the cookie, please ensure it is valid. {_!r}"
            )
            self.session = {}
            return self.run()

        self.ui_invoke()

    def ui_invoke(self):
        """
        Runs authorisation process
        and invokes the UI.
        """

        self.spotify = SpotiventfulSpotfy(
            self.session.get("cookie"), auth=self.access_token_data["accessToken"]
        )
        self.spotify.spotivents_thread.start()

        self.init_tray()

        self.song_queue = SongQueue()
        self.image_queue = ImageQueue()
        self.cache_manager = CacheManager(
            self.spotify, self.song_queue, self.image_queue
        )
        self.cache_manager.start()

        self.spotlight = SpotlightUI(self.spotify, self.song_queue)
        self.show_spotlight()
        self.listener_thread.start()

        self.console.print("All systems ready, listening for shortcuts!")

        while 1:
            self.app.exec_()

    def init_tray(self):
        self.tray_menu = QMenu()

        self.action_open = QAction("Open")
        self.action_open.triggered.connect(self.show_spotlight)
        self.tray_menu.addAction(self.action_open)

        self.action_exit = QAction("Exit")
        self.action_exit.triggered.connect(App.exit)
        self.tray_menu.addAction(self.action_exit)

        self.tray = QSystemTrayIcon()

        icon_path = pathlib.Path(ASSETS_DIR) / "img" / "logo_small.png"
        self.tray.setIcon(QIcon(icon_path.as_posix()))
        self.tray.setVisible(True)
        self.tray.setToolTip("Spotlightify")
        self.tray.setContextMenu(self.tray_menu)
        self.tray.activated.connect(lambda reason: self.show_spotlight(reason=reason))

    def show_spotlight(self, **kwargs):
        def focus_windows():  # Only way to focus UI on Windows
            mouse = Controller()
            # mouse position before focus
            mouse_pos_before = mouse.position
            # changing the mouse position for click
            target_pos_x = ui.pos().x() + ui.textbox.pos().x()
            target_pos_y = ui.pos().y() + ui.textbox.pos().y()
            mouse.position = (target_pos_x, target_pos_y)
            mouse.click(Button.left)
            mouse.position = mouse_pos_before

        if kwargs and kwargs["reason"] != 3:
            # if kwargs contains "reason" this has been invoked by the tray icon being clicked
            # reason = 3 means the icon has been left-clicked, so anything other than a left click
            # should open the context menu
            return

        ui = self.spotlight
        ui.show()
        ui.raise_()
        ui.activateWindow()
        ui.function_row.refresh(None)  # refreshes function row button icons

        if sys.platform == "win32":
            focus_windows()

    @staticmethod
    def exit():
        return sys.exit()


if __name__ == "__main__":
    application = App()
    application.run()
