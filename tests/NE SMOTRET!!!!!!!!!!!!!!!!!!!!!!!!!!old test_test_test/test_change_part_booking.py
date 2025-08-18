import pytest
from constants import HEADERS, BASE_URL


class TestBookings:
    def test_updata_booking(self, auth_session, booking_data, booking_data2):
        # Создаём бронирование
        create_booking = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
        assert create_booking.status_code == 200, "Ошибка при создании брони"

        booking_id = create_booking.json().get("bookingid")
        assert booking_id is not None, "Идентификатор брони не найден в ответе"
        assert create_booking.json()["booking"]["firstname"] == booking_data["firstname"], "Заданное имя не совпадает"
        assert create_booking.json()["booking"]["totalprice"] == booking_data["totalprice"], "Заданная стоимость не совпадает"
        # Обновляем бронирование
        patch_booking = auth_session.patch(f"{BASE_URL}/booking/{booking_id}", json=booking_data2)
        assert patch_booking.status_code == 200, "Бронь не найдена"
        assert patch_booking.json()["firstname"] != booking_data["firstname"], "Заданное имя  совпадает"

        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 200, "Бронь не найдена"
        assert get_booking.json()["lastname"] == booking_data2["lastname"], "Заданная фамилия не совпадает"