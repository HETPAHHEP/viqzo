from http import HTTPStatus


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
