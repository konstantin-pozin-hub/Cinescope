from models.base_models import RegisterUserResponse
from tests.test_api.api_manager import ApiManager


class TestAuthAPI:
    def test_register_user(self, api_manager: ApiManager, test_user):
        response = api_manager.auth_api.register_user(user_data=test_user)
        register_user_response = RegisterUserResponse(**response.json())
        assert register_user_response.email == test_user['email'], "Email не совпадает"

    def test_register_and_login_user(self, api_manager: ApiManager, registered_user):
        """
        Тест на регистрацию и авторизацию пользователя.
        """

        login_data = {
            "email": registered_user["email"],
            "password": registered_user["password"]
        }

        response = api_manager.auth_api.login_user(login_data)
        response_data = response.json()

        # Проверки
        assert "accessToken" in response_data, "Токен доступа отсутствует в ответе"
        assert response_data["user"]["email"] == registered_user["email"], "Email не совпадает"

    def test_wrong_register_user(self, api_manager: ApiManager, test_user_with_wrong_email):
        response = api_manager.auth_api.register_user(test_user_with_wrong_email, expected_status=400)
