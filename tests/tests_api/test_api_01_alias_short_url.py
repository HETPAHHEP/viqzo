from http import HTTPStatus

import pytest

from tests import utils


@pytest.mark.django_db(transaction=True)
class Test01AliasShort:

    def test_01_01_create_alias_url_not_auth(self, client, original_link_with_alias):
        response = client.post('/api/links/', data=original_link_with_alias)
        assert response.status_code == HTTPStatus.CREATED, (
            f'POST-запрос с валидной ссылкой и alias от неавторизованного пользователя '
            f'на api/links/ для создания пользовательского кода не возвращает ответ со статусом 201.'
        )

    def test_01_02_create_alias_link_and_check_idempotency(self, client, original_link_with_alias):
        response = client.post('/api/links/', data=original_link_with_alias)
        assert response.status_code == HTTPStatus.CREATED, (
            f'POST-запрос с валидной ссылкой и alias от неавторизованного пользователя '
            f'на api/links/ для создания пользовательского кода не возвращает ответ со статусом 201.'
        )

        response = client.post('/api/links/', data=original_link_with_alias)
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f'POST-запрос с валидной ссылкой и alias от неавторизованного пользователя '
            f'на api/links/ для создания пользовательского кода для уже созданной ссылки '
            f'возвращает ответ со статусом 400 (не дает создать новую ссылку с данным кодом).'
        )

        response = client.post('/api/links/', data=original_link_with_alias)
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f'POST-запрос с валидной ссылкой и alias от неавторизованного пользователя '
            f'на api/links/ для создания пользовательского кода для уже созданной ссылки '
            f'возвращает ответ со статусом 400 (не дает создать новую ссылку с данным кодом).'
        )

    def test_01_03_create_alias_link_with_invalid_original_link(self, client, invalid_original_link):
        response = client.post('/api/links/', data=invalid_original_link)
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f'POST-запрос с невалидной ссылкой и alias от неавторизованного пользователя '
            f'на api/links/ для создания пользовательского кода должен возвращать ответ '
            f'со статусом 400 (короткая ссылка не создается).'
        )

    def test_01_04_create_alias_link_len_restrict_for_original_link(self, client, very_long_link_with_alias):
        response = client.post('/api/links/', data=very_long_link_with_alias)
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f'POST-запрос c длинной ссылкой на api/links/ для создания пользовательского кода '
            f'должен возвращать ошибку со статусом 400 (ограничение по длине ссылки).'
        )

    def test_01_04_create_link_with_short_alias(self, client, very_short_alias):
        response = client.post('/api/links/', data=very_short_alias)
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f'POST-запрос c коротким alias на api/links/ для создания пользовательского кода '
            f'должен возвращать ошибку со статусом 400 (ограничение по длине кода).'
        )

    def test_01_04_create_link_with_long_alias(self, client, very_long_alias):
        response = client.post('/api/links/', data=very_long_alias)
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f'POST-запрос c длинным alias на api/links/ для создания пользовательского кода '
            f'должен возвращать ошибку со статусом 400 (ограничение по длине кода).'
        )

    def test_01_05_create_alias_link_without_original_link(self, client):
        response = client.post('/api/links/')
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f'POST-запрос без ссылки на api/links/ для создания пользовательского кода '
            f'должен возвращать ошибку со статусом 400 (нужно добавить ссылку для сокращения).'
        )

    def test_02_01_get_original_link_by_alias(self, client, original_link_with_alias):
        code = utils.create_alias_link(client, original_link_with_alias)
        response = client.get(f'/api/links/{code}/')
        assert (
                response.status_code == HTTPStatus.OK and
                response.data.get('original_link') == original_link_with_alias.get('original_link') and
                response.data.get('short_url') == original_link_with_alias.get('alias')
        ), (
            f'GET-запрос с кодом на api/links/{code}/ для получения полной ссылки '
            f'не вернул нужную ссылку. '
        )

    def test_02_02_check_clicks_count_alias_link(self, client, original_link_with_alias):
        code = utils.create_alias_link(client, original_link_with_alias)
        response = client.get(f'/api/links/{code}/')
        assert (
                response.status_code == HTTPStatus.OK and
                response.data.get('original_link') == original_link_with_alias.get('original_link') and
                response.data.get('short_url') == original_link_with_alias.get('alias') and
                response.data.get('clicks_count') == 1
        ), (
            f'GET-запрос с кодом на api/links/{code}/ для получения полной ссылки '
            f'не вернул нужную ссылку с кликами на неё. '
        )

        clicked_at = response.data.get('last_clicked_at')

        response = client.get(f'/api/links/{code}/')
        assert (
                response.status_code == HTTPStatus.OK and
                response.data.get('original_link') == original_link_with_alias.get('original_link') and
                response.data.get('short_url') == original_link_with_alias.get('alias') and
                response.data.get('clicks_count') == 2 and
                response.data.get('last_clicked_at') != clicked_at
        ), (
            f'GET-запрос с кодом на api/links/{code}/ для получения полной ссылки '
            f'не посчитал повторно клики на нужную ссылку. '
        )
