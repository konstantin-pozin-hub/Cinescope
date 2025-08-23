from tests.test_api.auth_api import AuthAPI
from tests.test_api.movie_api import MovieAPI
from tests.test_api.user_api import UserAPI


class ApiManager:
    """
    Класс для управления API-классами с единой HTTP-сессией.
    """

    def __init__(self, session, base_url):
        """
        Инициализация ApiManager.
        :param session: HTTP-сессия, используемая всеми API-классами.
        """
        self.session = session
        self.auth_api = AuthAPI(session)
        self.user_api = UserAPI(session, base_url)
        self.base_url = base_url
        self.movie_api = MovieAPI(session,base_url)
