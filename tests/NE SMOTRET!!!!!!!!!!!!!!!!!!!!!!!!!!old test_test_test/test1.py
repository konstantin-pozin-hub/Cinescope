import requests
from faker import Faker

fake = Faker()


def test_google():
    response = requests.get("https://www.google.com")
    assert response.status_code == 200


def test_hello():
    print("hello")

def test_addition():
    assert 2 + 2 == 4