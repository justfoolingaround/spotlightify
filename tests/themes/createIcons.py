from settings import Theme, themes

Theme.read_themes_from_file()  # saves to the themes dict

themes_dict = themes

for key, value in themes_dict.items():
    Theme.create_theme_icon(value)
