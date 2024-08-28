from csv import reader
from http import HTTPStatus
from pathlib import Path

from django.conf import settings


def create_short_link(client, valid_original_link) -> str:
    """Создание обычной короткой ссылки.

    :returns code: Код для созданной короткой ссылки
    """

    response = client.post("/api/links/", data=valid_original_link)
    assert response.status_code == HTTPStatus.CREATED, (
        f"POST-запрос с валидной ссылкой от неавторизованного пользователя "
        f"на api/links/ для создания короткого кода не возвращает ответ "
        f"со статусом 201.\n"
        f"Детали: {response.data}"
    )

    code = response.data.get("short")
    if code:
        return code

    raise KeyError("Короткий код для ссылки отсутствует при создании")


def create_alias_link(client, original_link_with_alias) -> str:
    """Создание пользовательской короткой ссылки.

    :returns code: Выбранное имя для созданной короткой ссылки
    """

    response = client.post("/api/links/", data=original_link_with_alias)
    assert response.status_code == HTTPStatus.CREATED, (
        f"POST-запрос с валидной ссылкой и alias от неавторизованного пользователя "
        f"на api/links/ для создания пользовательского кода не возвращает ответ со статусом 201.\n"
        f"Детали: {response.data}"
    )

    code = response.data.get("short")
    if code:
        return code

    raise KeyError("Пользовательский код для ссылки отсутствует при создании")


def create_usergroup(client, name_for_usergroup) -> int:
    """Создание группы для пользовательских ссылок.

    :returns group_id: Id созданной группы
    """

    response = client.post("/api/groups/", data=name_for_usergroup)

    assert response.status_code == HTTPStatus.CREATED, (
        f"POST-запрос с именем от пользователя "
        f"на api/groups/ для создания группы не возвращает ответ "
        f"со статусом 201.\n"
        f"Детали: {response.data}"
    )

    group_id = response.data.get("id")

    if group_id:
        return group_id

    raise KeyError("Id группы отсутствует в ответе при её создании")


def create_all_groups(client, groups: list[dict]) -> list[int]:
    """Создание всех групп из словаря с их именами"""
    assert groups, (
        "Отсутствуют группы для создания"
    )

    groups_ids = []

    for group in groups:
        groups_ids.append(
            create_usergroup(client, group)
        )

    assert groups_ids and len(groups_ids) == len(groups),  (
        f"Количество созданных групп не равно количеству переданных\n"
        f"Передано: {len(groups)}"
        f"Создано: {len(groups_ids)} \n"
    )

    return groups_ids


def add_created_group_to_dict(group_id) -> dict:
    """Добавление ID группы в словарь для изменения ссылки"""
    group_dict = {"group": group_id}
    return group_dict


def add_created_group_to_dict_with_link(link, group) -> dict:
    """Добавление в фикстуру со ссылкой ID группы для создания ссылки"""
    link.update({"group": group})

    return link


def create_and_add_short_link_to_group(
    client, original_link, name_group
) -> tuple[str, int]:
    """Создание и добавление ссылки в группу"""

    group_id = create_usergroup(client, name_group)
    link = add_created_group_to_dict_with_link(original_link, group_id)

    response = client.post("/api/links/", data=link)

    assert (
        response.status_code == HTTPStatus.CREATED
        and response.data["group"]["id"] == group_id
    ), (
        f"POST-запрос от авторизованного пользователя "
        f"на /api/links/ для создания short ссылки с группой "
        f"не возвращает ответ со статусом 201 "
        f"(пользователь должен иметь возможность создать короткую ссылку со своей группой).\n"
        f"Детали: {response.data}"
    )

    short_code = response.data.get("short", None)

    if short_code:
        return short_code, group_id

    raise KeyError("Короткий код ссылки отсутствует в ответе при её создании")


def count_colors_from_csv() -> int:
    csv_file = "colors.csv"
    path_to_csv = Path(settings.BASE_DIR).joinpath(f"resources/{csv_file}")

    assert path_to_csv.exists() is True, (f"Отсутствует файл {csv_file} "
                                          f"с цветами для тестирования")

    with open(path_to_csv, encoding="utf-8") as file:
        csv_reader = reader(file)
        total = 0

        for row in csv_reader:
            if not row:
                raise KeyError(
                    "Отсутствует первая строка. Скорее всего, файл пуст"
                )

            total += 1

        return total - 1
