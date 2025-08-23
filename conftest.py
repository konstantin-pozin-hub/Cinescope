import random
import requests
from constants import BASE_URL, HEADERS, REGISTER_ENDPOINT, LOGIN_ENDPOINT, ADMIN_DATA
import pytest
from tests.test_api.api_manager import ApiManager
from utils.data_generator import DataGenerator
from faker import Faker
from custom_requester.custom_requester import CustomRequester

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
@pytest.fixture(scope="function")
def test_user():
    """
    Генерация случайного пользователя для тестов.
    """
    random_email = DataGenerator.generate_random_email()
    random_name = DataGenerator.generate_random_name()
    random_password = DataGenerator.generate_random_password()

    return {
        "email": random_email,
        "fullName": random_name,
        "password": random_password,
        "passwordRepeat": random_password,
        "roles": ["USER"]
    }


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
def test_user_generate():
    """
    Генерация случайного пользователя для тестов.
    """
    random_email = DataGenerator.generate_random_email()
    random_name = DataGenerator.generate_random_name()
    random_password = DataGenerator.generate_random_password()

    return {
        "fullName": random_name,
        "email": random_email,
        "password": random_password,
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
