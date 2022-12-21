import spotipy

from api import check


class ToggleFunctions:
    def __init__(self, sp):
        self.sp = sp
        self._check = check.CheckFunctions(sp)

    def like_song(self):
        """
        Likes the current song playing
        """
        try:
            current_song_uri = self.sp.current_user_playing_track()["item"]["uri"]
            if self._check.is_song_liked():
                self.sp.current_user_saved_tracks_delete([current_song_uri])
            else:
                self.sp.current_user_saved_tracks_add([current_song_uri])
        except:
            print("[Error] Song like could not be toggled")

    def shuffle(self):
        options = self.sp.client.cluster.player_state.options

        if options is None:
            return

        try:
            return self.sp.run_coroutine_threadsafe(
                self.sp.controller.set_shuffle(not options.shuffling_context)
            )
        except Exception as e:
            print(f"[Error] Could not toggle shuffle due to: {e!r}")

    def playback(self):

        if self.sp.client.cluster.player_state.is_paused:
            return self.sp.run_coroutine_threadsafe(self.sp.controller.resume())

        return self.sp.run_coroutine_threadsafe(self.sp.controller.pause())

    def repeat(self, state="context"):

        if state == "context":

            return self.sp.run_coroutine_threadsafe(
                self.sp.controller.set_repeat(
                    context=not self.sp.client.cluster.player_state.options.repeating_context
                )
            )

        if state == "track":

            return self.sp.run_coroutine_threadsafe(
                self.sp.controller.set_repeat(
                    track=not self.sp.client.cluster.player_state.options.repeating_track
                )
            )

        raise ValueError(f"Invalid state: {state!r}")
