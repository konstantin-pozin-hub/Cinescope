import pytest


@pytest.mark.parametrize("param_a,param_b", [
    ("a1", "b1"),
    ("a2", "b2")
])
class TestMultipleParams:

    def test_params_combination(self, param_a, param_b):
        print(f"1 тест: {param_a} и {param_b}")

    def test_another_method(self, param_a, param_b):
        combined = f"{param_a}-{param_b}"
        print(f"2 тест: {combined}")
        assert len(combined) > 2


@pytest.mark.parametrize("class_param", ["c1", "c2"])
class TestCombinedParametrization:

    @pytest.mark.parametrize("method_param", ["m1", "m2", "m3"])
    def test_combination(self, class_param, method_param):
        # Этот тест запустится 6 раз (2 параметра класса × 3 параметра метода)
        print(f"Тест 1 с параметризацией класса={class_param} и метода={method_param}")
        assert True

    def test_only_class_param(self, class_param):
        # Этот тест запустится 2 раза (только с параметрами класса)
        print(f"Тест 2 с параметризацией только класса={class_param}")
        assert True


@pytest.mark.parametrize("feature_flag,platform", [
    ("feature_a", "windows"),
    ("feature_a", "mac"),
    ("feature_b", "windows"),
    pytest.param("feature_b", "mac", marks=pytest.mark.skip(reason="Not supported on Mac"))
])
class TestFeatures:

    def test_feature_availability(self, feature_flag, platform):
        print(f"Testing {feature_flag} on {platform}")
        assert True


import pytest
from resources.user_creds import SuperAdminCreds


@pytest.mark.parametrize("email, password, expected_status", [
    (f"{SuperAdminCreds.USERNAME}", f"{SuperAdminCreds.PASSWORD}", (200, 201)),
    ("test_login1@email.com", "asdqwe123Q!", 500),  # Сервис не может обработать логин по незареганному юзеру
    ("", "password", 500),
], ids=["Admin login", "Invalid user", "Empty username"])
def test_login(email, password, expected_status, api_manager):
    login_data = {
        "email": email,
        "password": password
    }
    api_manager.auth_api.login_user(login_data=login_data, expected_status=expected_status)
