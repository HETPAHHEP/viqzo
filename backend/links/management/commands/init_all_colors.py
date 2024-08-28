from csv import reader
from pathlib import Path

from django.db import DatabaseError, IntegrityError
from django.conf import settings
from django.db.transaction import atomic
from django.core.management import BaseCommand, CommandError

from links.models import Color
from links.services.colors import Color as ColorChecker


class Command(BaseCommand):
    """Команда Django для создания заданных цветов."""

    help = (
        "Creating records in the database of all "
        "initially specified colors for the “Color” model."
    )

    def __delete_all_colors_(self) -> None:
        """Удаление всех записей цветов из базы данных"""
        if not Color.objects.exists():
            self.stdout.write(
                "All colors in the database have already been cleared!\n",
                style_func=self.style.WARNING,
            )
            return

        try:
            Color.objects.all().delete()
        except IntegrityError as e:
            self.stderr.write(
                f"IntegrityError while deleting.\n\n" f"Details: \n{e}\n\n"
            )
            raise CommandError(
                "Error when deleting colors from database"
            ) from e
        except DatabaseError as e:
            self.stderr.write(
                f"DatabaseError while deleting\n\n" f"Details: \n{e}\n\n"
            )
            raise CommandError(
                "Error when deleting colors from database"
            ) from e

        self.stdout.write(
            "DB is completely cleared of colors!\n",
            style_func=self.style.SUCCESS,
        )

    def __prepare_db_for_actions(self, options) -> None:
        """
        Проверка заполненности базы уже какими-либо цветами
        и подготовка к дальнейшим действиям.
        """
        if not Color.objects.exists():
            return

        if options["force"]:
            self.__delete_all_colors_()

        else:
            self.stderr.write(
                "The colors have not been cleared!\n"
                "Use the '--force' "
                "flag to completely remove all colors entries\n\n"
            )
            raise CommandError("Error while preparing DB")

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

    def _get_colors_from_csv(self, options) -> None:
        """Чтение файла и старт других функции для создания цветов"""
        csv_file = "colors.csv"
        path_to_csv = Path(settings.BASE_DIR).joinpath(f"resources/{csv_file}")

        if path_to_csv.exists():
            try:
                self.__prepare_db_for_actions(options)
                counter, colors = self.__check_and_init_colors_from_csv(
                    path_to_csv
                )
                self.__create_new_colors(colors)
            except CommandError as e:
                self.stdout.write(
                    style_func=self.style.ERROR,
                    msg="Closing command while error",
                )
                raise CommandError(f"{e}") from e

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

    def add_arguments(self, parser):
        """Добавление аргументов"""
        parser.add_argument(
            "--force",
            action="store_true",
            help="Force the database to be prepared to add new colors.",
        )
        parser.add_argument(
            "--delete-colors",
            action="store_true",
            help="Just delete all colors entries from DB.",
        )

    def handle(self, *args, **options):
        """Старт команды"""
        if options.get("delete_colors", False):
            self.__delete_all_colors_()
        else:
            self._get_colors_from_csv(options)
