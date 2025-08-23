class TestUser:
    def test_create_user(self, admin_api_manager, test_user_generate):
        create_user = admin_api_manager.user_api.create_user(test_user_generate)
        user_id = create_user.json().get("id")
        assert user_id is not None, "Идентификатор не найден в ответе"

    def test_duble_create_user(self, admin_api_manager, test_user_generate):
        create_user = admin_api_manager.user_api.create_user(test_user_generate)
        user_id = create_user.json().get("id")
        assert user_id is not None, "Идентификатор не найден в ответе"
        create_user2 = admin_api_manager.user_api.create_user(test_user_generate, expected_status=409)

    def test_delete_user(self, admin_api_manager, test_user_generate):
        create_user = admin_api_manager.user_api.create_user(test_user_generate)
        user_id = create_user.json().get("id")
        assert user_id is not None, "Идентификатор не найден в ответе"
        delete_user = admin_api_manager.user_api.delete_user(user_id, expected_status=200)

    def test_change_user(self, admin_api_manager, test_user_generate, test_user_for_updata):
        create_user = admin_api_manager.user_api.create_user(test_user_generate)
        user_id = create_user.json().get("id")
        assert user_id is not None, "Идентификатор не найден в ответе"
        patch_user = admin_api_manager.user_api.patch_user(user_id,test_user_for_updata)


    def test_wrong_change_user(self, admin_api_manager, test_user_generate, test_user_for_updata):
        create_user = admin_api_manager.user_api.create_user(test_user_generate)
        user_id = create_user.json().get("id")
        assert user_id is not None, "Идентификатор не найден в ответе"
        patch_user = admin_api_manager.user_api.patch_user(user_id, {"banned": "true", "roles": ["PUPPY"]}, expected_status=400)

