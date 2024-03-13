import urllib
from datetime import datetime
from dataclasses import dataclass, field

from RZD_Parser.url import attribute_parser


@dataclass
class URLFactory:
    """
    Requires all the necessary information to build a request query to get data
    from the Russian Railways website (https://company.rzd.ru/)


    date_publication_0: str | datetime - data start time
    date_publication_1: str | datetime - data end time (default the present moment)

    rubricator_id: int - ... (deafult 57)
    f810_pagesize: int - size of pages
    f810_pagenumber: int - number of page
    text_search: str = 'погрузка на сети'
    date_re - regular expression for a date_publication
    """

    date_publication_0: str | datetime
    date_publication_1: str | datetime

    rubricator_id: int = 57
    text_search: str = 'погрузка на сети'
    f810_pagesize: int = 10000
    f810_pagenumber: int = 1

    base_url: str = 'https://company.rzd.ru'
    url: str = field(init=False)
    date_re = r'^\d{2}\.\d{2}.\d{4}$'

    def update_url(self):
        self.url = self.base_url + '/ru/9397/page/13307?' + \
                   f'f810_pagesize={self.f810_pagesize}' \
                   f'&date_publication_0={self.date_publication_0}' \
                   f'&date_publication_1={self.date_publication_1}' \
                   f'&rubricator_id={self.rubricator_id}' \
                   f'&text_search={self.text_search}' \
                   f'&f810_pagenumber={self.f810_pagenumber}'

    def __post_init__(self):
        # Date publication validation
        self.date_publication_0 = attribute_parser.parse_date_publication(self.date_publication_0, self.date_re)
        self.date_publication_1 = attribute_parser.parse_date_publication(self.date_publication_1, self.date_re)

        self.update_url()

    def update_args(self, **kwargs):
        """Updates the parameters"""

        self.__dict__.update(kwargs)
        self.update_url()

