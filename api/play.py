from queue import Queue

import spotipy

from .playback import PlaybackFunctions


class PlayFunctions(PlaybackFunctions):
    def __init__(self, sp: spotipy.Spotify, queue: Queue):
        self.__queue = queue
        super().__init__(sp)

    def term(self, term: str):

        results = self.sp.search(term, limit=1, market="GB", type="track")["tracks"][
            "items"
        ]

        if len(results) == 0:
            return print(f"[Error] Unable to get results by searching {term!r}")

        track_uri = results[0]["uri"]

        return self.uri(track_uri)

    def uri(self, uri: str):

        try:
            self.sp.run_coroutine_threadsafe(
                self.sp.controller.play(
                    uri, to_device=self.sp.client.cluster.active_device_id
                )
            )
        except Exception as e:
            return print(f"[Error] Could not play {uri!r} due to: {e}")

        self.__queue.put(self.sp.track(uri))

    def id(self, id_: str, type_: str):
        return self.uri(f"spotify:{type_}:{id_}")

    def liked_songs(self):
        return self.sp.run_coroutine_threadsafe(
            self.sp.controller.play(f"spotify:user:{self.sp.me()['id']}:collection")
        )

    def queue_uri(self, uri: str):
        try:
            self.sp.run_coroutine_threadsafe(
                self.sp.controller.add_track_to_queue(
                    uri, to_device=self.client.cluster.active_device_id
                ),
            )
        except Exception as e:
            return print(f"[Error] Could not queue song from URI due to: {e}")

        track = self.sp.track(uri)
        self.__queue.put(track)

    def queue_id(self, id_: str):
        return self.queue_uri(f"spotify:track:{id_}")

    def queue_term(self, term: str):

        search_results = self.sp.search(term, limit=1, market="GB", type="track")[
            "tracks"
        ]["items"]

        if len(search_results) == 0:
            return print(f"[Error] Unable to get results by searching {term!r}")

        uri = search_results[0]["uri"]
        self.queue_uri(uri)

    def song_recommendations(self, id_: str):  # like a radio
        results = self.sp.recommendations(seed_tracks=[id_], limit=50)

        if len(results["tracks"]) == 0:
            return print(f"[Error] Could not find results by using the queue")

        uris = [track["uri"] for track in results["tracks"]]

        return self.sp.run_coroutine_threadsafe(
            self.sp.controller.add_tracks_to_queue(
                track_uris=uris, to_device=self.client.cluster.active_device_id
            )
        )
