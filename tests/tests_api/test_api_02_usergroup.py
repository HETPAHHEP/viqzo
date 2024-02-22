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

    def test_02_02_create_usergroup_and_check_idempotency(self, user_client, user_client2, name_for_usergroup):
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

        utils.create_usergroup(user_client2, name_for_usergroup)

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

    def test_04_01_get_group_not_auth(self, user_client, client, name_for_usergroup):
        response = client.get(f'/api/groups/1/')
        assert response.status_code == HTTPStatus.UNAUTHORIZED, (
            f'GET-запрос от не авторизированного пользователя '
            f'на /api/groups/ для получении информации о группе '
            f'не возвращает ответ со статусом 401 '
            f'(не авторизованный пользователь не может получить данные любой группы).'
        )

        group_id = utils.create_usergroup(user_client, name_for_usergroup)

        response = client.get(f'/api/groups/{group_id}/')
        assert response.status_code == HTTPStatus.UNAUTHORIZED, (
            f'GET-запрос от авторизированного пользователя '
            f'на /api/groups/ для получении информации о чужой группе '
            f'не возвращает ответ со статусом 401 '
            f'(не авторизованный пользователь не может получить данные любой группы).'
        )

    def test_04_02_get_group_auth(self, user_client, name_for_usergroup):
        group_id = utils.create_usergroup(user_client, name_for_usergroup)

        response = user_client.get(f'/api/groups/{group_id}/')
        assert response.status_code == HTTPStatus.OK, (
            f'GET-запрос от авторизированного пользователя '
            f'на /api/groups/ для получении информации о группе '
            f'не возвращает ответ со статусом 200 (пользователь может получить данные своей группы).'
        )

    def test_04_03_get_group_with_other_owner(self, user_client, user_client2, name_for_usergroup):
        group_id = utils.create_usergroup(user_client2, name_for_usergroup)

        response = user_client.get(f'/api/groups/{group_id}/')
        assert response.status_code == HTTPStatus.NOT_FOUND, (
            f'GET-запрос от авторизированного пользователя '
            f'на /api/groups/group_id/ для получении информации о чужой группе '
            f'не возвращает ответ со статусом 404 '
            f'(пользователь не может получить данные чужой группы, она будет не найдена).'
        )

    def test_04_04_get_non_existent_group(self, user_client):
        response = user_client.get(f'/api/groups/666/')
        assert response.status_code == HTTPStatus.NOT_FOUND, (
            f'GET-запрос от авторизированного пользователя '
            f'на /api/groups/group_id/ для получении информации о несуществующей группе '
            f'не возвращает ответ со статусом 404 '
            f'(пользователь не может получить данные несуществующей группы).'
        )

    def test_05_01_get_all_user_groups_not_auth(self, client):
        response = client.get(f'/api/groups/')
        assert response.status_code == HTTPStatus.UNAUTHORIZED, (
            f'GET-запрос от не авторизированного пользователя '
            f'на /api/groups/ для получении списка групп '
            f'не возвращает ответ со статусом 401 '
            f'(пользователь должен получить список своих групп).'
        )

    def test_05_02_get_all_user_groups(self, user_client, name_for_usergroup):
        utils.create_usergroup(user_client, name_for_usergroup)

        response = user_client.get(f'/api/groups/')
        assert (response.data
                and response.status_code == HTTPStatus.OK), (
            f'GET-запрос от авторизированного пользователя '
            f'на /api/groups/ для получении списка групп '
            f'не возвращает ответ со статусом 200 '
            f'(пользователь должен получить список своих групп).'
        )

    def test_05_03_get_and_check_only_all_user_groups(self, user_client, user_client2, name_for_usergroup):
        utils.create_usergroup(user_client, name_for_usergroup)
        utils.create_usergroup(user_client2, name_for_usergroup)

        response = user_client.get(f'/api/groups/')
        assert response.status_code == HTTPStatus.OK, (
            f'GET-запрос от авторизированного пользователя '
            f'на /api/groups/ для получении списка групп '
            f'не возвращает ответ со статусом 200 '
            f'(пользователь должен получить только список своих групп).'
        )

        assert response.data and len(response.data) == 1, (
            f'GET-запрос от авторизированного пользователя '
            f'на /api/groups/ для получении списка групп '
            f'не дал правильный список групп пользователя '
            f'(пользователь должен получить только список своих групп).'
        )

    def test_06_01_create_and_add_short_link_to_group(self, user_client, name_for_usergroup, valid_original_link):
        group_id = utils.create_usergroup(user_client, name_for_usergroup)
        link_with_group = valid_original_link.update(
            {
                'group': group_id
            }
        )

        response = user_client.post(f'/api/links/', data=link_with_group)
        assert (response.status_code == HTTPStatus.CREATED
                and response.group == group_id), (
            f'POST-запрос от авторизованного пользователя '
            f'на /api/groups/group_id/add-link/ для добавления short ссылки в группу '
            f'не возвращает ответ со статусом 201 '
            f'(пользователь должен иметь возможность добавить короткую ссылку в группу).'
        )

    def test_06_02_add_alias_link_to_group(self, user_client, name_for_usergroup, original_link_with_alias):
        group_id = utils.create_usergroup(user_client, name_for_usergroup)
        link = utils.create_alias_link_and_return_id_in_dict(user_client, original_link_with_alias)

        response = user_client.post(f'/api/groups/{group_id}/add-link/', data=link)
        assert response.status_code == HTTPStatus.CREATED, (
            f'POST-запрос от авторизованного пользователя '
            f'на /api/groups/group_id/add-link/ для добавления alias ссылки в группу '
            f'не возвращает ответ со статусом 201 '
            f'(пользователь должен иметь возможность добавить короткую ссылку в группу).'
        )

    def test_06_03_add_alias_and_short_links_to_group(
            self, user_client, name_for_usergroup, valid_original_link, original_link_with_alias
    ):
        group_id = utils.create_usergroup(user_client, name_for_usergroup)
        short_link = utils.create_short_link_and_return_id_in_dict(user_client, valid_original_link)
        alias_link = utils.create_alias_link_and_return_id_in_dict(user_client, original_link_with_alias)

        links = short_link.update(alias_link)

        response = user_client.post(f'/api/groups/{group_id}/add-link/', data=links)
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f'POST-запрос от авторизованного пользователя '
            f'на /api/groups/group_id/add-link/ при добавлении alias и short ссылок в группу '
            f'не возвращает ответ со статусом 400 '
            f'(пользователь должен может добавить только одну ссылку одного типа за раз в группу).'
        )

    def test_06_04_add_non_existent_links_to_group(self, user_client, name_for_usergroup):
        group_id = utils.create_usergroup(user_client, name_for_usergroup)

        response = user_client.post(
            f'/api/groups/{group_id}/add-link/',
            data={
                'short_link': 1
            }
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f'POST-запрос от авторизованного пользователя '
            f'на /api/groups/group_id/add-link/ для добавления несуществующей short ссылки в группу '
            f'не возвращает ответ со статусом 400 (нельзя добавить несуществующую ссылку в группу).'
        )

        response = user_client.post(
            f'/api/groups/{group_id}/add-link/',
            data={
                'alias_link': 1
            }
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f'POST-запрос от авторизованного пользователя '
            f'на /api/groups/group_id/add-link/ для добавления несуществующей alias ссылки в группу '
            f'не возвращает ответ со статусом 400 (нельзя добавить несуществующую ссылку в группу).'
        )

    def test_06_04_add_not_own_links_to_group(
            self, user_client, user_client2, name_for_usergroup, valid_original_link, original_link_with_alias
    ):
        group_id = utils.create_usergroup(user_client, name_for_usergroup)
        short_link = utils.create_short_link_and_return_id_in_dict(user_client2, valid_original_link)
        alias_link = utils.create_alias_link_and_return_id_in_dict(user_client2, original_link_with_alias)

        response = user_client.post(f'/api/groups/{group_id}/add-link/', data=short_link)

        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f'POST-запрос от авторизованного пользователя '
            f'на /api/groups/group_id/add-link/ для добавления чужой short ссылки в группу '
            f'не возвращает ответ со статусом 400 (нельзя добавить чужую ссылку в группу).'
        )

        response = user_client.post(f'/api/groups/{group_id}/add-link/', data=alias_link)

        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f'POST-запрос от авторизованного пользователя '
            f'на /api/groups/group_id/add-link/ для добавления чужой alias ссылки в группу '
            f'не возвращает ответ со статусом 400 (нельзя добавить чужую ссылку в группу).'
        )

    def test_06_05_add_links_to_not_own_group(
            self, user_client, user_client2, name_for_usergroup, valid_original_link, original_link_with_alias
    ):
        group_id = utils.create_usergroup(user_client2, name_for_usergroup)
        short_link = utils.create_short_link_and_return_id_in_dict(user_client, valid_original_link)
        alias_link = utils.create_alias_link_and_return_id_in_dict(user_client, original_link_with_alias)

        response = user_client.post(f'/api/groups/{group_id}/add-link/', data=short_link)

        assert response.status_code == HTTPStatus.NOT_FOUND, (
            f'POST-запрос от авторизованного пользователя '
            f'на /api/groups/group_id/add-link/ для добавления short ссылки в чужую группу '
            f'не возвращает ответ со статусом 400 (нельзя добавить ссылку в чужую группу).'
        )

        response = user_client.post(f'/api/groups/{group_id}/add-link/', data=alias_link)

        assert response.status_code == HTTPStatus.NOT_FOUND, (
            f'POST-запрос от авторизованного пользователя '
            f'на /api/groups/group_id/add-link/ для добавления alias ссылки в чужую группу '
            f'не возвращает ответ со статусом 400 (нельзя добавить ссылку в чужую группу).'
        )

    def test_06_06_add_link_twice(
            self, user_client, name_for_usergroup, valid_original_link, original_link_with_alias
    ):
        group_id = utils.create_usergroup(user_client, name_for_usergroup)
        short_link = utils.create_short_link_and_return_id_in_dict(user_client, valid_original_link)

        response = user_client.post(f'/api/groups/{group_id}/add-link/', data=short_link)

        assert response.status_code == HTTPStatus.CREATED, (
            f'POST-запрос от авторизованного пользователя '
            f'на /api/groups/group_id/add-link/ для добавления short ссылки в свою группу '
            f'не возвращает ответ со статусом 201 (пользователь может добавить ссылку в свою группу).'
        )

        response = user_client.post(f'/api/groups/{group_id}/add-link/', data=short_link)

        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f'POST-запрос от авторизованного пользователя '
            f'на /api/groups/group_id/add-link/ для добавления short ссылки в группу ещё раз'
            f'не возвращает ответ со статусом 400 (нельзя добавить ссылку дважды в группу).'
        )

        alias_link = utils.create_alias_link_and_return_id_in_dict(user_client, original_link_with_alias)

        response = user_client.post(f'/api/groups/{group_id}/add-link/', data=alias_link)

        assert response.status_code == HTTPStatus.CREATED, (
            f'POST-запрос от авторизованного пользователя '
            f'на /api/groups/group_id/add-link/ для добавления alias ссылки в свою группу '
            f'не возвращает ответ со статусом 201 (пользователь может добавить ссылку в свою группу).'
        )

        response = user_client.post(f'/api/groups/{group_id}/add-link/', data=alias_link)

        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f'POST-запрос от авторизованного пользователя '
            f'на /api/groups/group_id/add-link/ для добавления alias ссылки в группу ещё раз'
            f'не возвращает ответ со статусом 400 (нельзя добавить ссылку дважды в группу).'
        )

    def test_07_01_remove_short_link_from_group(
            self, user_client, name_for_usergroup, valid_original_link,
    ):
        group_id, short_link = utils.create_usergroup_with_short_link(
            user_client, name_for_usergroup, valid_original_link
        )

        response = user_client.delete(f'/api/groups/{group_id}/remove-link/', data=short_link)

        assert response.status_code == HTTPStatus.NO_CONTENT, (
            f'POST-запрос от авторизованного пользователя '
            f'на /api/groups/group_id/add-link/ для удаления short ссылки из своей группы '
            f'не возвращает ответ со статусом 204 (пользователь может удалить ссылку из своей группы).'
        )

    def test_07_02_remove_alias_link_from_group(
            self, user_client, name_for_usergroup, original_link_with_alias
    ):
        group_id, alias_link = utils.create_usergroup_with_alias_link(
            user_client, name_for_usergroup, original_link_with_alias
        )

        response = user_client.delete(f'/api/groups/{group_id}/remove-link/', data=alias_link)

        assert response.status_code == HTTPStatus.NO_CONTENT, (
            f'POST-запрос от авторизованного пользователя '
            f'на /api/groups/group_id/add-link/ для удаления alias ссылки из своей группы '
            f'не возвращает ответ со статусом 204 (пользователь может удалить ссылку из своей группы).'
        )

    def test_07_03_remove_short_link_from_group_twice(
            self, user_client, name_for_usergroup, valid_original_link,
    ):
        group_id, short_link = utils.create_usergroup_with_short_link(
            user_client, name_for_usergroup, valid_original_link
        )

        response = user_client.delete(f'/api/groups/{group_id}/remove-link/', data=short_link)

        assert response.status_code == HTTPStatus.NO_CONTENT, (
            f'POST-запрос от авторизованного пользователя '
            f'на /api/groups/group_id/add-link/ для удаления short ссылки из своей группы '
            f'не возвращает ответ со статусом 204 (пользователь может удалить ссылку из своей группы).'
        )

        response = user_client.delete(f'/api/groups/{group_id}/remove-link/', data=short_link)

        assert response.status_code == HTTPStatus.NOT_FOUND, (
            f'POST-запрос от авторизованного пользователя '
            f'на /api/groups/group_id/add-link/ для удаления short ссылки из своей группы '
            f'не возвращает ответ со статусом 400 (ссылка уже была удалена).'
        )

    def test_07_03_remove_alias_link_from_group_twice(
            self, user_client, name_for_usergroup, original_link_with_alias,
    ):
        group_id, alias_link = utils.create_usergroup_with_alias_link(
            user_client, name_for_usergroup, original_link_with_alias
        )

        response = user_client.delete(f'/api/groups/{group_id}/remove-link/', data=alias_link)

        assert response.status_code == HTTPStatus.NO_CONTENT, (
            f'POST-запрос от авторизованного пользователя '
            f'на /api/groups/group_id/add-link/ для удаления short ссылки из своей группы '
            f'не возвращает ответ со статусом 204 (пользователь может удалить ссылку из своей группы).'
        )

        response = user_client.delete(f'/api/groups/{group_id}/remove-link/', data=alias_link)

        assert response.status_code == HTTPStatus.NOT_FOUND, (
            f'POST-запрос от авторизованного пользователя '
            f'на /api/groups/group_id/add-link/ для удаления short ссылки из своей группы '
            f'не возвращает ответ со статусом 400 (ссылка уже была удалена).'
        )

    def test_07_04_remove_not_own_short_link(
            self, user_client, user_client2,
            name_for_usergroup, original_link_with_alias, valid_original_link,
            new_name_for_usergroup
    ):
        group_id, short_link = utils.create_usergroup_with_short_link(
            user_client, name_for_usergroup, valid_original_link
        )

        response = user_client2.delete(f'/api/groups/{group_id}/remove-link/', data=short_link)

        assert response.status_code == HTTPStatus.NOT_FOUND, (
            f'POST-запрос от авторизованного пользователя '
            f'на /api/groups/group_id/add-link/ для удаления short ссылки из чужой группы '
            f'не возвращает ответ со статусом 404 (нельзя удалить чужую ссылку из чужой группы).'
        )

        group_id, alias_link = utils.create_usergroup_with_alias_link(
            user_client, new_name_for_usergroup, original_link_with_alias
        )

        response = user_client2.delete(f'/api/groups/{group_id}/remove-link/', data=alias_link)

        assert response.status_code == HTTPStatus.NOT_FOUND, (
            f'POST-запрос от авторизованного пользователя '
            f'на /api/groups/group_id/add-link/ для удаления alias ссылки из чужой группы '
            f'не возвращает ответ со статусом 404 (нельзя удалить чужую ссылку из чужой группы).'
        )

    def test_08_01_delete_group(self, user_client, name_for_usergroup):
        group_id = utils.create_usergroup(user_client, name_for_usergroup)

        response = user_client.delete(f'/api/groups/{group_id}/')

        assert response.status_code == HTTPStatus.NO_CONTENT, (
            f'POST-запрос от авторизованного пользователя '
            f'на /api/groups/group_id/ для удаления группы '
            f'не возвращает ответ со статусом 204 (пользователь может удалить свою группу).'
        )

    def test_08_02_delete_not_own_group(self, user_client, user_client2, name_for_usergroup):
        group_id = utils.create_usergroup(user_client, name_for_usergroup)

        response = user_client2.delete(f'/api/groups/{group_id}/')

        assert response.status_code == HTTPStatus.NOT_FOUND, (
            f'POST-запрос от авторизованного пользователя '
            f'на /api/groups/group_id/ для удаления чужой группы '
            f'не возвращает ответ со статусом 404 (пользователь не может удалить чужую группу).'
        )
