class TestMovie:

    def test_get_all_movies(self, api_manager):
        get_all_movies = api_manager.movie_api.get_movie_all()
        assert get_all_movies.status_code == 200, "Что то не так, ожидался 200 статус"

    def test_get_id_movie(self, api_manager):
        response = api_manager.movie_api.get_movie_info(22)
        response_data = response.json()
        assert response.status_code == 200, "Что то не так, ожидался 200 статус"
        name = response_data.get("name")
        assert name == "Море крови и рваных жоп", "Имена не совпадают"

    def test_create_movie(self, admin_api_manager, test_movie):
        create_movie = admin_api_manager.movie_api.create_movie(test_movie)
        movie_id = create_movie.json().get("id")
        assert movie_id is not None, "Идентификатор не найден в ответе"

    def test_wrong_create_movie(self, admin_api_manager, test_movie_with_wrong_data):
        wrong_create_movie = admin_api_manager.movie_api.create_movie(test_movie_with_wrong_data,expected_status=400)
        assert wrong_create_movie.status_code == 400, "Ошибка при создании фильма"

    def test_duble_create_movie(self, admin_api_manager, test_movie):
        create_movie = admin_api_manager.movie_api.create_movie(test_movie)
        movie_id = create_movie.json().get("id")
        assert movie_id is not None, "Идентификатор не найден в ответе"
        create_movie2 = admin_api_manager.movie_api.create_movie(test_movie,expected_status=409)

    def test_delete_movie(self, admin_api_manager, test_movie):
        create_movie = admin_api_manager.movie_api.create_movie(test_movie)
        movie_id = create_movie.json().get("id")
        assert movie_id is not None, "Идентификатор не найден в ответе"
        delete_movie = admin_api_manager.movie_api.delete_movie(movie_id,expected_status=200)
        check_delete_movie = admin_api_manager.movie_api.get_movie_info(movie_id,expected_status=404)

    def test_duble_delete_movie(self, admin_api_manager, test_movie):
        create_movie = admin_api_manager.movie_api.create_movie(test_movie)
        movie_id = create_movie.json().get("id")
        assert movie_id is not None, "Идентификатор не найден в ответе"
        delete_movie = admin_api_manager.movie_api.delete_movie(movie_id,expected_status=200)
        check_delete_movie = admin_api_manager.movie_api.get_movie_info(movie_id,expected_status=404)
        duble_delete_movie = admin_api_manager.movie_api.delete_movie(movie_id,expected_status=404)

    def test_wrong_delete_movie(self, admin_api_manager, test_movie):
        create_movie = admin_api_manager.movie_api.create_movie(test_movie)
        wrong_delete_movie = admin_api_manager.movie_api.delete_movie(0,expected_status=404)

    def test_change_movie(self, admin_api_manager, test_movie, test_movie_for_updata):
        create_movie = admin_api_manager.movie_api.create_movie(test_movie)
        movie_id = create_movie.json().get("id")
        assert movie_id is not None, "Идентификатор не найден в ответе"
        patch_movie = admin_api_manager.movie_api.patch_movie(movie_id, test_movie_for_updata)

    def test_wrong_change_movie(self, admin_api_manager, test_movie):
        create_movie = admin_api_manager.movie_api.create_movie(test_movie)
        movie_id = create_movie.json().get("id")
        assert movie_id is not None, "Идентификатор не найден в ответе"
        patch_movie = admin_api_manager.movie_api.patch_movie(movie_id, {"roles": ["SUPERBOSS"], "verified": True, "banned": False},expected_status=404)
