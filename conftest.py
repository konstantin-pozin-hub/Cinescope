import random
import requests
import json
from pydantic import BaseModel
from PydanticExamples.work_with_pydantic import Roles, UserModel, BaseModel
from constants import BASE_URL, HEADERS, REGISTER_ENDPOINT, LOGIN_ENDPOINT, ADMIN_DATA
import pytest

from entities.user import User
from models.base_models import TestUser
from tests.test_api.api_manager import ApiManager
from tests.test_api.resources.user_creds import SuperAdminCreds
from utils.data_generator import DataGenerator
from faker import Faker
from custom_requester.custom_requester import CustomRequester
from enum import Enum
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
faker = Faker()


@pytest.fixture(scope="function")
def admin_api_manager(api_manager):
    response = api_manager.auth_api.login_user(ADMIN_DATA)
    response_data = response.json()
    token = f"Bearer {response_data.get('accessToken')}"
    api_manager.movie_api._update_session_headers(Authorization=token)
    return api_manager


@pytest.fixture(scope="session")
def session():
    """
    Фикстура для создания HTTP-сессии.
    """
    http_session = requests.Session()

    yield http_session
    http_session.close()


@pytest.fixture(scope="session")
def base_url():
    return "https://auth.dev-cinescope.coconutqa.ru/"


@pytest.fixture(scope="session")
def api_manager(session, base_url):
    """
    Фикстура для создания экземпляра ApiManager.
    """
    return ApiManager(session, base_url)


@pytest.fixture(scope="function")
def registered_user(api_manager, test_user):
    """
    Фикстура для регистрации и получения данных зарегистрированного пользователя.
    """
    response = api_manager.auth_api.register_user(test_user)
    response_data = response.json()
    registered_user = test_user.copy()
    registered_user["id"] = response_data["id"]
    return registered_user


# Фикстуры для тестов юзера
@pytest.fixture
def test_user_model() -> TestUser:
    random_password = DataGenerator.generate_random_password()
    random_name = DataGenerator.generate_random_name()
    random_email = DataGenerator.generate_random_email()

    return TestUser(
        email=random_email,
        fullName=random_name,
        password=random_password,
        passwordRepeat=random_password,
        roles=[Roles.USER.value]
    )


@pytest.fixture
def test_user(test_user_model):
    user_data = test_user_model.model_dump()
    return user_data


@pytest.fixture(scope="function")
def test_user_for_updata():
    return {
        "roles": [
            "USER"
        ],
        "verified": True,
        "banned": False
    }


@pytest.fixture(scope="function")
def test_user_with_wrong_email():
    """
    Генерация случайного пользователя для тестов.
    """
    random_name = DataGenerator.generate_random_name()
    random_password = DataGenerator.generate_random_password()

    return {
        "email": "1234",
        "fullName": random_name,
        "password": random_password,
        "passwordRepeat": random_password,
        "roles": ["USER"]
    }


# Фикстуры для тестов фильма
@pytest.fixture(scope="function")
def test_movie():
    """
    Генерация случайного пользователя для тестов.
    """

    random_name = DataGenerator.generate_random_name()

    return {
        "name": random_name,
        "imageUrl": "https://example.com/image.png",
        "price": 100,
        "description": "Описание фильма",
        "location": "SPB",
        "published": True,
        "genreId": 1
    }


@pytest.fixture(scope="function")
def test_movie_for_updata():
    return {
        "published": False
    }


@pytest.fixture(scope="function")
def test_movie_with_wrong_data():
    return {
        "name": "",
        "imageUrl": "https://example.com/image.png",
        "price": 100,
        "description": "Описание фильма",
        "location": "SPB",
        "published": True,
        "genreId": 1
    }


# Новое по 5 модулю
@pytest.fixture
def user_session():
    user_pool = []

    def _create_user_session():
        session = requests.Session()
        user_session = ApiManager(session, base_url)
        user_pool.append(user_session)
        return user_session

    yield _create_user_session

    for user in user_pool:
        user.close_session()


@pytest.fixture
def super_admin(user_session):
    new_session = user_session()

    super_admin = User(
        SuperAdminCreds.get_name(),
        SuperAdminCreds.get_password(),
        [Roles.SUPER_ADMIN.value],
        new_session)

    super_admin.api.auth_api.authenticate(super_admin.creds)
    return super_admin


@pytest.fixture(scope="function")
def creation_user_data(test_user):
    updated_data = test_user
    updated_data.update({
        "verified": True,
        "banned": False
    })
    return updated_data


@pytest.fixture(scope="function")
def creation_admin_data(test_user):
    updated_data = test_user
    updated_data.update({
        "email": ADMIN_DATA['email'],
        "password": ADMIN_DATA['password'],
        "verified": True,
        "banned": False
    })
    return updated_data


@pytest.fixture(scope="function")
def common_user(user_session, super_admin, creation_user_data):
    new_session = user_session()

    common_user = User(
        creation_user_data['email'],
        creation_user_data['password'],
        [Roles.USER.value],
        new_session)

    super_admin.api.user_api.create_user(creation_user_data)
    common_user.api.auth_api.authenticate(common_user.creds)
    return common_user


# SAM NAPISAL
@pytest.fixture(scope="function")
def admin(user_session, super_admin, creation_user_data):
    new_session = user_session()

    admin = User(
        creation_user_data['email'],
        creation_user_data['password'],
        [Roles.ADMIN.value],
        new_session)

    super_admin.api.user_api.create_user(creation_user_data)
    admin.api.auth_api.authenticate(admin.creds)
    return admin
