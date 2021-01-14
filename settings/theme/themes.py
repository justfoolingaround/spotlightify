from definitions import CACHE_DIR, ASSETS_DIR, sep
import os
import json
import re


class Theme(object):

    def __init__(self, name: str, background: str, foreground: str, accent: str, hover: str, focus: str):
        self.__background = background
        self.__foreground = foreground
        self.__accent = accent
        self.__name = name
        self.__hover = hover
        self.__focus = focus

    @property
    def focus(self):
        return self.__focus

    @focus.setter
    def focus(self, value):
        self.__focus = value

    @property
    def hover(self):
        return self.__hover

    @hover.setter
    def hover(self, value):
        self.__hover = value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def background(self):
        return self.__background

    @background.setter
    def background(self, value):
        self.__background = value

    @property
    def foreground(self):
        return self.__foreground

    @foreground.setter
    def foreground(self, value):
        self.__foreground = value

    @property
    def accent(self):
        return self.__accent

    @accent.setter
    def accent(self, value):
        self.__accent = value

    def to_dict(self) -> dict:
        th_dict = {
            "name": self.name,
            "foreground": self.foreground,
            "background": self.background,
            "accent": self.accent,
            "hover": self.hover,
            "focus": self.focus
        }
        return th_dict

    @staticmethod
    def read_themes_from_file():
        """
        Reads themes from the JSON theme file and stores them in the `themes` dictionary within the themes.py file
        :return: list of themes read in from JSON files
        """

        path = f"{CACHE_DIR}themes.json"

        themes_dict = {}
        with open(f'{path}') as f:  # load themes JSON
            themes_dict = dict(json.load(f))

        items = dict(themes_dict).items()
        for key, values in items:  # load each theme
            obj = Theme(key, values["background"], values["foreground"], values["accent"], values["hover"], values["focus"])
            themes[key] = obj

    @staticmethod
    def change_theme(theme):
        """
        Changes all SVG fills to the correct accent colour
        :return:
        """
        try:
            if theme is None:
                raise Exception("[Error] Theme not found")

            path = f"{ASSETS_DIR}svg{sep}"
            file_names = os.listdir(path)
            for file in file_names:
                if file[:2] == "t-":  # skips icons which have the theme icon prefix 't-'
                    continue
                text = ""
                with open(f'{path}{file}', 'r') as f:  # change all svg fills to accent colour
                    text = f.read()
                    text = re.sub('fill="(.*?)"', f'fill="{theme.accent}"', text)
                with open(f'{path}{file}', 'w') as f:
                    f.write(text)

        except Exception as ex:
            print(ex)

    @staticmethod
    def create_theme_icon(theme):
        try:
            path = f"{ASSETS_DIR}svg{sep}t-{theme.name}.svg"
            f = open(path, "w")
            f.write(theme_icon_template(theme.foreground, theme.background, theme.accent))
            f.close()
        except:
            print("[Warning] Cannot create icon for theme.")


# all themes are stored in this object
themes = {"Dark": Theme("Dark", "#191414", "#B3B3B3", "#1ED760", "#251e1e", "#3f3232"),
          "Light": Theme("Light", "#B3B3B3", "#191414", "#332929", "#251e1e", "#3f3232")}


def theme_icon_template(foreground, background, accent):
    return f'''<svg width="300" height="300" xmlns="http://www.w3.org/2000/svg">
 <g>
  <title>background</title>
  <rect fill="#fff" id="canvas_background" height="602" width="802" y="-1" x="-1"/>
  <g display="none" overflow="visible" y="0" x="0" height="100%" width="100%" id="canvasGrid">
   <rect fill="url(#gridpattern)" stroke-width="0" y="0" x="0" height="100%" width="100%"/>
  </g>
 </g>
 <g>
  <title>Layer 1</title>
  <rect id="svg_2" height="100" width="300" y="0" x="0" stroke-opacity="null" stroke-width="0" stroke="#000" fill="{accent}"/>
  <rect id="svg_4" height="100" width="300" y="100" x="0" stroke-opacity="null" stroke-width="0" stroke="#000" fill="{background}"/>
  <rect id="svg_5" height="100" width="300" y="200" x="0" stroke-opacity="null" stroke-width="0" stroke="#000" fill="{foreground}"/>
 </g>
</svg>'''
