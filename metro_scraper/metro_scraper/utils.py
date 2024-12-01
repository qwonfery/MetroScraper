import re


def to_number_string(cost_string: str) -> str:
    """
    Функция заменяет все нецифровые символы в строке на ""
    :param cost_string:
    :return: обработанная строка
    """

    return re.sub(r'\D', '', cost_string)