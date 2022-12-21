from typing import List

from api.limiter import Limiter


class MiscFunctions:
    def __init__(self, sp):
        self.sp = sp

    @Limiter.rate_limiter(seconds=10)
    def get_device_list(self) -> list:
        try:
            devices = self.sp.devices()["devices"]
            return devices
        except:
            print("[Error] Cannot get list of devices")
            return None

    def set_device(self, id_: str):
        return self.sp.run_coroutine_threadsafe(
            self.sp.controller.transfer_across_device(id_)
        )

    def set_default_device(self):
        return self.set_device(self.get_device_list()[0]["id"])

    def set_volume(self, value: int):
        """
        Changes the volume of the currently playing device
        :param value: int between 1 and 10
        """
        self.sp.run_coroutine_threadsafe(
            self.sp.controller.set_volume(
                value * 10, to_device=self.sp.client.cluster.active_device_id
            )
        )

    @Limiter.rate_limiter(seconds=20)
    def get_user_playlists(self) -> List[dict]:
        return self.sp.current_user_playlists(limit=50)["items"]
