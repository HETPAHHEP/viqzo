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

    code = response.data.get('short_url')
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

    code = response.data.get('short_url')
    if code:
        return code

    raise KeyError('пользовательского код для ссылки отсутствует при создании')


def create_usergroup(client, name_for_usergroup):
    """Создание группы для пользовательских ссылок.

    """

    response = client.post('/api/groups/', data=name_for_usergroup)
    assert response

