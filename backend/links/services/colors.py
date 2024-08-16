import re
from re import Pattern
from csv import reader
from pathlib import Path
from dataclasses import dataclass

from PIL import Image, ImageDraw

from core.enums import Limits
from viqzo.settings import BASE_DIR


@dataclass
class Color:
    name: str
    color_hex: str

    HEX_COLOR_REGEX: Pattern = re.compile(
        r"^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$"
    )

    def __post_init__(self):
        if not self.is_valid_hex_color(self.color_hex):
            raise ValueError("Недопустимый hex формат цвета")

        if len(self.name) > Limits.MAX_LEN_COLOR_NAME:
            raise ValueError(
                f"Длинна названия цвета не может быть больше "
                f"{Limits.MAX_LEN_COLOR_NAME}"
            )

    @classmethod
    def is_valid_hex_color(cls, color_hex: str) -> bool:
        return bool(cls.HEX_COLOR_REGEX.match(color_hex))


__test_colors_palette = [
    Color(name="Light pink", color_hex="#FF579F"),
    Color(name="Light cyan", color_hex="#34E5FF"),
    Color(name="Bright blue", color_hex="#3185FC"),
    Color(name="Light magenta", color_hex="#FF49FF"),
    Color(name="Yellow Yandex", color_hex="#FFCC00"),
    Color(name="Mostly pure green", color_hex="#80FF00"),
    Color(name="Light cyan - lime green", color_hex="#37FF8B"),
    Color(name="Vivid orange", color_hex="#FE5A1D"),
    Color(name="Palatinate blue", color_hex="#273BE2"),
    Color(name="Bright red", color_hex="#ED254E"),
    Color(name="Bright yellow", color_hex="#FEE440"),
    Color(name="Pure orange", color_hex="#FE7500"),
    Color(name="Dark cyan", color_hex="#177E89"),
    Color(name="Pure violet", color_hex="#8000FF"),
    Color(name="Soft blue and purple", color_hex="#7765E3"),
    Color(name="Cornflowerblue", color_hex="#6495ED"),
    Color(name="American pink", color_hex="#FF033E"),
    Color(name="Salmon-orange", color_hex="#E55137"),
    Color(name="Coral", color_hex="#FF7F50"),
    Color(name="Verdepom green", color_hex="#34C924"),
]


def __get_colors_from_csv() -> (int, list[Color]):
    csv_file = "colors.csv"
    path_to_csv = Path(BASE_DIR).joinpath(f"resources/{csv_file}")

    if path_to_csv.exists():
        with open(path_to_csv, encoding="utf-8") as file:
            csv_reader = reader(file)

            new_colors = []
            total = -1

            for name, color_hex in csv_reader:
                if total == -1:
                    total += 1
                    continue

                try:
                    new_colors.append(Color(name=name, color_hex=color_hex))
                    total += 1
                except ValueError as e:
                    raise ValueError(
                        f"Error during command execution. Detail: {e}. "
                        f"Row: {name, ' ', color_hex}"
                    ) from e

            return total, new_colors
    else:
        raise FileNotFoundError("CSV file not found!")


def __view_colors(colors_palette):
    """Для просмотра цветов при разработке"""

    # Создаем изображение с заданными размерами
    image_width = 100
    image_height = 100 * len(colors_palette)
    image = Image.new("RGB", (image_width, image_height))
    draw = ImageDraw.Draw(image)

    # Рисуем прямоугольник для каждого цвета
    y = 0
    for color in colors_palette:
        draw.rectangle(((0, y), (image_width, y + 100)), fill=color.color_hex)
        y += 100

        # Сохраняем изображение на диск
        image_path = "colors_prev.png"
        image.save(image_path)


if __name__ == "__main__":
    # Просмотр готовой тестовой палитры цветов из кода
    # __view_colors(__test_colors_palette)

    # Просмотр палитры цветов из CSV файла
    total_colors, colors = __get_colors_from_csv()

    if colors:
        __view_colors(colors)
        print(f"Done! Total colors in preview: {total_colors}")
