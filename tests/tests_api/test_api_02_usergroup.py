from http import HTTPStatus

import pytest

from tests import utils


@pytest.mark.django_db(transaction=True)
class Test02UserGroup:
    """Тестирование API для взаимодействия с группой"""

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

    def test_03_01_edit_group_name(self, user_client, name_for_usergroup, new_name_for_usergroup):
        group_id = utils.create_usergroup(user_client, name_for_usergroup)

        response = user_client.patch(f'/api/groups/{group_id}/', data=new_name_for_usergroup)
        assert (response.status_code == HTTPStatus.OK
                and response.data.get('name') == new_name_for_usergroup.get('name')), (
            f'PATCH-запрос от авторизированного пользователя '
            f'на /api/groups/ для изменения имени группы с переданным полем имени и данными '
            f'не возвращает ответ со статусом 200 (имя группы нельзя поменять).'
        )

    def test_03_02_edit_group_name_without_new_name_field(self, user_client, name_for_usergroup):
        group_id = utils.create_usergroup(user_client, name_for_usergroup)

        response = user_client.patch(f'/api/groups/{group_id}/')
        assert (response.status_code == HTTPStatus.OK
                and response.data.get('name') == name_for_usergroup.get('name')), (
            f'PATCH-запрос от авторизированного пользователя '
            f'на /api/groups/ для изменения имени группы без переданного полем имени и данными '
            f'не возвращает ответ со статусом 200 (имя группы не должно поменяться).'
        )

    def test_03_03_edit_group_name_with_empty_new_name_field(
            self, user_client, name_for_usergroup, empty_name_for_usergroup
    ):
        group_id = utils.create_usergroup(user_client, name_for_usergroup)
        response = user_client.patch(f'/api/groups/{group_id}/', data=empty_name_for_usergroup)
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f'PATCH-запрос от авторизированного пользователя '
            f'на /api/groups/ для изменения имени группы c переданным пустым полем имени '
            f'не возвращает ответ со статусом 400 (для изменения имени группы необходимо передать не пустое имя).'
        )

    def test_03_04_edit_group_name_to_existing_group_name(
            self, user_client, name_for_usergroup, new_name_for_usergroup
    ):
        utils.create_usergroup(user_client, name_for_usergroup)
        group_id_2 = utils.create_usergroup(user_client, new_name_for_usergroup)

        response = user_client.patch(f'/api/groups/{group_id_2}/', data=name_for_usergroup)
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f'PATCH-запрос от авторизированного пользователя '
            f'на /api/groups/ для изменения имени группы c переданным полем имени, которое уже есть у другой группы, '
            f'не возвращает ответ со статусом 400 (имя каждой группы пользователя уникально).'
        )

    def test_03_05_edit_group_name_very_long_new_name(
            self, user_client, name_for_usergroup, very_long_name_for_usergroup
    ):
        group_id = utils.create_usergroup(user_client, name_for_usergroup)
        response = user_client.patch(f'/api/groups/{group_id}/', data=very_long_name_for_usergroup)
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f'PATCH-запрос от авторизированного пользователя '
            f'на /api/groups/ для изменения имени группы c переданным полем имени, которое превышает допустимую длину, '
            f'не возвращает ответ со статусом 400 (имя группы пользователя имеет ограничение по количеству символов).'
        )

    def test_04_01_get_group(self, user_client, name_for_usergroup):
        group_id = utils.create_usergroup(user_client, name_for_usergroup)

        response = user_client.get(f'/api/groups/{group_id}/')
        assert response.status_code == HTTPStatus.OK, (
            f'GET-запрос от авторизированного пользователя '
            f'на /api/groups/ для получении информации о группе '
            f'не возвращает ответ со статусом 200 (пользователь может получить данные своей группы).'
        )

    def test_04_02_get_group_with_other_owner(self, user_client, user_client2, name_for_usergroup):
        group_id = utils.create_usergroup(user_client2, name_for_usergroup)

        response = user_client.get(f'/api/groups/{group_id}/')
        assert response.status_code == HTTPStatus.NOT_FOUND, (
            f'GET-запрос от авторизированного пользователя '
            f'на /api/groups/group_id/ для получении информации о чужой группе '
            f'не возвращает ответ со статусом 404 '
            f'(пользователь не может получить данные чужой группы, она будет не найдена).'
        )

    def test_04_03_get_non_existent_group(self, user_client):
        response = user_client.get(f'/api/groups/666/')
        assert response.status_code == HTTPStatus.NOT_FOUND, (
            f'GET-запрос от авторизированного пользователя '
            f'на /api/groups/group_id/ для получении информации о несуществующей группе '
            f'не возвращает ответ со статусом 404 '
            f'(пользователь не может получить данные несуществующей группы).'
        )

    def test_04_04_get_all_user_groups(self, user_client, user_client2, name_for_usergroup):
        user_group_id = utils.create_usergroup(user_client, name_for_usergroup)
        other_group_id = utils.create_usergroup(user_client2, name_for_usergroup)

        response = user_client.get(f'/api/groups/')
        assert response.status_code == HTTPStatus.OK, (
            f'GET-запрос от авторизированного пользователя '
            f'на /api/groups/ для получении списка групп '
            f'не возвращает ответ со статусом 200 '
            f'(пользователь должен получить список своих групп).'
        )

        response = user_client.get(f'/api/groups/{other_group_id}/')

        assert response.status_code == HTTPStatus.NOT_FOUND
