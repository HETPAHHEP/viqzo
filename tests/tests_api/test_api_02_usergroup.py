from http import HTTPStatus

import pytest

from tests import utils


@pytest.mark.django_db(transaction=True)
class Test02UserGroup:

    def test_01_01_create_usergroup_not_auth(self, client, name_for_usergroup):
        response = client.post('/api/groups/', data=name_for_usergroup)
        assert response.status_code == HTTPStatus.UNAUTHORIZED, (
            f'POST-запрос от неавторизованного пользователя '
            f'на /api/groups/ для создания группы ссылок не возвращает ответ со статусом 401 '
            f'(запрет на создание группы, если не авторизованы).'
        )

    def test_02_01_create_usergroup_auth(self, user_client, name_for_usergroup):
        response = user_client.post('/api/groups/', data=name_for_usergroup)
        assert (
            response.status_code == HTTPStatus.CREATED and
            response.data.get('name') == name_for_usergroup.get('name')
        ), (
            f'POST-запрос от авторизованного пользователя '
            f'на /api/groups/ для создания группы ссылок не возвращает ответ со статусом 201 '
            f'(группа успешно создана).'
        )

    def test_02_02_create_usergroup_and_check_idempotency(self, user_client, name_for_usergroup):
        response = user_client.post('/api/groups/', data=name_for_usergroup)
        assert response.status_code == HTTPStatus.CREATED, (
            f'POST-запрос от авторизованного пользователя '
            f'на /api/groups/ для создания группы ссылок не возвращает ответ со статусом 201 '
            f'(группа успешно создана).'
        )

        response = user_client.post('/api/groups/', data=name_for_usergroup)
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f'POST-запрос от авторизованного пользователя '
            f'на /api/groups/ для создания группы ссылок не возвращает ответ со статусом 400 '
            f'(группа с таким именем у данного пользователя уже существует).'
        )

        response = user_client.post('/api/groups/', data=name_for_usergroup)
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f'POST-запрос от авторизованного пользователя '
            f'на /api/groups/ для создания группы ссылок не возвращает ответ со статусом 400 '
            f'(группа с таким именем у данного пользователя уже существует).'
        )

    def test_02_03_create_usergroup_len_restrict_for_name(self, user_client, very_long_name_for_usergroup):
        response = user_client.post('/api/groups/', data=very_long_name_for_usergroup)
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f'POST-запрос от авторизованного пользователя '
            f'на /api/groups/ для создания группы ссылок с очень длинным именем не возвращает ответ со статусом 400 '
            f'(нельзя создать группы с именем, которое длиннее установленного лимита).'
        )

    def test_02_04_create_usergroup_short_name(self, user_client, very_short_name_for_usergroup):
        response = user_client.post('/api/groups/', data=very_short_name_for_usergroup)
        assert response.status_code == HTTPStatus.CREATED, (
            f'POST-запрос от авторизованного пользователя '
            f'на /api/groups/ для создания группы ссылок с очень коротким именем не возвращает ответ со статусом 201 '
            f'(можно создать группу с именем).'
        )

    def test_02_05_create_usergroup_empty_name(self, user_client, empty_name_for_usergroup):
        response = user_client.post('/api/groups/', data=empty_name_for_usergroup)
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f'POST-запрос от авторизованного пользователя '
            f'на /api/groups/ для создания группы ссылок с пустым именем не возвращает ответ со статусом 400 '
            f'(нельзя создать группу без имени).'
        )

    def test_02_05_create_usergroup_without_name(self, user_client):
        response = user_client.post('/api/groups/')
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f'POST-запрос от авторизованного пользователя '
            f'на /api/groups/ для создания группы ссылок без поля с именем не возвращает ответ со статусом 400 '
            f'(нельзя создать группу без имени).'
        )
