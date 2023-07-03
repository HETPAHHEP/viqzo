from http import HTTPStatus


def create_short_link(client, valid_original_link):
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

