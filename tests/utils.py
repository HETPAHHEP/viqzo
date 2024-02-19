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


def create_usergroup(client, name_for_usergroup) -> int:
    """Создание группы для пользовательских ссылок.

    :returns group_id: Id созданной группы
    """

    response = client.post('/api/groups/', data=name_for_usergroup)
    print(response.data)

    assert response.status_code == HTTPStatus.CREATED, (
        f'POST-запрос с именем от пользователя '
        f'на api/groups/ для создания группы не возвращает ответ '
        f'со статусом 201.'
    )

    group_id = response.data.get('id')

    if group_id:
        return group_id

    raise KeyError('Id группы отсутствует в ответе при её создании')
