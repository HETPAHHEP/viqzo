from http import HTTPStatus

import pytest

from tests import utils


@pytest.mark.django_db(transaction=True)
class Test02ShortLinksWithGroup:
    """Тестирование API для проверки связанности коротких ссылок и групп"""

    def test_01_01_create_and_add_short_link_to_group(
        self, user_client, name_for_usergroup, valid_original_link
    ):
        group_id = utils.create_usergroup(user_client, name_for_usergroup)
        utils.add_created_group_to_dict_with_link(
            valid_original_link, group_id
        )

        response = user_client.post("/api/links/", data=valid_original_link)

        assert (
            response.status_code == HTTPStatus.CREATED
            and response.data["group"]["id"] == group_id
        ), (
            "POST-запрос от авторизованного пользователя "
            "на /api/links/ для создания short ссылки с группой "
            "не возвращает ответ со статусом 201 "
            "(пользователь должен иметь возможность создать короткую ссылку со своей группой)."
        )

    def test_01_02_create_and_add_alias_link_to_group(
        self, user_client, name_for_usergroup, original_link_with_alias
    ):
        group_id = utils.create_usergroup(user_client, name_for_usergroup)
        utils.add_created_group_to_dict_with_link(
            original_link_with_alias, group_id
        )

        response = user_client.post(
            "/api/links/", data=original_link_with_alias
        )
        assert (
            response.status_code == HTTPStatus.CREATED
            and response.data["group"]["id"] == group_id
        ), (
            "POST-запрос от авторизованного пользователя "
            "на /api/links/ для создания alias ссылки с группой "
            "не возвращает ответ со статусом 201 "
            "(пользователь должен иметь возможность создать короткую alias ссылку с группой)."
        )

    def test_01_03_create_and_add_links_to_not_own_group(
        self,
        user_client,
        user_client2,
        name_for_usergroup,
        valid_original_link,
        original_link_with_alias,
    ):
        group_id = utils.create_usergroup(user_client2, name_for_usergroup)
        utils.add_created_group_to_dict_with_link(
            valid_original_link, group_id
        )

        response = user_client.post("/api/links/", data=valid_original_link)

        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            "POST-запрос от авторизованного пользователя "
            "на /api/links/ для создания short ссылки с чужой группой "
            "не возвращает ответ со статусом 400 (нельзя добавить ссылку в чужую группу)."
        )

        utils.add_created_group_to_dict_with_link(
            original_link_with_alias, group_id
        )

        response = user_client.post(
            "/api/links/", data=original_link_with_alias
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            "POST-запрос от авторизованного пользователя "
            "на /api/links/ для создания alias ссылки с чужой группой "
            "не возвращает ответ со статусом 400 (нельзя добавить ссылку в чужую группу)."
        )

    def test_01_04_create_and_add_links_to_group_twice(
        self,
        user_client,
        name_for_usergroup,
        valid_original_link,
        original_link_with_alias,
        original_link_with_other_alias,
    ):
        group_id = utils.create_usergroup(user_client, name_for_usergroup)
        utils.add_created_group_to_dict_with_link(
            valid_original_link, group_id
        )

        response = user_client.post("/api/links/", data=valid_original_link)

        assert (
            response.status_code == HTTPStatus.CREATED
            and response.data["group"]["id"] == group_id
        ), (
            "POST-запрос от авторизованного пользователя "
            "на /api/links/ для создания short ссылки и добавления её в свою группу "
            "не возвращает ответ со статусом 201 (пользователь может добавить ссылку в свою группу)."
        )

        response = user_client.post("/api/links/", data=valid_original_link)

        assert (
            response.status_code == HTTPStatus.CREATED
            and response.data["group"]["id"] == group_id
        ), (
            "POST-запрос от авторизованного пользователя "
            "на /api/links/ для создания short ссылки и добавления в свою группу ещё раз "
            "не возвращает ответ со статусом 201 (пользователь может добавить вторую ссылку в свою группу)."
        )

        utils.add_created_group_to_dict_with_link(
            original_link_with_alias, group_id
        )

        response = user_client.post(
            "/api/links/", data=original_link_with_alias
        )

        assert (
            response.status_code == HTTPStatus.CREATED
            and response.data["group"]["id"] == group_id
        ), (
            "POST-запрос от авторизованного пользователя "
            "на /api/links/ для создания alias ссылки и добавления её в свою группу "
            "не возвращает ответ со статусом 201 (пользователь может добавить ссылку в свою группу)."
        )

        response = user_client.post(
            "/api/links/", data=original_link_with_alias
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            "POST-запрос от авторизованного пользователя "
            "на /api/links/ для создания alias ссылки и добавления в свою группу ещё раз "
            "не возвращает ответ со статусом 400 "
            "(нельзя создать ссылку с одинаковым алиасом и добавить её в группу)."
        )

        utils.add_created_group_to_dict_with_link(
            original_link_with_other_alias, group_id
        )

        response = user_client.post(
            "/api/links/", data=original_link_with_other_alias
        )

        assert (
            response.status_code == HTTPStatus.CREATED
            and response.data["group"]["id"] == group_id
        ), (
            "POST-запрос от авторизованного пользователя "
            "на /api/links/ для создания alias ссылки и добавления её в свою группу "
            "не возвращает ответ со статусом 201 (пользователь может добавить ссылку в свою группу)."
        )

    def test_02_01_edit_group_at_short_link(
        self,
        user_client,
        valid_original_link,
        name_for_usergroup,
        new_name_for_usergroup,
    ):
        link_short_code, group_id = utils.create_and_add_short_link_to_group(
            user_client, valid_original_link, name_for_usergroup
        )

        new_group_id = utils.create_usergroup(
            user_client, new_name_for_usergroup
        )

        response = user_client.patch(
            f"/api/links/{link_short_code}/",
            data=utils.add_created_group_to_dict(new_group_id),
        )

        assert (
            response.status_code == HTTPStatus.OK
            and response.data["group"]["id"] == new_group_id
        ), (
            "PATCH-запрос от авторизованного пользователя "
            "на /api/links/ для изменения short ссылки с добавлением её в свою новую группу "
            "не возвращает ответ со статусом 200 (пользователь может поменять у ссылки свою группу)."
        )

    def test_02_02_edit_group_at_alias_link(
        self,
        user_client,
        original_link_with_alias,
        name_for_usergroup,
        new_name_for_usergroup,
    ):
        link_short_code, group_id = utils.create_and_add_short_link_to_group(
            user_client, original_link_with_alias, name_for_usergroup
        )

        new_group_id = utils.create_usergroup(
            user_client, new_name_for_usergroup
        )

        response = user_client.patch(
            f"/api/links/{link_short_code}/",
            data=utils.add_created_group_to_dict(new_group_id),
        )

        assert (
            response.status_code == HTTPStatus.OK
            and response.data["group"]["id"] == new_group_id
        ), (
            "PATCH-запрос от авторизованного пользователя "
            "на /api/links/ для изменения alias ссылки с добавлением её в свою новую группу "
            "не возвращает ответ со статусом 200 (пользователь может поменять у ссылки свою группу)."
        )

    def test_02_03_edit_non_existent_group_at_link(
        self,
        user_client,
        valid_original_link,
        original_link_with_alias,
        name_for_usergroup,
        new_name_for_usergroup,
    ):
        link_short_code, group_id = utils.create_and_add_short_link_to_group(
            user_client, valid_original_link, name_for_usergroup
        )

        response = user_client.patch(
            f"/api/links/{link_short_code}/",
            data=utils.add_created_group_to_dict(666),
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            "PATCH-запрос от авторизованного пользователя "
            "на /api/links/ для изменения short ссылки с добавлением её в несуществующую группу "
            "не возвращает ответ со статусом 400 "
            "(пользователь не может поменять у ссылки свою группу на несуществующую)."
        )

        link_short_code, group_id = utils.create_and_add_short_link_to_group(
            user_client, original_link_with_alias, new_name_for_usergroup
        )

        response = user_client.patch(
            f"/api/links/{link_short_code}/",
            data=utils.add_created_group_to_dict(666),
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            "PATCH-запрос от авторизованного пользователя "
            "на /api/links/ для изменения alias ссылки с добавлением её в несуществующую группу "
            "не возвращает ответ со статусом 400 "
            "(пользователь не может поменять у ссылки свою группу на несуществующую)."
        )

    def test_02_04_edit_group_at_link_with_same_id(
        self,
        user_client,
        original_link_with_alias,
        name_for_usergroup,
        valid_original_link,
        new_name_for_usergroup,
    ):
        link_short_code, group_id = utils.create_and_add_short_link_to_group(
            user_client, original_link_with_alias, name_for_usergroup
        )

        response = user_client.patch(
            f"/api/links/{link_short_code}/",
            data=utils.add_created_group_to_dict(group_id),
        )

        assert (
            response.status_code == HTTPStatus.OK
            and response.data["group"]["id"] == group_id
        ), (
            "PATCH-запрос от авторизованного пользователя "
            "на /api/links/ для изменения alias ссылки c такой же группой "
            "не возвращает ответ со статусом 200 (пользователь может передать такую же группу для изменения)."
        )

        link_short_code, group_id = utils.create_and_add_short_link_to_group(
            user_client, valid_original_link, new_name_for_usergroup
        )

        response = user_client.patch(
            f"/api/links/{link_short_code}/",
            data=utils.add_created_group_to_dict(group_id),
        )

        assert (
            response.status_code == HTTPStatus.OK
            and response.data["group"]["id"] == group_id
        ), (
            "PATCH-запрос от авторизованного пользователя "
            "на /api/links/ для изменения short ссылки c такой же группой "
            "не возвращает ответ со статусом 200 (пользователь может передать такую же группу для изменения)."
        )

    def test_02_05_edit_not_own_group_at_link(
        self,
        user_client,
        user_client2,
        valid_original_link,
        original_link_with_alias,
        name_for_usergroup,
        new_name_for_usergroup,
    ):
        other_group_id = utils.create_usergroup(
            user_client2, name_for_usergroup
        )

        link_short_code, group_id = utils.create_and_add_short_link_to_group(
            user_client, valid_original_link, name_for_usergroup
        )

        response = user_client.patch(
            f"/api/links/{link_short_code}/",
            data=utils.add_created_group_to_dict(other_group_id),
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            "PATCH-запрос от авторизованного пользователя "
            "на /api/links/ для изменения short ссылки с добавлением её в чужую группу "
            "не возвращает ответ со статусом 400 "
            "(пользователь не может поменять у ссылки группу на чужую)."
        )

        link_short_code, group_id = utils.create_and_add_short_link_to_group(
            user_client, original_link_with_alias, new_name_for_usergroup
        )

        response = user_client.patch(
            f"/api/links/{link_short_code}/",
            data=utils.add_created_group_to_dict(other_group_id),
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            "PATCH-запрос от авторизованного пользователя "
            "на /api/links/ для изменения alias ссылки с добавлением её в чужую группу "
            "не возвращает ответ со статусом 400 "
            "(пользователь не может поменять у ссылки свою группу на чужую)."
        )

    def test_02_06_try_edit_not_own_link(
        self,
        user_client,
        user_client2,
        valid_original_link,
        original_link_with_alias,
        name_for_usergroup,
        new_name_for_usergroup,
    ):
        link_short_code, group_id = utils.create_and_add_short_link_to_group(
            user_client, valid_original_link, name_for_usergroup
        )

        response = user_client2.patch(
            f"/api/links/{link_short_code}/",
            data=utils.add_created_group_to_dict(group_id),
        )

        assert response.status_code == HTTPStatus.NOT_FOUND, (
            "PATCH-запрос от авторизованного пользователя "
            "на /api/links/ для изменения чужой short ссылки с добавлением её в группу "
            "не возвращает ответ со статусом 404 "
            "(пользователь не может поменять чужую ссылку)."
        )

        link_short_code, group_id = utils.create_and_add_short_link_to_group(
            user_client, original_link_with_alias, new_name_for_usergroup
        )

        response = user_client2.patch(
            f"/api/links/{link_short_code}/",
            data=utils.add_created_group_to_dict(group_id),
        )

        assert response.status_code == HTTPStatus.NOT_FOUND, (
            "PATCH-запрос от авторизованного пользователя "
            "на /api/links/ для изменения чужой alias ссылки с добавлением её в группу "
            "не возвращает ответ со статусом 404 "
            "(пользователь не может поменять чужую ссылку)."
        )

    def test_02_06_edit__link_with_char_group_field(
        self,
        user_client,
        valid_original_link,
        original_link_with_alias,
        name_for_usergroup,
        new_name_for_usergroup,
    ):
        link_short_code, group_id = utils.create_and_add_short_link_to_group(
            user_client, valid_original_link, name_for_usergroup
        )

        response = user_client.patch(
            f"/api/links/{link_short_code}/",
            data=utils.add_created_group_to_dict("First"),
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            "PATCH-запрос от авторизованного пользователя "
            "на /api/links/ для изменения short ссылки с передачей неправильного ID группы "
            "не возвращает ответ со статусом 400 "
            "(пользователь может поменять только на существующую группу)."
        )

        link_short_code, group_id = utils.create_and_add_short_link_to_group(
            user_client, original_link_with_alias, new_name_for_usergroup
        )

        response = user_client.patch(
            f"/api/links/{link_short_code}/",
            data=utils.add_created_group_to_dict("Second"),
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            "PATCH-запрос от авторизованного пользователя "
            "на /api/links/ для изменения short ссылки с передачей неправильного ID группы "
            "не возвращает ответ со статусом 400 "
            "(пользователь может поменять только на существующую группу)."
        )

    def test_03_01_filter_links_by_group(
        self,
        user_client,
        name_for_usergroup,
        new_name_for_usergroup,
        valid_original_link,
        original_link_with_alias,
    ):
        link_short_code_1, group_id_1 = (
            utils.create_and_add_short_link_to_group(
                user_client, valid_original_link, name_for_usergroup
            )
        )

        link_short_code_2, group_id_2 = (
            utils.create_and_add_short_link_to_group(
                user_client, original_link_with_alias, new_name_for_usergroup
            )
        )

        response = user_client.get(f"/api/links/?group_id={group_id_1}")

        assert (
            response.status_code == HTTPStatus.OK
            and response.data["count"] == 1
            and response.data["results"][0]["short"] == link_short_code_1
            and response.data["results"][0]["group"]["id"] == group_id_1
        ), (
            "GET-запрос от авторизованного пользователя "
            "на /api/links/?group_id=group_id для фильтрации ссылок по группе "
            "не возвращает ответ со статусом 200 "
            "(пользователь может фильтровать ссылке по группам)."
        )

        response = user_client.get(f"/api/links/?group_id={group_id_2}")

        assert (
            response.status_code == HTTPStatus.OK
            and response.data["count"] == 1
            and response.data["results"][0]["short"] == link_short_code_2
            and response.data["results"][0]["group"]["id"] == group_id_2
        ), (
            "GET-запрос от авторизованного пользователя "
            "на /api/links/?group_id=group_id для фильтрации ссылок по группе "
            "не возвращает ответ со статусом 200 "
            "(пользователь может фильтровать ссылке по группам)."
        )

    def test_03_02_filter_links_by_non_existent_group(
        self,
        user_client,
        name_for_usergroup,
        new_name_for_usergroup,
        valid_original_link,
        original_link_with_alias,
    ):
        utils.create_and_add_short_link_to_group(
            user_client, valid_original_link, name_for_usergroup
        )

        utils.create_and_add_short_link_to_group(
            user_client, original_link_with_alias, new_name_for_usergroup
        )

        response = user_client.get(f"/api/links/?group_id={666}")

        assert (
            response.status_code == HTTPStatus.OK
            and response.data["count"] == 0
        ), (
            "GET-запрос от авторизованного пользователя "
            "на /api/links/?group_id=group_id для фильтрации ссылок по несуществующей группе "
            "не возвращает ответ со статусом 200 и количеством записей 0 "
            "(пользователь может фильтровать ссылке по группам)."
        )

        response = user_client.get(f"/api/links/?group_id={777}")

        assert (
            response.status_code == HTTPStatus.OK
            and response.data["count"] == 0
        ), (
            "GET-запрос от авторизованного пользователя "
            "на /api/links/?group_id=group_id для фильтрации ссылок по несуществующей группе "
            "не возвращает ответ со статусом 200 и количеством записей 0 "
            "(пользователь может фильтровать ссылке по группам)."
        )

    def test_03_03_filter_not_own_links_by_group(
        self,
        user_client,
        name_for_usergroup,
        new_name_for_usergroup,
        valid_original_link,
        original_link_with_alias,
        user_client2,
    ):
        link_short_code_1, group_id_1 = (
            utils.create_and_add_short_link_to_group(
                user_client, valid_original_link, name_for_usergroup
            )
        )

        link_short_code_2, group_id_2 = (
            utils.create_and_add_short_link_to_group(
                user_client, original_link_with_alias, new_name_for_usergroup
            )
        )

        response = user_client2.get(f"/api/links/?group_id={group_id_1}")

        assert (
            response.status_code == HTTPStatus.OK
            and response.data["count"] == 0
        ), (
            "GET-запрос от авторизованного пользователя "
            "на /api/links/?group_id=group_id для фильтрации ссылок по несуществующей группе "
            "не возвращает ответ со статусом 200 и количеством записей 0 "
            "(пользователь может фильтровать ссылке по группам)."
        )

        response = user_client2.get(f"/api/links/?group_id={group_id_2}")

        assert (
            response.status_code == HTTPStatus.OK
            and response.data["count"] == 0
        ), (
            "GET-запрос от авторизованного пользователя "
            "на /api/links/?group_id=group_id для фильтрации ссылок по несуществующей группе "
            "не возвращает ответ со статусом 200 и количеством записей 0 "
            "(пользователь может фильтровать ссылке по группам)."
        )
