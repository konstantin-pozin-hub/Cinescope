import pytest


class TestUser:

    def test_create_user(self, super_admin, creation_user_data):
        response = super_admin.api.user_api.create_user(creation_user_data).json()

        assert response.get('id') and response['id'] != '', "ID должен быть не пустым"
        assert response.get('email') == creation_user_data['email']
        assert response.get('fullName') == creation_user_data['fullName']
        assert len(response.get('roles', [])) == 1
        assert creation_user_data['roles'] in response.get('roles', [])
        assert response.get('verified') is True

    def test_get_user_by_locator(self, super_admin, creation_user_data):
        created_user_response = super_admin.api.user_api.create_user(creation_user_data).json()
        response_by_id = super_admin.api.user_api.get_user(created_user_response['id']).json()
        response_by_email = super_admin.api.user_api.get_user(creation_user_data['email']).json()

        assert response_by_id == response_by_email, "Содержание ответов должно быть идентичным"
        assert response_by_id.get('id') and response_by_id['id'] != '', "ID должен быть не пустым"
        assert response_by_id.get('email') == creation_user_data['email']
        assert response_by_id.get('fullName') == creation_user_data['fullName']
        assert len(response_by_id.get('roles', [])) == 1
        assert creation_user_data['roles'] in response_by_id.get('roles', [])
        assert response_by_id.get('verified') is True

    @pytest.mark.slow
    def test_get_user_by_id_common_user(self, common_user):
        common_user.api.user_api.get_user(common_user.email, expected_status=403)

    @pytest.mark.slow
    def test_duble_create_user(self, super_admin, test_user_generate):
        create_user = super_admin.api.user_api.create_user(test_user_generate)
        user_id = create_user.json().get("id")
        assert user_id is not None, "Идентификатор не найден в ответе"
        create_user2 = super_admin.api.user_api.create_user(test_user_generate, expected_status=409)

    def test_delete_user(self, super_admin, test_user_generate):
        create_user = super_admin.api.user_api.create_user(test_user_generate)
        user_id = create_user.json().get("id")
        assert user_id is not None, "Идентификатор не найден в ответе"
        delete_user = super_admin.api.user_api.delete_user(user_id, expected_status=200)

    def test_change_user(self, super_admin, test_user_generate, test_user_for_updata):
        create_user = super_admin.api.user_api.create_user(test_user_generate)
        user_id = create_user.json().get("id")
        assert user_id is not None, "Идентификатор не найден в ответе"
        patch_user = super_admin.api.user_api.patch_user(user_id, test_user_for_updata)

    def test_wrong_change_user(self, super_admin, test_user_generate, test_user_for_updata):
        create_user = super_admin.api.user_api.create_user(test_user_generate)
        user_id = create_user.json().get("id")
        assert user_id is not None, "Идентификатор не найден в ответе"
        patch_user = super_admin.api.user_api.patch_user(user_id, {"banned": "true", "roles": ["PUPPY"]},
                                                         expected_status=400)
