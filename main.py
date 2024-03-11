import re

import requests


PHONE_NUMBER_RETRIVE = re.compile(
    r"(?:(?:8|\+7) {0,1})?(?:\(?\d{3}\)?[\- ]{0,1})[\d\- ]{7,10}"
)
# Допускаем что вокруг скобок могут быть пробелы как в примере:
PHONE_NUMBER_CHECK = re.compile(
    r"^\+?(\d{0,3})( ?\(\d{3,5}\) ?)(\d{1,3})\-(\d{1,2})\-(\d{1,2})$"
)


def get_response(url: str) -> requests.Response | None:
    """
    Проверка доступности страницы.
    Если страница доступна возвращает объект response.
    """
    response = requests.get(url)
    if response.status_code == 200:
        return response
    return None


def get_phone_numbers(data: str) -> str:
    """Получение номера телефона."""
    result = PHONE_NUMBER_RETRIVE.findall(data)
    print(result)
    return result


def valid_phone_number(data: str) -> bool:
    """Проверка номера телефона на соответствие паттерну."""
    if PHONE_NUMBER_CHECK.match(data):
        return True
    return False


def find_phone_numbers_on_page(url: str) -> list | None:
    """Поиск номеров телефонов на странице."""
    response = get_response(url)
    if not response:
        print(f"Requested page `{url}` is not available.")
        return None
    print(f"Requested page `{url}` is available.")
    phone_nums = get_phone_numbers(response.text)
    if not phone_nums:
        print("Phone numbers not found in requested page.")
        return None
    valid_numbers = []
    for num in phone_nums:
        print(f"Retrived number: {num}")
        if valid_phone_number(num) and num not in valid_numbers:
            valid_numbers.append(num)
    return valid_numbers


if __name__ == "__main__":
    url = "https://sstmk.ru"
    result = find_phone_numbers_on_page(url)
    print(f"Found valid phone numbers on page: {result if result else 'None'}")
