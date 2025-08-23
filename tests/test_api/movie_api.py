from custom_requester.custom_requester import CustomRequester
from constants import MOVIE_ENDPOINT


class MovieAPI(CustomRequester):
    """
    Класс для работы с API фильмов.
    """

    # def __init__(self, session):
    #     super().__init__(base_url=session.base_url)
    #     self.session = session

    def __init__(self, session, base_url):  # принимаем оба параметра
        super().__init__(session=session, base_url="https://api.dev-cinescope.coconutqa.ru/")

    def get_movie_info(self, movie_id, expected_status=200):
        """
        Получение информации о пользователе.
        :param movie_id: ID фильма.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="GET",
            endpoint=f"{MOVIE_ENDPOINT}/{movie_id}",
            expected_status=expected_status
        )

    def get_movie_all(self, expected_status=200):
        """
        Получение информации о пользователе.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="GET",
            endpoint=MOVIE_ENDPOINT,
            expected_status=expected_status
        )

    def delete_movie(self, movie_id, expected_status=200):
        """
        Удаление пользователя.
        :param movie_id: ID фильма.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="DELETE",
            endpoint=f"/{MOVIE_ENDPOINT}/{movie_id}",
            expected_status=expected_status
        )

    def create_movie(self, test_movie, expected_status=201):
        """

        param test_movie: Данные с фильмом
        param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="POST",
            endpoint=MOVIE_ENDPOINT,
            data=test_movie,
            expected_status=expected_status

        )

    def patch_movie(self, movie_id, test_movie_for_updata, expected_status=200):
        return self.send_request(
            method="PATCH",
            endpoint=MOVIE_ENDPOINT + f"/{movie_id}",
            data=test_movie_for_updata,
            expected_status=expected_status
        )
