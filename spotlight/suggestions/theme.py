from api.manager import PlaybackManager
from settings import themes, Theme
from spotlight.suggestions.menu import MenuSuggestion
from spotlight.suggestions.templates import ExecutableSuggestion


class ThemeMenuSuggestion(MenuSuggestion):
    def __init__(self):
        MenuSuggestion.__init__(self, "Themes", "Change the Spotlightify theme", "theme-icon", "Themes ", [])

    def refresh_menu_suggestions(self):
        items = ThemeMenuItems.create_items()

        self.menu_suggestions = items


class ThemeMenuItems:
    @staticmethod
    def create_items():
        return [CreateThemeMenuSuggestion(), ChangeThemeMenuSuggestion(), OpenThemeFolderSuggestion()]


class CreateThemeMenuSuggestion(ExecutableSuggestion):
    def __init__(self):
        ExecutableSuggestion.__init__(self, "Create Theme", "Create your own Spotlightify theme", "theme-icon", lambda: None)


class ChangeThemeMenuSuggestion(MenuSuggestion):
    def __init__(self):
        MenuSuggestion.__init__(self, "Change Theme", "Select the Spotlightify theme", "theme-icon", "", [],
                                fill_prefix=False)

    def refresh_menu_suggestions(self):
        suggestions = []
        Theme.read_themes_from_file()
        for key, value in themes.items():
            suggestions.append(
                ExecutableSuggestion(key, f"Set {key} as active theme", f"t-{key}", PlaybackManager.set_active_theme,
                                     value))
        self.menu_suggestions = suggestions


class OpenThemeFolderSuggestion(MenuSuggestion):
    def __init__(self):
        MenuSuggestion.__init__(self, "Open Theme Folder", "Add, delete or modify theme files", "theme-icon", "", [],
                                fill_prefix=False)

    def refresh_menu_suggestions(self):
        self.menu_suggestions = []
