"""
This module parses and converts data from HTML response to pandas.DataFrame

"""


import requests.models

MONTH_LIST = ['январе', 'фервале', 'марте', 'апреле', 'мае', 'июне', 'июле', 'августе', 'сентябре',
              'октябре', 'ноябре', 'декабре']
BAN_WORDS = MONTH_LIST + ['в'] + ['году'] + [str(year) for year in range(2000, 2025)]
METRIC_LIST = ['млн', 'млрд', 'тонн']


def get_supply_data(text: str) -> str:
    """
    Returns supply data.

    Если есть % то возвращает None (Значит там прирост, это мы можем и сами посчитать)
    Если данные за год суммарно, то возвращает None, чтобы данные не повторялись
    # TODO: Сделать раздельную логику для селекта за год и за месяцы

    Если в сообщении есть размерность (млн тонн и прочее) то удаляем месяц, 'в' и прочие BAN WORDS
    Если размерности в конце сообщения нет, то сохраняем ее и добавляем в конец

    Examples:
        >>> get_supply_data('Погрузка экспортных грузов в порты на сети ОАО «РЖД» выросла на 0,9% в январе-ноябре')
        >>> None

        >>> get_supply_data('Погрузка на сети ОАО «РЖД» составила 1,2 млрд тонн в 2020 году')
        >>> None

        >>> get_supply_data('Погрузка на сети ОАО «РЖД» составила 106,7 млн тонн в марте')
        >>> '106,7 млн тонн в марте'
    """

    if '%' in text:
        return None

    if 'году' in text:
        return None

    text = text
    total_value = text.split('составила')[1]

    metric = " ".join([el for el in text.split() if el in METRIC_LIST])

    if any(map(lambda k: k in METRIC_LIST, total_value.split())):
        return " ".join([el for el in total_value.split() if el not in BAN_WORDS])

    else:
        return total_value + metric

