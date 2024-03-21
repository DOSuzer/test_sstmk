import re
import socket
from collections import OrderedDict

import requests


PHONE_NUMBER_RETRIVE = re.compile(
    r"class=\"phone-number\".+>([\d\- ()+]+)<"
)

PHONE_NUMBER_CHECK = re.compile(
    r"^(\+(\d{0,3}))?(\(\d{3,5}\))(\d{1,3})\-(\d{1,2})\-(\d{1,2})$"
)


TRANSFORM_PATTERNS = OrderedDict({
    r" ": r"",
    r"^\(": r"+7(",
    r"^8\(": r"+7(",
})


def get_response(url: str) -> requests.Response | None:
    """
    Проверка доступности страницы.
    Если страница доступна возвращает объект response.
    """
    response = requests.get(url)
    if response.status_code == 200:
        return response
    return None


def get_phone_number(data: str) -> str:
    """Получение номера телефона."""
    result = PHONE_NUMBER_RETRIVE.findall(data)
    return result[0]


def valid_phone_number(data: str) -> str:
    """Проверка номера телефона на соответствие паттерну."""
    for pattern, replacement in TRANSFORM_PATTERNS.items():
        data = re.sub(pattern, replacement, data)
    if not PHONE_NUMBER_CHECK.match(data):
        return "Retrived phone number is not valid."
    return f"Valid phone number is: {data}"


def find_phone_numbers_on_page(url: str) -> str:
    """Поиск номеров телефонов на странице."""
    try:
        ip_address = socket.gethostbyname(url)
    except socket.gaierror:
        return f"Host `{url}` is not resolved."
    print(f"Host `{url}` is at `{ip_address}`.")
    response = get_response('https://' + url)
    if not response:
        return f"Requested page `https://{url}` is not available."
    print(f"Requested page `https://{url}` is available.")
    phone_num = get_phone_number(response.text)
    if not phone_num:
        return "Phone number not found in requested page."
    print(f"Retrived phone number `{phone_num}`.")
    return valid_phone_number(phone_num)


if __name__ == "__main__":
    url = "sstmk.ru"
    print(find_phone_numbers_on_page(url))
