from os import mkdir, path
from threading import Thread

from spotipy import Spotify

from caching.queues import ImageQueue, SongQueue
from caching.threads import (
    AlbumCacheThread,
    ArtistCacheThread,
    ImageCacheThread,
    LikedCacheThread,
    PlaylistCacheThread,
    SongCacheThread,
)
from definitions import CACHE_DIR


class CacheManager(Thread):

    title = "spotlightify.cache_manager"

    def __init__(self, sp: Spotify, song_queue: SongQueue, image_queue: ImageQueue):
        Thread.__init__(self)
        self.create_cache()
        self.sp = sp
        self.song_queue = song_queue
        self.image_queue = image_queue

        # NOTE: These wait for songs to be added to their respective queues before caching them.

        threads = (
            SongCacheThread,
            ImageCacheThread,
            # NOTE: These run on startup of the application and skip caching if the file they wish to alter have been
            # updated within the last day.
            PlaylistCacheThread,
            LikedCacheThread,
            AlbumCacheThread,
            ArtistCacheThread,
        )

        self.threads = [
            thread(self.sp, self.song_queue, self.image_queue) for thread in threads
        ]

    @staticmethod
    def create_cache():
        if not path.exists(CACHE_DIR):
            mkdir(CACHE_DIR)

        art_path = f"{CACHE_DIR}art"
        if not path.exists(art_path):
            mkdir(art_path)

    def has_running_tasks(self):
        return False
        return any(thread.is_working for thread in self.threads)

    def run(self):
        for thread in self.threads:
            thread.start()

        return super().run()
