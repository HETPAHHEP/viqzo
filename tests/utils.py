from http import HTTPStatus


def create_short_link(client, valid_original_link) -> str:
    """Создание обычной короткой ссылки.

    :returns code: Код для созданной короткой ссылки
    """

    response = client.post('/api/links/', data=valid_original_link)
    assert response.status_code == HTTPStatus.CREATED, (
        f'POST-запрос с валидной ссылкой от неавторизованного пользователя '
        f'на api/links/ для создания короткого кода не возвращает ответ '
        f'со статусом 201.'
    )

    code = response.data.get('short')
    if code:
        return code

    raise KeyError('Короткий код для ссылки отсутствует при создании')


def create_alias_link(client, original_link_with_alias) -> str:
    """Создание пользовательской короткой ссылки.

    :returns code: Выбранное имя для созданной короткой ссылки
    """

    response = client.post('/api/links/', data=original_link_with_alias)
    assert response.status_code == HTTPStatus.CREATED, (
        f'POST-запрос с валидной ссылкой и alias от неавторизованного пользователя '
        f'на api/links/ для создания пользовательского кода не возвращает ответ со статусом 201.'
    )

    code = response.data.get('short')
    if code:
        return code

    raise KeyError('Пользовательский код для ссылки отсутствует при создании')


def create_short_link_and_return_id_in_dict(client, valid_original_link) -> dict:
    """Создание обычной короткой ссылки.

    :returns code: ID созданной короткой ссылки
    """

    response = client.post('/api/links/', data=valid_original_link)
    assert response.status_code == HTTPStatus.CREATED, (
        f'POST-запрос с валидной ссылкой от пользователя '
        f'на api/links/ для создания короткого кода не возвращает ответ '
        f'со статусом 201.'
    )

    link_id = response.data.get('id')
    if link_id:
        return {
            'short_link': link_id
        }

    raise KeyError('ID короткой ссылки отсутствует после создания в ответе.')


def create_alias_link_and_return_id_in_dict(client, original_link_with_alias) -> dict:
    """Создание пользовательской короткой ссылки.

    :returns code: ID созданной короткой ссылки
    """

    response = client.post('/api/links/', data=original_link_with_alias)
    assert response.status_code == HTTPStatus.CREATED, (
        f'POST-запрос с валидной ссылкой и alias от пользователя '
        f'на api/links/ для создания пользовательского кода не возвращает ответ со статусом 201.'
    )

    link_id = response.data.get('id')
    if link_id:
        return {
            'alias_link': link_id
        }

    raise KeyError('ID пользовательской ссылки отсутствует после создания в ответе.')


def create_usergroup(client, name_for_usergroup) -> int:
    """Создание группы для пользовательских ссылок.

    :returns group_id: Id созданной группы
    """

    response = client.post('/api/groups/', data=name_for_usergroup)

    assert response.status_code == HTTPStatus.CREATED, (
        f'POST-запрос с именем от пользователя '
        f'на api/groups/ для создания группы не возвращает ответ '
        f'со статусом 201.'
    )

    group_id = response.data.get('id')

    if group_id:
        return group_id

    raise KeyError('Id группы отсутствует в ответе при её создании')


def create_and_add_short_link_to_group(client, original_link, group_id) -> int:
    """Создание и добавление ссылки в группу"""

    short_link = create_short_link_and_return_id_in_dict(client, original_link)
    response = client.post(f'/api/groups/{group_id}/add-link/', data=short_link)

    assert response.status_code == HTTPStatus.CREATED, (
        f'POST-запрос от авторизованного пользователя '
        f'на api/groups/group_id/add-link/ для добавления ссылки в групп не возвращает ответ '
        f'со статусом 201.'
    )

    short_link_id = short_link.get('short_link')

    if short_link_id:
        return short_link_id

    raise KeyError('Id группы отсутствует в ответе при её создании')


def create_and_add_alias_link_to_group(client, original_link_alias, group_id) -> int:
    """Создание и добавление ссылки в группу"""

    alias_link = create_alias_link_and_return_id_in_dict(client, original_link_alias)
    response = client.post(f'/api/groups/{group_id}/add-link/', data=alias_link)

    assert response.status_code == HTTPStatus.CREATED, (
        f'POST-запрос от авторизованного пользователя '
        f'на api/groups/group_id/add-link/ для добавления ссылки в групп не возвращает ответ '
        f'со статусом 201.'
    )

    alias_link_id = alias_link.get('alias_link')

    if alias_link_id:
        return alias_link_id

    raise KeyError('Id группы отсутствует в ответе при её создании')


def create_usergroup_with_short_link(client, name_for_usergroup, valid_original_link) -> tuple[int, dict]:
    """Создание группы для пользовательских ссылок вместе ссылкой.

    :returns (group_id, {'short_link': short_link_id}): Id созданной группы, ID ссылки
    """

    response = client.post('/api/groups/', data=name_for_usergroup)

    assert response.status_code == HTTPStatus.CREATED, (
        f'POST-запрос с именем от пользователя '
        f'на api/groups/ для создания группы не возвращает ответ '
        f'со статусом 201.'
    )

    group_id = response.data.get('id')

    if group_id:
        short_link_id = create_and_add_short_link_to_group(client, valid_original_link, group_id)
        short_link = {
            'short_link': short_link_id
        }

        return group_id, short_link

    raise KeyError('Id группы отсутствует в ответе при её создании')


def create_usergroup_with_alias_link(client, name_for_usergroup, original_link_with_alias) -> tuple[int, dict]:
    """Создание группы для пользовательских ссылок вместе ссылкой.

    :returns (group_id, {'alias_link': alias_link_id}): Id созданной группы, ID ссылки
    """

    response = client.post('/api/groups/', data=name_for_usergroup)

    assert response.status_code == HTTPStatus.CREATED, (
        f'POST-запрос с именем от пользователя '
        f'на api/groups/ для создания группы не возвращает ответ '
        f'со статусом 201.'
    )

    group_id = response.data.get('id')

    if group_id:
        alias_link_id = create_and_add_alias_link_to_group(client, original_link_with_alias, group_id)
        alias_link = {
            'alias_link': alias_link_id
        }

        return group_id, alias_link

    raise KeyError('Id группы отсутствует в ответе при её создании')
