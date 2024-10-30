from csv import reader
from pathlib import Path

from django.core.files import File
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from .validators import Link


class LinksParser:
    """Класс для импорта/экспорта ссылок пользователя"""

    def __init__(
        self,
        user,
        file,
        new_group_name: str | None = None,
        existing_group: int | None = None,
    ):
        self.user = user
        self.file = file
        self.group = new_group_name if new_group_name else existing_group

    def _check_file_extension(self):
        self.file_extension = Path(str(self.file)).suffix[1:].lower()

        return self.file_extension

    def _parse_links_from_csv(self):
        with open(self.file, "utf-8") as file_csv:
            csv_reader = reader(file_csv)
            header_link, header_alis = csv_reader[0]

            if header_link != "link" and (
                header_alis is not None and header_alis != "alias"
            ):
                raise ValidationError(
                    {
                        "csv_error": _(
                            "Заголовки CSV файла не "
                            "соответствуют ожидаемым полям link | alias"
                        )
                    }
                )

            links = []

            for link, alias in csv_reader[1:]:
                try:
                    links.append(Link(link=link, alias=alias))
                except ValueError as e:
                    raise ValidationError from e

                except ValidationError as e:
                    raise ValidationError from e

            return links

    def _parse_links_from_json(self):
        pass

    def _create_group_for_links(self):
        pass

    def _add_parsed_links_to_db(self, file: File):
        pass

    def _start_parsing(self):
        self._check_file_extension()

        if self.file_extension == "csv":
            pass

        if self.file_extension == "json":
            pass
