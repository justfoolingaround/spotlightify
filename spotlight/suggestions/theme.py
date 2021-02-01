from api.manager import PlaybackManager
from settings import themes, Theme
from spotlight.suggestions.menu import MenuSuggestion
from spotlight.suggestions.options import OptionSuggestion
from spotlight.suggestions.templates import ExecutableSuggestion, PassiveSuggestion


class ThemeMenuSuggestion(MenuSuggestion):
    def __init__(self):
        MenuSuggestion.__init__(self, "Themes", "Change the Spotlightify theme", "theme-icon", "Themes ", [])

    def refresh_menu_suggestions(self):
        suggestions = []
        Theme.read_themes_from_file()
        suggestions.append(CreateThemeSuggestion())
        for key, value in themes.items():
            suggestions.append(
                ThemeSuggestion(key, key, value))
        self.menu_suggestions = suggestions


class CreateThemeSuggestion(ExecutableSuggestion):
    def __init__(self):
        ExecutableSuggestion.__init__(self, "Create Theme", "Create your own Spotlightify theme", "plus", lambda: None)


class ThemeSuggestion(OptionSuggestion):
    def __init__(self, name, icon_name, theme):
        OptionSuggestion.__init__(self, name, f"Set {name} as the active theme", f"t-{icon_name}",
                                  PlaybackManager.set_active_theme, "", theme, "exe")
        self.option_suggestions = [PassiveSuggestion(name, "Options", f"t-{icon_name}"),
                                   ExecutableSuggestion("Set as Active Theme", f"Set '{name}' as the active theme",
                                                        "tick", PlaybackManager.set_active_theme, theme),
                                   EditThemeSuggestion(name, theme),
                                   DeleteThemeSuggestion(name)]


class EditThemeSuggestion(ExecutableSuggestion):
    def __init__(self, name, theme):
        ExecutableSuggestion.__init__(self, "Edit Theme", f"Edit the '{name}' theme", "edit", lambda: None, parameter=theme)


class DeleteThemeSuggestion(ExecutableSuggestion):
    def __init__(self, name):
        ExecutableSuggestion.__init__(self, "Delete Theme", f"Delete the '{name}' theme", "delete", lambda: None)
