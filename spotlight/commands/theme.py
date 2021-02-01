from spotlight.commands.command import Command
from spotlight.suggestions.theme import ThemeMenuSuggestion


class ThemeCommand(Command):
    def __init__(self):
        Command.__init__(self, "Themes", "Change the Spotlightify theme", "themes")

    def get_suggestions(self, parameter=""):
        if parameter == "":
            return [ThemeMenuSuggestion()]

