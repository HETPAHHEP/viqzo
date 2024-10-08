from http import HTTPStatus

import pytest

from tests import utils


@pytest.mark.django_db(transaction=True)
class Test01AliasShort:
    """Тестирование API пользовательских ссылок (с алиасом)"""

    def test_01_01_create_alias_url_not_auth(
        self, client, original_link_with_alias
    ):
        response = client.post("/api/links/", data=original_link_with_alias)
        assert response.status_code == HTTPStatus.CREATED, (
            f"POST-запрос с валидной ссылкой и alias от неавторизованного пользователя "
            f"на api/links/ для создания пользовательского кода не возвращает ответ со статусом 201.\n"
            f"Детали: {response.data}"
        )

    def test_01_02_create_alias_link_and_check_idempotency(
        self, client, original_link_with_alias
    ):
        response = client.post("/api/links/", data=original_link_with_alias)
        assert response.status_code == HTTPStatus.CREATED, (
            f"POST-запрос с валидной ссылкой и alias от неавторизованного пользователя "
            f"на api/links/ для создания пользовательского кода не возвращает ответ со статусом 201.\n"
            f"Детали: {response.data}"
        )

        response = client.post("/api/links/", data=original_link_with_alias)
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f"POST-запрос с валидной ссылкой и alias от неавторизованного пользователя "
            f"на api/links/ для создания пользовательского кода для уже созданной ссылки "
            f"возвращает ответ со статусом 400 (не дает создать новую ссылку с данным кодом).\n"
            f"Детали: {response.data}"
        )

        response = client.post("/api/links/", data=original_link_with_alias)
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f"POST-запрос с валидной ссылкой и alias от неавторизованного пользователя "
            f"на api/links/ для создания пользовательского кода для уже созданной ссылки "
            f"возвращает ответ со статусом 400 (не дает создать новую ссылку с данным кодом).\n"
            f"Детали: {response.data}"
        )

    def test_01_03_create_alias_link_with_invalid_original_link(
        self, client, invalid_original_link
    ):
        response = client.post("/api/links/", data=invalid_original_link)
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f"POST-запрос с невалидной ссылкой и alias от неавторизованного пользователя "
            f"на api/links/ для создания пользовательского кода должен возвращать ответ "
            f"со статусом 400 (короткая ссылка не создается).\n"
            f"Детали: {response.data}"
        )

    def test_01_04_create_alias_link_len_restrict_for_original_link(
        self, client, very_long_link_with_alias
    ):
        response = client.post("/api/links/", data=very_long_link_with_alias)
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f"POST-запрос c длинной ссылкой на api/links/ для создания пользовательского кода "
            f"должен возвращать ошибку со статусом 400 (ограничение по длине ссылки).\n"
            f"Детали: {response.data}"
        )

    def test_01_04_create_link_with_short_alias(
        self, client, very_short_alias
    ):
        response = client.post("/api/links/", data=very_short_alias)
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f"POST-запрос c коротким alias на api/links/ для создания пользовательского кода "
            f"должен возвращать ошибку со статусом 400 (ограничение по длине кода).\n"
            f"Детали: {response.data}"
        )

    def test_01_04_create_link_with_long_alias(self, client, very_long_alias):
        response = client.post("/api/links/", data=very_long_alias)
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f"POST-запрос c длинным alias на api/links/ для создания пользовательского кода "
            f"должен возвращать ошибку со статусом 400 (ограничение по длине кода).\n"
            f"Детали: {response.data}"
        )

    def test_01_05_create_alias_link_without_original_link(self, client):
        response = client.post("/api/links/")
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f"POST-запрос без ссылки на api/links/ для создания пользовательского кода "
            f"должен возвращать ошибку со статусом 400 (нужно добавить ссылку для сокращения).\n"
            f"Детали: {response.data}"
        )

    def test_02_01_get_original_link_by_alias(
        self, client, original_link_with_alias
    ):
        code = utils.create_alias_link(client, original_link_with_alias)
        response = client.get(f"/api/links/{code}/")
        assert (
            response.status_code == HTTPStatus.OK
            and response.data.get("original_link")
            == original_link_with_alias.get("original_link")
            and response.data.get("short")
            == original_link_with_alias.get("alias")
        ), (
            f"GET-запрос с кодом на api/links/{code}/ для получения полной ссылки "
            f"не вернул нужную ссылку.\n"
            f"Детали: {response.data}"
        )

    def test_02_02_check_clicks_count_alias_link(
        self, client, original_link_with_alias
    ):
        code = utils.create_alias_link(client, original_link_with_alias)
        response = client.get(f"/api/links/{code}/")
        assert (
            response.status_code == HTTPStatus.OK
            and response.data.get("original_link")
            == original_link_with_alias.get("original_link")
            and response.data.get("short")
            == original_link_with_alias.get("alias")
            and response.data.get("clicks_count") == 1
        ), (
            f"GET-запрос с кодом на api/links/{code}/ для получения полной ссылки "
            f"не вернул нужную ссылку с кликами на неё.\n"
            f"Детали: {response.data}"
        )

        clicked_at = response.data.get("last_clicked_at")

        response = client.get(f"/api/links/{code}/")
        assert (
            response.status_code == HTTPStatus.OK
            and response.data.get("original_link")
            == original_link_with_alias.get("original_link")
            and response.data.get("short")
            == original_link_with_alias.get("alias")
            and response.data.get("clicks_count") == 2
            and response.data.get("last_clicked_at") != clicked_at
        ), (
            f"GET-запрос с кодом на api/links/{code}/ для получения полной ссылки "
            f"не посчитал повторно клики на нужную ссылку.\n"
            f"Детали: {response.data}"
        )

    def test_03_01_create_alias_url_auth(
        self, user_client, original_link_with_alias
    ):
        response = user_client.post(
            "/api/links/", data=original_link_with_alias
        )

        assert response.status_code == HTTPStatus.CREATED, (
            f"POST-запрос с валидной ссылкой от авторизованного пользователя "
            f"на api/links/ для создания короткого кода не возвращает ответ со статусом 201.\n"
            f"Детали: {response.data}"
        )

    def test_04_01_edit_alias_link_active_status_true_after_create(
        self,
        user_client,
        original_link_with_alias,
        is_active_status_true_str_capital,
        is_active_status_true_bool,
        is_active_status_true_num,
        is_active_status_true_str_lowercase,
    ):
        short_code = utils.create_short_link(
            user_client, original_link_with_alias
        )

        response = user_client.patch(
            f"/api/links/{short_code}/", data=is_active_status_true_bool
        )

        assert response.status_code == HTTPStatus.OK and response.data[
            "is_active"
        ] == is_active_status_true_bool.get("is_active"), (
            f"PATCH-запрос от авторизованного пользователя "
            f"на /api/links/ для изменения статуса alias ссылки "
            f"не возвращает ответ со статусом 200 (пользователь может изменить статус).\n"
            f"Детали: {response.data}"
        )

        response = user_client.patch(
            f"/api/links/{short_code}/", data=is_active_status_true_num
        )

        assert response.status_code == HTTPStatus.OK and response.data[
            "is_active"
        ] == is_active_status_true_num.get("is_active"), (
            f"PATCH-запрос от авторизованного пользователя "
            f"на /api/links/ для изменения статуса alias ссылки "
            f"не возвращает ответ со статусом 200 (пользователь может изменить статус).\n"
            f"Детали: {response.data}"
        )

        response = user_client.patch(
            f"/api/links/{short_code}/", data=is_active_status_true_str_capital
        )

        assert (
            response.status_code == HTTPStatus.OK
            and type(response.data["is_active"]) == bool
            and response.data["is_active"]
        ), (
            f"PATCH-запрос от авторизованного пользователя "
            f"на /api/links/ для изменения статуса alias ссылки "
            f"не возвращает ответ со статусом 200 (пользователь может изменить статус).\n"
            f"Детали: {response.data}"
        )

        response = user_client.patch(
            f"/api/links/{short_code}/",
            data=is_active_status_true_str_lowercase,
        )

        assert (
            response.status_code == HTTPStatus.OK
            and type(response.data["is_active"]) == bool
            and response.data["is_active"]
        ), (
            f"PATCH-запрос от авторизованного пользователя "
            f"на /api/links/ для изменения статуса alias ссылки "
            f"не возвращает ответ со статусом 200 (пользователь может изменить статус).\n"
            f"Детали: {response.data}"
        )

    def test_04_02_edit_alias_link_active_status_false_after_create(
        self,
        user_client,
        original_link_with_alias,
        is_active_status_false_str_capital,
        is_active_status_false_bool,
        is_active_status_false_num,
        is_active_status_false_str_lowercase,
    ):
        short_code = utils.create_short_link(
            user_client, original_link_with_alias
        )

        response = user_client.patch(
            f"/api/links/{short_code}/", data=is_active_status_false_bool
        )

        assert (
            response.status_code == HTTPStatus.OK
            and type(response.data["is_active"]) == bool
            and not response.data["is_active"]
        ), (
            f"PATCH-запрос от авторизованного пользователя "
            f"на /api/links/ для изменения статуса alias ссылки "
            f"не возвращает ответ со статусом 200 (пользователь может изменить статус).\n"
            f"Детали: {response.data}"
        )

        response = user_client.patch(
            f"/api/links/{short_code}/", data=is_active_status_false_num
        )

        assert (
            response.status_code == HTTPStatus.OK
            and type(response.data["is_active"]) == bool
            and not response.data["is_active"]
        ), (
            f"PATCH-запрос от авторизованного пользователя "
            f"на /api/links/ для изменения статуса alias ссылки "
            f"не возвращает ответ со статусом 200 (пользователь может изменить статус).\n"
            f"Детали: {response.data}"
        )

        response = user_client.patch(
            f"/api/links/{short_code}/",
            data=is_active_status_false_str_capital,
        )

        assert (
            response.status_code == HTTPStatus.OK
            and type(response.data["is_active"]) == bool
            and not response.data["is_active"]
        ), (
            f"PATCH-запрос от авторизованного пользователя "
            f"на /api/links/ для изменения статуса alias ссылки "
            f"не возвращает ответ со статусом 200 (пользователь может изменить статус).\n"
            f"Детали: {response.data}"
        )

        response = user_client.patch(
            f"/api/links/{short_code}/",
            data=is_active_status_false_str_lowercase,
        )

        assert (
            response.status_code == HTTPStatus.OK
            and type(response.data["is_active"]) == bool
            and not response.data["is_active"]
        ), (
            f"PATCH-запрос от авторизованного пользователя "
            f"на /api/links/ для изменения статуса alias ссылки "
            f"не возвращает ответ со статусом 200 (пользователь может изменить статус).\n"
            f"Детали: {response.data}"
        )

    def test_04_03_edit_alias_link_active_status_with_false_status(
        self,
        user_client,
        original_link_with_alias,
        is_active_status_false_bool,
        is_active_status_true_bool,
    ):
        short_code = utils.create_short_link(
            user_client, original_link_with_alias
        )

        response = user_client.patch(
            f"/api/links/{short_code}/", data=is_active_status_false_bool
        )

        assert (
            response.status_code == HTTPStatus.OK
            and type(response.data["is_active"]) == bool
            and not response.data["is_active"]
        ), (
            f"PATCH-запрос от авторизованного пользователя "
            f"на /api/links/ для изменения статуса alias ссылки "
            f"не возвращает ответ со статусом 200 (пользователь может изменить статус).\n"
            f"Детали: {response.data}"
        )

        response = user_client.patch(
            f"/api/links/{short_code}/", data=is_active_status_false_bool
        )

        assert (
            response.status_code == HTTPStatus.OK
            and type(response.data["is_active"]) == bool
            and not response.data["is_active"]
        ), (
            f"PATCH-запрос от авторизованного пользователя "
            f"на /api/links/ для изменения статуса alias ссылки "
            f"не возвращает ответ со статусом 200 (пользователь может изменить статус).\n"
            f"Детали: {response.data}"
        )

        response = user_client.patch(
            f"/api/links/{short_code}/", data=is_active_status_true_bool
        )

        assert (
            response.status_code == HTTPStatus.OK
            and type(response.data["is_active"]) == bool
            and response.data["is_active"]
        ), (
            f"PATCH-запрос от авторизованного пользователя "
            f"на /api/links/ для изменения статуса alias ссылки "
            f"не возвращает ответ со статусом 200 (пользователь может изменить статус).\n"
            f"Детали: {response.data}"
        )

    def test_04_04_edit_not_own_alias_link_active_status(
        self,
        user_client,
        user_client2,
        original_link_with_alias,
        is_active_status_false_bool,
        is_active_status_true_bool,
    ):
        short_code = utils.create_short_link(
            user_client, original_link_with_alias
        )

        response = user_client2.patch(
            f"/api/links/{short_code}/", data=is_active_status_false_bool
        )

        assert response.status_code == HTTPStatus.NOT_FOUND, (
            f"PATCH-запрос от авторизованного пользователя "
            f"на /api/links/ для изменения статуса чужой alias ссылки "
            f"не возвращает ответ со статусом 404 (пользователь не может изменить статус чужой ссылки).\n"
            f"Детали: {response.data}"
        )

        response = user_client2.patch(
            f"/api/links/{short_code}/", data=is_active_status_true_bool
        )

        assert response.status_code == HTTPStatus.NOT_FOUND, (
            f"PATCH-запрос от авторизованного пользователя "
            f"на /api/links/ для изменения статуса чужой alias ссылки "
            f"не возвращает ответ со статусом 404 (пользователь не может изменить статус чужой ссылки).\n"
            f"Детали: {response.data}"
        )

        response = user_client.patch(
            f"/api/links/{short_code}/", data=is_active_status_false_bool
        )

        assert response.status_code == HTTPStatus.OK, (
            f"PATCH-запрос от авторизованного пользователя "
            f"на /api/links/ для изменения статуса alias ссылки "
            f"не возвращает ответ со статусом 200 (пользователь не может изменить статус чужой ссылки).\n"
            f"Детали: {response.data}"
        )

        response = user_client2.patch(
            f"/api/links/{short_code}/", data=is_active_status_true_bool
        )

        assert response.status_code == HTTPStatus.NOT_FOUND, (
            f"PATCH-запрос от авторизованного пользователя "
            f"на /api/links/ для изменения статуса чужой alias ссылки "
            f"не возвращает ответ со статусом 404 (пользователь не может изменить статус чужой ссылки).\n"
            f"Детали: {response.data}"
        )

    def test_04_05_check_show_alias_link_after_change_status(
        self,
        user_client,
        original_link_with_alias,
        is_active_status_false_bool,
    ):
        short_code = utils.create_short_link(
            user_client, original_link_with_alias
        )

        response = user_client.patch(
            f"/api/links/{short_code}/", data=is_active_status_false_bool
        )

        assert response.status_code == HTTPStatus.OK and response.data[
            "is_active"
        ] == is_active_status_false_bool.get("is_active"), (
            f"PATCH-запрос от авторизованного пользователя "
            f"на /api/links/ для изменения статуса alias ссылки "
            f"не возвращает ответ со статусом 200 (пользователь может изменить статус).\n"
            f"Детали: {response.data}"
        )

        response = user_client.get(f"/api/links/{short_code}/")

        assert response.status_code == HTTPStatus.NOT_FOUND, (
            f"GET-запрос от авторизованного пользователя "
            f"на /api/links/short_code для получения полной ссылки после изменения статуса на False "
            f"не возвращает ответ со статусом 404 (пользователь может отключить выдачу полной ссылки).\n"
            f"Детали: {response.data}"
        )
