import pytest
import requests
from constants import BASE_URL, HEADERS, admin_data


class TestUser:
    def test_create_user(self, admin_session, test_user2):
        create_user = admin_session.post(f'{BASE_URL}/user', json=test_user2)
        assert create_user.status_code == 201, "Ошибка при создании юзера"
        user_id = create_user.json().get("id")
        assert user_id is not None, "Идентификатор не найден в ответе"

    def test_duble_create_user(self, admin_session, test_user2):
        create_user = admin_session.post(f"{BASE_URL}/user", json=test_user2)
        assert create_user.status_code == 201, "Ошибка при создании юзера"
        user_id = create_user.json().get("id")
        assert user_id is not None, "Идентификатор не найден в ответе"
        create_user2 = admin_session.post(f"{BASE_URL}/user", json=test_user2)
        assert create_user2.status_code == 409

    def test_delete_user(self, admin_session, test_user2):
        create_user = admin_session.post(f'{BASE_URL}/user', json=test_user2)
        assert create_user.status_code == 201, "Ошибка при создании юзера"
        user_id = create_user.json().get("id")
        assert user_id is not None, "Идентификатор не найден в ответе"
        delete_user = admin_session.delete(f'{BASE_URL}/user/{user_id}')
        assert delete_user.status_code == 200

    def test_change_user(self, admin_session, test_user2):
        create_user = admin_session.post(f'{BASE_URL}/user', json=test_user2)
        assert create_user.status_code == 201, "Ошибка при создании юзера"
        user_id = create_user.json().get("id")
        assert user_id is not None, "Идентификатор не найден в ответе"
        user_id = create_user.json().get("id")
        assert user_id is not None, "Идентификатор не найден в ответе"
        patch_user = admin_session.patch(f'{BASE_URL}/user/{user_id}', json={"banned": "true", "roles": ["ADMIN"]})
        assert patch_user.status_code == 200, 'Ошибка при обновлении данных'

    def test_wrong_change_user(self, admin_session, test_user2):
        create_user = admin_session.post(f'{BASE_URL}/user', json=test_user2)
        assert create_user.status_code == 201, "Ошибка при создании юзера"
        user_id = create_user.json().get("id")
        assert user_id is not None, "Идентификатор не найден в ответе"
        user_id = create_user.json().get("id")
        assert user_id is not None, "Идентификатор не найден в ответе"
        patch_user = admin_session.patch(f'{BASE_URL}/user/{user_id}', json={"banned": "true", "roles": ["PUPPY"]})
        assert patch_user.status_code == 400, 'Ожидалась 400'
