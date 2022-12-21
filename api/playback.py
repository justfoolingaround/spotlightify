import re

import spotipy

from api.limiter import Limiter

TIME_REGEX = re.compile(r"(?:(?:(?P<hour>\d+):)?(?P<minute>\d+):)?(?P<second>\d+)")


class PlaybackFunctions:
    def __init__(self, sp: spotipy.Spotify):
        self.sp = sp

    def skip(self):
        return self.sp.run_coroutine_threadsafe(
            self.sp.controller.next_track(
                to_device=self.sp.client.cluster.active_device_id
            )
        )

    def pause(self):
        if not self.sp.client.cluster.player_state.is_paused:
            return self.sp.run_coroutine_threadsafe(
                self.sp.controller.pause(
                    to_device=self.sp.client.cluster.active_device_id
                )
            )
        else:
            return print("The player is already paused.")

    def resume(self):
        if self.sp.client.cluster.player_state.is_paused:
            return self.sp.run_coroutine_threadsafe(
                self.sp.controller.resume(
                    to_device=self.sp.client.cluster.active_device_id
                )
            )
        else:
            return print("The player is already playing.")

    def previous(self):
        return self.sp.run_coroutine_threadsafe(
            self.sp.controller.previous_track(
                to_device=self.sp.client.cluster.active_device_id
            )
        )

    def goto(self, time):

        time_frame = TIME_REGEX.match(time)

        if time_frame is None:
            return print(
                "Could not parse time. A valid time format may be 1:40, 40 or even 1:40:00."
            )

        time_in_seconds = 0

        if time_frame.group("hour"):
            time_in_seconds += int(time_frame.group("hour")) * 60 * 60

        if time_frame.group("minute"):
            time_in_seconds += int(time_frame.group("minute")) * 60

        if time_frame.group("second"):
            time_in_seconds += int(time_frame.group("second"))

        print("seeking to " + str(time_in_seconds))
        return self.sp.run_coroutine_threadsafe(
            self.sp.controller.seek(
                float(time_in_seconds * 1000),
                to_device=self.sp.client.cluster.active_device_id,
            )
        )

    @Limiter.rate_limiter(seconds=10)
    def get_current_song_info(self) -> dict:

        track = self.sp.client.cluster.player_state.track

        if track is None:
            return {"name": "Nothing Currently Playing", "artist": ""}

        track_id = track.uri[14:]

        data = self.sp.run_coroutine_threadsafe(
            self.sp.controller.query_entity_metadata(track_id, "track")
        )

        images = data["album"]["cover_group"]["image"]

        if images:
            image = "https://i.scdn.co/image/" + images[-1]["file_id"]
        else:
            image = None

        return {
            "name": data["name"],
            "artist": ", ".join(artist["name"] for artist in data["artist"]),
            "image": image,
            "id": track_id,
        }
