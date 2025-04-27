import copy

from scripts.install.colors_definer import ColorsDefiner
from scripts.types.installation_color import InstallationMode, InstallationColor
from scripts.utils.color_converter.color_converter import ColorConverter


class ColorReplacementGenerator:
    def __init__(self, colors_provider: ColorsDefiner, color_converter: ColorConverter):
        self.colors = copy.deepcopy(colors_provider)
        self.color_converter = color_converter

    def convert(self, mode: InstallationMode, theme_color: InstallationColor) -> list[tuple[str, str]]:
        """Generate a list of color replacements for the given theme color and mode"""
        return [
            (element, self._create_rgba_value(element, mode, theme_color))
            for element in self.colors.replacers
        ]

    def _create_rgba_value(self, element: str, mode: str, theme_color: InstallationColor) -> str:
        """Create RGBA value for the specified element"""
        color_def = self._get_color_definition(element, mode)

        h = color_def.get("h", theme_color.hue)
        s = int(color_def["s"]) / 100
        l = int(color_def["l"]) / 100
        alpha = color_def["a"]

        if theme_color.saturation is not None:
            s *= theme_color.saturation / 100

        red, green, blue = self.color_converter.hsl_to_rgb(h, s, l)

        return f"rgba({red}, {green}, {blue}, {alpha})"

    def _get_color_definition(self, element: str, mode: str) -> dict:
        """Get color definition for element, handling defaults if needed"""
        replacer = self.colors.replacers[element]

        if mode not in replacer and replacer["default"]:
            default_element = replacer["default"]
            return self.colors.replacers[default_element][mode]

        return replacer[mode]
