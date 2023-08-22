import pytest
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token


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
def token_user_superuser(user_superuser):
    token = Token.objects.get_or_create(user=user_superuser)
    return {
        'access': str(token),
    }


@pytest.fixture
def user_superuser_client(token_user_superuser):
    client = APIClient()
    client.credentials(
        HTTP_AUTHORIZATION=f'Token {token_user_superuser["access"]}'
    )
    return client


@pytest.fixture
def token_user(user):
    token = Token.objects.create(user=user)
    return {
        'access': str(token),
    }


@pytest.fixture
def user_client(token_user):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token_user["access"]}')
    return client
