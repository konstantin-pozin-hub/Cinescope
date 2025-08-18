import requests
from constants import BASE_URL, HEADERS, REGISTER_ENDPOINT, LOGIN_ENDPOINT, admin_data
import pytest
from utils.data_generator import DataGenerator


@pytest.fixture(scope="session")
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


@pytest.fixture(scope="session")
def auth_session(test_user):
    # Регистрируем нового пользователя
    register_url = f"{BASE_URL}{REGISTER_ENDPOINT}"
    response = requests.post(register_url, json=test_user, headers=HEADERS)
    assert response.status_code == 201, "Ошибка регистрации пользователя"

    # Логинимся для получения токена
    login_url = f"{BASE_URL}{LOGIN_ENDPOINT}"
    login_data = {
        "email": test_user["email"],
        "password": test_user["password"]
    }
    response = requests.post(login_url, json=login_data, headers=HEADERS)
    assert response.status_code == 200, "Ошибка авторизации"

    # Получаем токен и создаём сессию
    token = response.json().get("accessToken")
    assert token is not None, "Токен доступа отсутствует в ответе"

    session = requests.Session()
    session.headers.update(HEADERS)
    session.headers.update({"Authorization": f"Bearer {token}"})
    return session


@pytest.fixture(scope="session")
def admin_session():
    login_url = f"{BASE_URL}{LOGIN_ENDPOINT}"
    login_data = admin_data
    response = requests.post(login_url, json=login_data, headers=HEADERS)
    assert response.status_code == 200, "Ошибка авторизации"

    # Получаем токен и создаём сессию
    token = response.json().get("accessToken")
    assert token is not None, "Токен доступа отсутствует в ответе"

    session = requests.Session()
    session.headers.update(HEADERS)
    session.headers.update({"Authorization": f"Bearer {token}"})
    return session


@pytest.fixture
def test_user2():
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


@pytest.fixture(scope="session")
def test_user3():
    """
    Генерация случайного пользователя для тестов.
    """
    random_email = DataGenerator.generate_random_email()
    random_name = DataGenerator.generate_random_name()
    random_password = DataGenerator.generate_random_password()

    return {
        "email": "1234",
        "fullName": random_name,
        "password": random_password,
        "passwordRepeat": random_password,
        "roles": ["USER"]
    }


@pytest.fixture
def test_movie1():
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


@pytest.fixture(scope="session")
def test_movie2():
    return {
        "published": False
    }
