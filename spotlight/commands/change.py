from spotipy import Spotify

from api.check import CheckFunctions
from api.manager import PlaybackManager
from spotlight.commands.command import Command
from spotlight.suggestions.menu import MenuSuggestion
from spotlight.suggestions.templates import ExecutableSuggestion


class LikeCommand(Command):
    def __init__(self, sp: Spotify):
        Command.__init__(
            self, "Like", "Add the currently playing song to Saved playlist", "like"
        )
        self.sp = sp
        # The rate limiter requires the same is_song_liked method to run for it to properly limit API requests
        self.liked = CheckFunctions(self.sp).is_song_liked

    def get_suggestions(self, parameter=""):
        if parameter != "":
            return []
        liked = self.liked()
        item_list = []
        if liked:
            item_list.append(
                ExecutableSuggestion(
                    "Unlike",
                    "Remove the currently playing song from your Liked Songs",
                    "heart-no-fill",
                    PlaybackManager.toggle_like_song,
                )
            )
        else:
            item_list.append(
                ExecutableSuggestion(
                    "Like",
                    "Add the currently playing song to your Liked Songs",
                    "heart",
                    PlaybackManager.toggle_like_song,
                )
            )
        return item_list


class RepeatCommand(Command):
    def __init__(self, sp):
        self.sp = sp

        Command.__init__(
            self, "Repeat", "Change the repeat state of your Spotify player", "repeat"
        )

    def get_suggestions(self, parameter=None):

        options = self.sp.client.cluster.player_state.options

        return [
            MenuSuggestion(
                self.title,
                self.description,
                "repeat",
                "repeat",
                [
                    ExecutableSuggestion(
                        "context",
                        f"Toggle repeat of context (currently {'not ' if not options.repeating_context else ''}repeating)",
                        "repeat",
                        lambda _: PlaybackManager.toggle_repeat(_, "context"),
                    ),
                    ExecutableSuggestion(
                        "track",
                        f"Toggle repeat of track (currently {'not ' if not options.repeating_track else ''}repeating)",
                        "repeat",
                        lambda _: PlaybackManager.toggle_repeat(_, "track"),
                    ),
                ],
            )
        ]


class ShuffleCommand(Command):
    def __init__(self, sp: Spotify):
        Command.__init__(self, "Shuffle", "Change Shuffle State", "shuffle")
        self.sp = sp

    def get_suggestions(self, parameter=None):

        if self.sp.client.cluster.player_state.options.shuffling_context:
            current_state, next_state = "ON", "OFF"
        else:
            current_state, next_state = "OFF", "ON"
        return [
            ExecutableSuggestion(
                "Shuffle",
                f"Shuffle is {current_state}. Turn {next_state}",
                "shuffle",
                PlaybackManager.toggle_shuffle,
            )
        ]
