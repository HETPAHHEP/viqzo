from http import HTTPStatus

import pytest


@pytest.mark.django_db(transaction=True)
class Test00BasicShort:

    def test_01_01_create_short_url_not_auth(self, client, valid_original_link, invalid_original_link):
        response = client.post('/api/links/')
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f'POST-запрос без ссылки на api/links/ для создания короткого кода '
            f'должен возвращать ошибку со статусом 400 '
            f'(нужно добавить ссылку для сокращения).'
        )

        response = client.post('/api/links/', data=valid_original_link)
        assert response.status_code == HTTPStatus.CREATED, (
            f'POST-запрос с валидной ссылкой от неавторизованного пользователя '
            f'на api/links/ для создания короткого кода не возвращает ответ '
            f'со статусом 201.'
        )

        response = client.post('/api/links/', data=valid_original_link)
        assert response.status_code == HTTPStatus.OK, (
            f'POST-запрос с валидной ссылкой от неавторизованного пользователя '
            f'на api/links/ для создания короткого кода для уже созданной ссылки '
            f'не возвращает ответ со статусом 200.'
        )

        response = client.post('/api/links/', data=invalid_original_link)
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f'POST-запрос с невалидной ссылкой от неавторизованного пользователя '
            f'на api/links/ для создания короткого кода должен возвращать ответ '
            f'со статусом 400 (короткая ссылка не создается).'
        )
