import typing


def multiply(a: int, b: int) -> int:
    return a * b


print(multiply("5", 4))


def sum_numbers(numbers: list[int]) -> int:
    return sum(numbers)


print(sum_numbers([1, 2, 3, 5, 67, 8]))


def find_user(user_id: int) -> typing.Optional[str]:
    if user_id == 1:
        return "Пользователь найден"
    return None


print(find_user(0))
print(find_user(1))


def process_input(value: typing.Union[str, int]) -> typing.Union:
    return f"Ты передал: {value}"


print(process_input("xbd"))
print(process_input(12))


class User:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def greet(self) -> str:
        return f"Привет, меня зовут {self.name}!"
user1=User("Alex", 25)
print(user1.greet())


def get_even_numbers(numbers: list[int]) -> list[int]:
    return [num for num in numbers if num % 2 == 0]
print(get_even_numbers([1,2,3,4,5,67,8,9]))