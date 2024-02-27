import requests
from typing import Iterable, Optional
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict, TypeVar

from RZD_Parser.url import URLFactory
from RZD_Parser.parser.data_parser import DataParser


Data = TypeVar('Data', bound=List[Dict[str, float]])
Index = TypeVar('Index', bound=List[datetime])
URL = TypeVar('URL', bound=str)


class HTMLUtils:
    __headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
    }

    engine = 'html.parser'

    def __init__(self):
        self.url_factory = None
        self.data_parser = DataParser()

    @property
    def response(self):
        return requests.get(self.url_factory.url, headers=self.__headers)

    def get_data(self, url_factory) -> tuple[Data, Index]:
        """Returns data (list of dicts) and index (list of dates)"""

        self.url_factory = url_factory

        page_count = self.__get_page_count()

        data = list()
        index = list()

        for page_number in page_count:
            self.url_factory.update_args(f810_pagenumber=page_number)
            month_url_list = self._get_month_url_list(url_factory=self.url_factory)

            for month_url in month_url_list:
                month_data = self._get_month_data(month_url=month_url)
                month_datetime = self._get_month_datetime(month_url=month_url)

                if len(month_data.keys()) < 10:
                    # попалась страница с лишней информацией, хз как иначе их фильтровать
                    continue

                # print(f'({month_url}) {month_datetime}: {month_data}')

                data.append(month_data)
                index.append(month_datetime)

        return data, index

    def _get_month_url_list(self, url_factory: URLFactory) -> list[URL]:
        soup = BeautifulSoup(self.response.text, self.engine)

        links = [url_factory.base_url + a['href'] for a in soup.find_all('a', class_='search-results__heading')]

        return links

    def _get_month_data(self, month_url) -> dict:
        response = requests.get(month_url, headers=self.__headers)
        soup = BeautifulSoup(response.text, self.engine)

        text = soup.text

        result = self.data_parser.parse_values(text)

        return result

    def _get_month_datetime(self, month_url) -> str:
        response = requests.get(month_url, headers=self.__headers)
        soup = BeautifulSoup(response.text, self.engine)

        date = soup.find('span', class_="text-red").text

        return date

    def __get_page_count(self) -> Iterable[int]:
        soup = BeautifulSoup(self.response.text, self.engine).find_all('a', class_='pager__link')

        n = 1 if not soup else int(soup[-1].text)

        return range(1, n + 1)

