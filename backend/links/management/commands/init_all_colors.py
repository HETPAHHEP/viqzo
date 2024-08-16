from csv import reader
from pathlib import Path

from django.db.transaction import atomic
from django.core.management import BaseCommand, CommandError

from links.models import Color
from viqzo.settings import BASE_DIR
from links.services.colors import Color as ColorChecker


class Command(BaseCommand):
    """Команда Django для создания заданных цветов"""

    help = (
        "Creating records in the database of all "
        "initially specified colors for the “Color” model."
    )

    def __check_and_init_colors_from_csv(
        self, file_path
    ) -> (int, list[ColorChecker]):
        """Чтение цветов из файла и их проверка с помощью Dataclass"""
        with open(file_path, encoding="utf-8") as file:
            csv_reader = reader(file)
            new_colors = []
            total = -1

            for name, color_hex in csv_reader:
                if total == -1:
                    total += 1
                    continue

                try:
                    new_colors.append(
                        ColorChecker(name=name, color_hex=color_hex)
                    )
                    total += 1
                except ValueError as e:
                    self.stderr.write(
                        f'Error report problem:\n\n'
                        f'ID ROW: {total}\n\n'
                        f'ROW: {name, ' ', color_hex}\n\n'
                        f'Error details: {str(e)}'
                    )
                    raise CommandError(
                        "Error while checking new colors"
                    ) from e

        return total, new_colors

    @atomic()
    def __create_new_colors(self, colors: list[ColorChecker]) -> None:
        """Создание записей цветов в базе данных"""
        for color in colors:
            try:
                Color.objects.create(
                    name=color.name, color_hex=color.color_hex
                )
            except ValueError as e:
                self.stderr.write(
                    f"Error report problem:\n\n"
                    f"Color name: {color.name}\n\n"
                    f"Color HEX: {color.color_hex}\n\n"
                    f"Error details: {str(e)}"
                )
                raise CommandError("Error while creating new colors") from e

    def _get_colors_from_csv(self) -> None:
        """Чтение файла и старт других функции для создания цветов"""
        csv_file = "colors.csv"
        path_to_csv = Path(BASE_DIR).joinpath(f"resources/{csv_file}")

        if path_to_csv.exists():
            try:
                counter, colors = self.__check_and_init_colors_from_csv(
                    path_to_csv
                )
                self.__create_new_colors(colors)
            except CommandError as e:
                self.stdout.write(
                    style_func=self.style.ERROR,
                    msg="Closing command while error",
                )
                raise CommandError from e

            self.stdout.write(
                self.style.SUCCESS(
                    f"{Color.__name__} data from {csv_file} "
                    f"imported successfully. "
                    f"Total colors: {counter}"
                )
            )
        else:
            raise CommandError(
                f"CSV file not found! Check that the file "
                f"is on the path {path_to_csv}"
            )

    def handle(self, *args, **options):
        """Старт команды"""
        self._get_colors_from_csv()
