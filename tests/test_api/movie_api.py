from custom_requester.custom_requester import CustomRequester
from constants import MOVIE_ENDPOINT


class MovieAPI(CustomRequester):

    USER_BASE_URL = "https://api.dev-cinescope.coconutqa.ru/"

    def __init__(self, session):
        self.session = session
        super().__init__(session, self.USER_BASE_URL)

    def get_movie_info(self, movie_id, expected_status=200):
        return self.send_request("GET", f"movies/{movie_id}", expected_status=expected_status)

    def get_all_movie(self, expected_status=200):
        return self.send_request("GET", f"movies", expected_status=expected_status)

    def create_movie(self, test_movie, expected_status=201):
        return self.send_request(
            endpoint="movies",
            method="POST",
            data=test_movie,
            expected_status=expected_status
        )

    def delete_movie(self, movie_id, expected_status=204):
        return self.send_request("DELETE", f"movies/{movie_id}", expected_status=expected_status)

    def patch_movie(self, movie_id, test_movie_for_updata, expected_status=200):
        return self.send_request(
            method="PATCH",
            endpoint=MOVIE_ENDPOINT + f"/{movie_id}",
            data=test_movie_for_updata,
            expected_status=expected_status
        )

    def get_filtred_movie(self, params, expected_status=200):
        string_params = ""
        for param_name, param_value in params.items():
            string_params += f"{param_name}={param_value}&"

        return self.send_request("GET", f"movies/?{string_params}", expected_status=expected_status)
