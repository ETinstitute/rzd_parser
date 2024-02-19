import bs4
import requests
import warnings
import pandas as pd
from typing import Union, Optional, Iterable
from bs4 import BeautifulSoup
from datetime import datetime

from RZD_Parser.exceptions.request_exceptions import RZDConnectionError
from RZD_Parser.url import URLFactory
from RZD_Parser.exceptions import RZhDBadRequest
from RZD_Parser.parser.web_parser import (get_supply_data)


class Parser:
    # Скопировал с StackOverflow, честно хз зачем нужно, но без нее не работает
    __headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
    }

    engine = 'html.parser'

    def __init__(
            self,
            date_publication_0: Union[str, datetime],
            date_publication_1: Union[str, datetime] = datetime.now(),
            rubricator_id: int = 57,
            text_search: str = 'погрузка на сети',
            pagenumber: int = 1,

            # some big number
            pagesize: int = 10000

    ):
        """Class for parsing the Russian Railways website

        Args:
            date_publication_0 (datetime): the left boundary of time
            date_publication_1 (datetime, optional): the right boundary of time. Defaults to datetime.now().
            rubricator_id (int, optional): ... . Defaults to 57 ('погрузка на сети').
            text_search (str, optional): ... . Defaults to 'погрузка на сети'.
        """

        self.url_factory = URLFactory(
            f810_pagesize=pagesize,
            text_search=text_search,
            rubricator_id=rubricator_id,
            date_publication_0=date_publication_0,
            date_publication_1=date_publication_1,
            f810_pagenumber=pagenumber
        )

        self.url = self.url_factory.url
        self.response = None

    def parse_data(self, dropna=True) -> pd.DataFrame:
        """
        Returns pandas.DataFrame with the following data: text, value and date

        If the drona value is True, then only non-empty values will remain
        """

        data = self.__get_data()

        df = pd.DataFrame(data, columns=['text', 'values', 'date'])
        return df if not dropna else df[df['values'] != 'None']

    def __get_data(self) -> list[tuple]:
        url = self.url_factory.url

        page_count = self.__get_page_count(url)
        data = list()

        for page_number in page_count:
            self.url_factory.f810_pagenumber = page_number
            self.url_factory.update_parameters()

            url = self.url_factory.url

            data.append(self.__get_page(url=url))

        # [[1, 2], [3, 4]] -> [1, 2, 3, 4]
        data = sum(data, [])

        return data

    def __get_page_count(self, url) -> Iterable[int]:
        response = requests.get(url, headers=self.__headers)
        soup = BeautifulSoup(response.text, self.engine).find_all('a', class_='pager__link')

        n = 1 if not soup else int(soup[-1].text)

        return range(1, n + 1)

    def __get_page(self, url) -> list[tuple]:
        """
        Returns parsed web page

        if the code is not 200, the RZD Exception is raised
        """

        response = requests.get(url, headers=self.__headers)

        if response.status_code == 200:
            return self.__parse_page(response)

        if 400 <= response.status_code < 500:
            raise RZDConnectionError(url=url)

        raise RZhDBadRequest(status_code=response.status_code, message=None)

    def __parse_page(self, response) -> list[tuple]:
        soup = BeautifulSoup(response.text, self.engine)

        text = map(lambda row: row.a.text, soup.find_all('div', class_='search-results__content'))
        values = map(lambda row: self.__parse_values(row), soup.find_all('div', class_='search-results__content'))
        dates = map(lambda row: self.__parse_dates(row), soup.find_all('div', class_='search-results__date'))

        data = zip(text, values, dates)

        return list(data)

    @staticmethod
    def __parse_dates(row: bs4.element.Tag) -> Optional[str]:
        text = row.text.split()[0]

        return text

    @staticmethod
    def __parse_values(row: bs4.element.Tag) -> Optional[str]:
        text = row.a.text

        try:
            value = get_supply_data(text)

        except Exception as exc:
            return warnings.warn(f'skip raw: {text}')

        return str(value)
