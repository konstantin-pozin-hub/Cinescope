import pytest


class TestMovie:

    # def test_get_all_movies(self, api_manager):
    #     get_all_movies = api_manager.movie_api.get_movie_all()
    #     assert get_all_movies.status_code == 200, "Что то не так, ожидался 200 статус"
    #
    # def test_get_id_movie(self, api_manager):
    #     response = api_manager.movie_api.get_movie_info(22)
    #     response_data = response.json()
    #     assert response.status_code == 200, "Что то не так, ожидался 200 статус"
    #     name = response_data.get("name")
    #     assert name == "Море крови и рваных жоп", "Имена не совпадают"
    @pytest.mark.slow
    def test_create_movie(self, super_admin, test_movie):
        response = super_admin.api.movie_api.create_movie(test_movie).json()

        assert response.get('id') and response['id'] != '', "ID должен быть не пустым"
        assert response.get('price') == test_movie['price']
        assert response.get('name') == test_movie['name']
        assert response.get('description') == test_movie['description']

    def test_wrong_create_movie(self, super_admin, test_movie_with_wrong_data):
        wrong_create_movie = super_admin.api.movie_api.create_movie(test_movie_with_wrong_data,
                                                                    expected_status=400).json()

    def test_duble_create_movie(self, super_admin, test_movie):
        response = super_admin.api.movie_api.create_movie(test_movie).json()
        assert response.get('id') and response['id'] != '', "ID должен быть не пустым"
        create_movie2 = super_admin.api.movie_api.create_movie(test_movie, expected_status=409)

    @pytest.mark.db
    def test_delete_movie(self, super_admin, test_movie):
        create_movie = super_admin.api.movie_api.create_movie(test_movie)
        movie_id = create_movie.json().get("id")
        assert movie_id is not None, "Идентификатор не найден в ответе"
        delete_movie = super_admin.api.movie_api.delete_movie(movie_id, expected_status=200)
        check_delete_movie = super_admin.api.movie_api.get_movie_info(movie_id, expected_status=404)

    @pytest.fixture
    def user(self, request):
        return request.getfixturevalue(request.param)

    @pytest.mark.parametrize("user,status_code",
                             [('common_user', 403),
                              ('super_admin', 200)],
                             indirect=['user'])
    def test_delete_movie(self, super_admin, user, test_movie, status_code):
        create_movie = super_admin.api.movie_api.create_movie(test_movie)
        movie_id = create_movie.json().get("id")
        assert movie_id is not None, "Идентификатор не найден в ответе"
        responce = user.api.movie_api.delete_movie(movie_id, expected_status=status_code)

    @pytest.mark.ui
    def test_duble_delete_movie(self, super_admin, test_movie):
        create_movie = super_admin.api.movie_api.create_movie(test_movie)
        movie_id = create_movie.json().get("id")
        assert movie_id is not None, "Идентификатор не найден в ответе"
        delete_movie = super_admin.api.movie_api.delete_movie(movie_id, expected_status=200)
        check_delete_movie = super_admin.api.movie_api.get_movie_info(movie_id, expected_status=404)
        duble_delete_movie = super_admin.api.movie_api.delete_movie(movie_id, expected_status=404)

    skip_test = False

    @pytest.mark.skipif(skip_test, reason="Так захотелось")
    def test_wrong_delete_movie(self, super_admin, test_movie):
        create_movie = super_admin.api.movie_api.create_movie(test_movie)
        wrong_delete_movie = super_admin.api.movie_api.delete_movie(0, expected_status=404)

    @pytest.mark.skip()
    def test_change_movie(self, super_admin, test_movie, test_movie_for_updata):
        create_movie = super_admin.api.movie_api.create_movie(test_movie)
        movie_id = create_movie.json().get("id")
        assert movie_id is not None, "Идентификатор не найден в ответе"
        patch_movie = super_admin.api.movie_api.patch_movie(movie_id, test_movie_for_updata)

    def test_wrong_change_movie(self, super_admin, test_movie):
        create_movie = super_admin.api.movie_api.create_movie(test_movie)
        movie_id = create_movie.json().get("id")
        assert movie_id is not None, "Идентификатор не найден в ответе"
        patch_movie = super_admin.api.movie_api.patch_movie(movie_id, {"roles": ["SUPERBOSS"], "verified": True,
                                                                       "banned": False}, expected_status=404)

    @pytest.mark.slow
    def test_common_create_movie(self, common_user, test_movie):
        response = common_user.api.movie_api.create_movie(test_movie, expected_status=403).json()

    @pytest.mark.slow
    @pytest.mark.parametrize(
        "params", [
            {"minPrice": 1, "maxPrice": 1000},
            {"location": ["SPB", "MSK"]},
            {"genreID": 1}
        ],
        ids=[
            "Filtred by minPrice and maxPrice",
            "Filtred by location",
            "Filtred by genreID"
        ]
    )
    def test_filtes(self, super_admin, params):
        responce = super_admin.api.movie_api.get_filtred_movie(params)
