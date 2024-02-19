from http import HTTPStatus

import pytest
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


@pytest.fixture
def user_superuser(django_user_model):
    return django_user_model.objects.create_superuser(
        username='TestSuperuser',
        email='testsuperuser@viqzo.fake',
        password='123456789',
    )


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(
        username='TestUser',
        email='testuser@viqzo.fake',
        password='123456789',
    )


@pytest.fixture
def user2(django_user_model):
    return django_user_model.objects.create_user(
        username='TestUser2',
        email='testuser2@viqzo.fake',
        password='123456789',
    )


@pytest.fixture
def token_user_superuser(user_superuser):
    token = Token.objects.get_or_create(user=user_superuser)
    return {
        'access': str(token),
    }


@pytest.fixture
def user_superuser_client(token_user_superuser):
    client = APIClient()
    token = token_user_superuser["access"][9:49]
    client.credentials(
        HTTP_AUTHORIZATION=f'Token {token}'
    )

    # Проверка входа
    response = client.get('/api/groups/')
    assert response.status_code == HTTPStatus.OK

    return client


@pytest.fixture
def user_client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def user_client2(user2):
    client = APIClient()
    client.force_authenticate(user=user2)
    return client

#
# @pytest.fixture
# def token_user(user):
#     token = Token.objects.create(user=user)
#     return {
#         'access': str(token),
#     }
#
#
# @pytest.fixture
# def user_client(token_user):
#     client = APIClient()
#     client.credentials(
#         HTTP_AUTHORIZATION=f'Token {token_user["access"]}'
#     )
#
#     response = client.get('/api/groups/')
#     assert response.status_code == HTTPStatus.OK
#
#     return client
#
#
# @pytest.fixture
# def token_user2(user2):
#     token = Token.objects.create(user=user2)
#     return {
#         'access': str(token),
#     }
#
#
# @pytest.fixture
# def user_client2(token_user2):
#     client = APIClient()
#     client.credentials(
#         HTTP_AUTHORIZATION=f'Token {token_user2["access"]}'
#     )
#
#     response = client.get('/api/groups/')
#     assert response.status_code == HTTPStatus.OK
#
#     return client
