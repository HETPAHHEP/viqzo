from http import HTTPStatus

import pytest

from tests import utils


@pytest.mark.django_db(transaction=True)
class Test00BasicShort:

    def test_01_01_create_short_url_not_auth(self, client, valid_original_link):
        response = client.post('/api/links/', data=valid_original_link)
        assert response.status_code == HTTPStatus.CREATED, (
            f'POST-запрос с валидной ссылкой от неавторизованного пользователя '
            f'на api/links/ для создания короткого кода не возвращает ответ '
            f'со статусом 201.'
        )

    def test_01_02_create_short_link_and_check_idempotency(self, client, valid_original_link):
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

    def test_01_03_create_short_link_with_invalid_original_link(self, client, invalid_original_link):
        response = client.post('/api/links/', data=invalid_original_link)
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f'POST-запрос с невалидной ссылкой от неавторизованного пользователя '
            f'на api/links/ для создания короткого кода должен возвращать ответ '
            f'со статусом 400 (короткая ссылка не создается).'
        )

    def test_01_04_create_short_link_len_restrict_for_original_link(self, client, very_long_link):
        response = client.post('/api/links/', data=very_long_link)
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f'POST-запрос c длинной ссылкой на api/links/ для создания короткого кода '
            f'должен возвращать ошибку со статусом 400 '
            f'(ограничение по длине ссылки).'
        )

    def test_01_05_create_short_link_without_original_link(self, client):
        response = client.post('/api/links/')
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f'POST-запрос без ссылки на api/links/ для создания короткого кода '
            f'должен возвращать ошибку со статусом 400 '
            f'(нужно добавить ссылку для сокращения).'
        )

    def test_02_01_get_original_link(self, client, valid_original_link):
        code = utils.create_short_link(client, valid_original_link)
        response = client.get(f'/api/links/{code}/')
        assert (
                response.status_code == HTTPStatus.OK and
                response.data.get('original_link') == valid_original_link.get('original_link')
        ), (
            f'GET-запрос с кодом на api/links/{code}/ для получения полной ссылки '
            f'не вернул нужную ссылку. '
        )

    def test_02_02_check_clicks_count(self, client, valid_original_link):
        code = utils.create_short_link(client, valid_original_link)
        response = client.get(f'/api/links/{code}/')
        assert (
                response.status_code == HTTPStatus.OK and
                response.data.get('original_link') == valid_original_link.get('original_link') and
                response.data.get('clicks_count') == 1
        ), (
            f'GET-запрос с кодом на api/links/{code}/ для получения полной ссылки '
            f'не вернул нужную ссылку с кликами на неё. '
        )

        clicked_at = response.data.get('last_clicked_at')

        response = client.get(f'/api/links/{code}/')
        assert (
                response.status_code == HTTPStatus.OK and
                response.data.get('original_link') == valid_original_link.get('original_link') and
                response.data.get('clicks_count') == 2 and
                response.data.get('last_clicked_at') != clicked_at
        ), (
            f'GET-запрос с кодом на api/links/{code}/ для получения полной ссылки '
            f'не посчитал повторно клики на нужную ссылку. '
        )
