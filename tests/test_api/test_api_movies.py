import pytest
import requests
from constants import movie_url, HEADERS, admin_data


class TestMovie:

    def test_get_all_movies(self):
        get_all_movie = requests.get(movie_url, headers=HEADERS)
        assert get_all_movie.status_code == 200, "Что то не так, ожидался 200 статус"

    def test_get_id_movie(self):
        movie_id = 25
        get_id_movie = requests.get(f"{movie_url}/{movie_id}", headers=HEADERS)
        assert get_id_movie.status_code == 200, "Что то не так, ожидался 200 статус"
        name = get_id_movie.json().get("name")
        assert name == "фывфывфывфывe", "Имена не совпадают"

    def test_create_movie(self, admin_session, test_movie1):
        create_movie = admin_session.post(movie_url, json=test_movie1, headers=HEADERS)
        assert create_movie.status_code == 201, "Ошибка при создании юзера"
        movie_id = create_movie.json().get("id")
        assert movie_id is not None, "Идентификатор не найден в ответе"

    def test_wrong_create_movie(self, admin_session, test_movie3):
        create_movie = admin_session.post(movie_url, json=test_movie3, headers=HEADERS)
        assert create_movie.status_code == 400, "Ошибка при создании юзера"

    def test_duble_create_movie(self, admin_session, test_movie1):
        create_movie = admin_session.post(movie_url, json=test_movie1, headers=HEADERS)
        assert create_movie.status_code == 201, "Ошибка при создании юзера"
        movie_id = create_movie.json().get("id")
        assert movie_id is not None, "Идентификатор не найден в ответе"
        create_movie2 = admin_session.post(movie_url, json=test_movie1, headers=HEADERS)
        assert create_movie2.status_code == 409

    def test_delete_movie(self, admin_session, test_movie1):
        create_movie = admin_session.post(movie_url, json=test_movie1, headers=HEADERS)
        assert create_movie.status_code == 201, "Ошибка при создании юзера"
        movie_id = create_movie.json().get("id")
        assert movie_id is not None, "Идентификатор не найден в ответе"
        delete_movie = admin_session.delete(f"{movie_url}/{movie_id}", headers=HEADERS)
        assert delete_movie.status_code == 200

    def test_duble_delete_movie(self, admin_session, test_movie1):
        create_movie = admin_session.post(movie_url, json=test_movie1, headers=HEADERS)
        assert create_movie.status_code == 201, "Ошибка при создании юзера"
        movie_id = create_movie.json().get("id")
        assert movie_id is not None, "Идентификатор не найден в ответе"
        delete_movie = admin_session.delete(f"{movie_url}/{movie_id}", headers=HEADERS)
        assert delete_movie.status_code == 200
        duble_delete_movie = admin_session.delete(f"{movie_url}/{movie_id}", headers=HEADERS)
        assert duble_delete_movie.status_code == 404

    def test_wrong_delete_movie(self,admin_session,test_movie1):
        create_movie = admin_session.post(movie_url, json=test_movie1, headers=HEADERS)
        assert create_movie.status_code == 201, "Ошибка создания юзера"
        wrong_delete_movie = admin_session.delete(f"{movie_url}/aaaaaaaaaaaaa",headers=HEADERS)
        assert wrong_delete_movie.status_code == 404
    def test_change_movie(self, admin_session, test_movie1, test_movie2):
        create_movie = admin_session.post(movie_url, json=test_movie1, headers=HEADERS)
        assert create_movie.status_code == 201, "Ошибка при создании юзера"
        movie_id = create_movie.json().get("id")
        assert movie_id is not None, "Идентификатор не найден в ответе"
        patch_movie = admin_session.patch(f"{movie_url}/{movie_id}",
                                          json=test_movie2, headers=HEADERS)
        assert patch_movie.status_code == 200, 'Ошибка при обновлении данных'

    def test_wrong_change_movie(self, admin_session, test_movie1):
        create_movie = admin_session.post(movie_url, json=test_movie1, headers=HEADERS)
        assert create_movie.status_code == 201, "Ошибка при создании юзера"
        movie_id = create_movie.json().get("id")
        assert movie_id is not None, "Идентификатор не найден в ответе"
        patch_movie = admin_session.patch(f"{movie_url}/{movie_id}",
                                          json={"roles": ["SUPERBOSS"], "verified": True, "banned": False},
                                          headers=HEADERS)
        assert patch_movie.status_code == 400, 'Ожидалась 400'
