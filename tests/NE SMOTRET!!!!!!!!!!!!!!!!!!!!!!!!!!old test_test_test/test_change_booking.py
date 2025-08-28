import faker.generator
import pytest
from faker import Faker
from constants import HEADERS, BASE_URL
import requests


pytestmark = pytest.mark.skip(reason="TASK-1234: Тесты временно отключены из-за нестабильности")

class TestBookings:
    def test_updata_booking(self, auth_session, booking_data, booking_data1):
        # Создаём бронирование
        create_booking = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
        assert create_booking.status_code == 200, "Ошибка при создании брони"

        booking_id = create_booking.json().get("bookingid")
        assert booking_id is not None, "Идентификатор брони не найден в ответе"
        assert create_booking.json()["booking"]["firstname"] == booking_data["firstname"], "Заданное имя не совпадает"
        assert create_booking.json()["booking"]["totalprice"] == booking_data["totalprice"], "Заданная стоимость не совпадает"
        # Обновляем бронирование
        put_booking = auth_session.put(f"{BASE_URL}/booking/{booking_id}", json=booking_data1)
        assert put_booking.status_code == 200, "Бронь не найдена"
        assert put_booking.json()["firstname"] != booking_data["firstname"], "Заданное имя  совпадает"
        assert put_booking.json()["totalprice"] != booking_data["totalprice"], "Заданная стоимость совпадает"
        assert put_booking.json()["lastname"] != booking_data["lastname"], "Заданное имя  совпадает"

        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 200, "Бронь не найдена"
        assert get_booking.json()["lastname"] == booking_data1["lastname"], "Заданная фамилия не совпадает"

    def test_wrong_creation(self, auth_session,wrong_booking_data):
        # Создаём бронирование
        create_booking = auth_session.post(f"{BASE_URL}/booking", json=wrong_booking_data)
        assert create_booking.status_code == 500, "Ошибка при создании брони не появилась"


    def test_wrong_updata(self, auth_session, booking_data, booking_data1):
        create_booking = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
        assert create_booking.status_code == 200, "Ошибка при создании брони"

        booking_id = 0000
        assert booking_id is not None, "Идентификатор брони не найден в ответе"
        assert create_booking.json()["booking"]["firstname"] == booking_data["firstname"], "Заданное имя не совпадает"
        assert create_booking.json()["booking"]["totalprice"] == booking_data[
            "totalprice"], "Заданная стоимость не совпадает"
        # Обновляем бронирование
        put_booking = auth_session.put(f"{BASE_URL}/booking/{booking_id}", json=booking_data1)
        assert put_booking.status_code == 405, "Что то не так"

    def test_delete_without_autorization(self,auth_session, booking_data):
        create_booking = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
        assert create_booking.status_code == 200, "Ошибка при создании брони"

        booking_id = create_booking.json().get("bookingid")
        assert booking_id is not None, "Идентификатор брони не найден в ответе"
        assert create_booking.json()["booking"]["firstname"] == booking_data["firstname"], "Заданное имя не совпадает"
        assert create_booking.json()["booking"]["totalprice"] == booking_data[ "totalprice"], "Заданная стоимость не совпадает"

        deleted_booking = requests.delete(f"{BASE_URL}/booking/{booking_id}")
        assert deleted_booking.status_code == 403, "Ожидалось 403 ошибка"

    def test_get_wrong_booking(self, auth_session, booking_data):
        create_booking = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
        assert create_booking.status_code == 200, "Ошибка при создании брони"

        booking_id = create_booking.json().get("bookingid")
        assert booking_id is not None, "Идентификатор брони не найден в ответе"
        assert create_booking.json()["booking"]["firstname"] == booking_data["firstname"], "Заданное имя не совпадает"
        assert create_booking.json()["booking"]["totalprice"] == booking_data[
            "totalprice"], "Заданная стоимость не совпадает"

        get_booking = auth_session.get(f"{BASE_URL}/booking/0000")
        assert get_booking.status_code == 404, "Бронь не дб найдена"
