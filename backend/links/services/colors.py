from typing import Pattern
from dataclasses import dataclass, field
import re

from PIL import Image, ImageDraw


@dataclass
class Color:
    color_hex: str

    HEX_COLOR_REGEX: Pattern = re.compile(
        r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$'
    )

    def __post_init__(self):
        if not self.is_valid_hex_color(self.color_hex):
            raise ValueError('Недопустимый hex формат цвета')

    @classmethod
    def is_valid_hex_color(cls, color_hex: str) -> bool:
        return bool(cls.HEX_COLOR_REGEX.match(color_hex))


colors_palette = [
    Color(color_hex='#FF579F'),
    Color(color_hex='#34E5FF'),
    Color(color_hex='#3185FC'),
    Color(color_hex='#FF49FF'),
    Color(color_hex='#FFFF00'),
    Color(color_hex='#80FF00'),
    Color(color_hex='#37FF8B'),
    Color(color_hex='#FE5A1D'),
    Color(color_hex='#273BE2'),
    Color(color_hex='#ED254E'),
    Color(color_hex='#FEE440'),
    Color(color_hex='#FF7F11'),
    Color(color_hex='#177E89'),
    Color(color_hex='#8000FF'),
    Color(color_hex='#7765E3'),
    Color(color_hex='#3B60E4'),
    Color(color_hex='#FFC914'),
    Color(color_hex='#E4572E'),
    Color(color_hex='#CE1483'),
    Color(color_hex='#31CB00'),
]


def __view_colors(colors):
    """Для просмотра цветов при разработке"""

    # Создаем изображение с заданными размерами
    image_width = 100
    image_height = 100 * len(colors)
    image = Image.new("RGB", (image_width, image_height))
    draw = ImageDraw.Draw(image)

    # Рисуем прямоугольник для каждого цвета
    y = 0
    for color in colors:
        draw.rectangle([(0, y), (image_width, y + 100)], fill=color.color_hex)
        y += 100

        # Сохраняем изображение на диск
        image_path = "colors_prev.png"
        image.save(image_path)


if __name__ == '__main__':
    __view_colors(colors_palette)
