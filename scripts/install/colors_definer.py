import json


class ColorsDefiner:
    replacers: dict[str, dict[str, dict[str, int]]]

    colors: dict[str, dict[str, int]]

    def __init__(self, filename):
        colors_dict = json.load(open(filename))
        self.replacers = colors_dict["elements"]
        self.colors = colors_dict["colors"]

    def get_color(self, color_name: str):
        """Get the full color definition (h, s, l, a) for a given color"""
        if color_name in self.colors:
            return self.colors[color_name]
        else:
            raise ValueError(f"Color '{color_name}' not found in colors definition.")