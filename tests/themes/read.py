from settings import Theme, themes

Theme.read_themes_from_file()  # saves to the themes dict

themes_dict = themes

print(themes_dict)
