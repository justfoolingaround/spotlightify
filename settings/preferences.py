import json
from definitions import CACHE_DIR
from settings import themes
from settings.themes import Theme
from auth import config
from ui import SpotlightUI


class Preferences:
    """Pref file for settings such as theming, and other general settings."""

    __instance__ = None

    def __init__(self):
        self.__config = config
        self.__current_theme = None
        self.ui = SpotlightUI.get_instance()

        self.load_preferences()

        # READ IN THEMES/SETTINGS
        if Preferences.__instance__ is None:
            Preferences.__instance__ = self

    def load_preferences(self):
        Theme.read_themes_from_file()
        self.current_theme = themes["Dark"]

    @property
    def current_theme(self):
        return self.__current_theme

    @current_theme.setter
    def current_theme(self, theme: Theme):
        # means that theme will not pointlessly change the color of svg assets when preferences are loaded at startup
        try:
            if self.__current_theme is not None:
                Theme.change_theme(theme)
            self.ui.change_theme(theme)
            self.__current_theme = theme
        except:
            print("[Warning] Theme not found. Defaulting to 'Dark' theme")
            t = themes["dark"]
            Theme.change_theme(t)
            self.ui.change_theme(t)
            self.__current_theme = t

    @staticmethod
    def get_instance():
        if Preferences.__instance__ is not None:
            return Preferences.__instance__
        else:
            raise Exception("[Error] No Preferences class instantiated")
