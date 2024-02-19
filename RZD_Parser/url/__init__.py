from dataclasses import dataclass, field
from datetime import datetime

from RZD_Parser.url import attribute_parser


@dataclass
class URLFactory:
    """
    Requires all the necessary information to build a request query to get data
    from the Russian Railways website (https://company.rzd.ru/)


    f810_pagesize: int - size of pages
    f810_pagenumber: int - number of page
    date_publication_0: str | datetime - data start time
    date_publication_1: str | datetime - data end time (default the present moment)
    rubricator_id: int - ... (deafult 57)
    text_search: str = 'погрузка на сети'
    date_re - regular expression for a date_publication
    """

    f810_pagesize: int
    text_search: str
    rubricator_id: int
    date_publication_0: str | datetime
    date_publication_1: str | datetime
    f810_pagenumber: int = 1
    url: str = field(init=False)
    date_re = r'^\d{2}\.\d{2}\.\d{4}$'

    def update_parameters(self):
        """Updates the parameters"""

        self.__post_init__()

    def __post_init__(self):
        self.date_publication_0 = attribute_parser.parse_date_publication(self.date_publication_0, self.date_re)
        self.date_publication_1 = attribute_parser.parse_date_publication(self.date_publication_1, self.date_re)
        self.rubricator_id = attribute_parser.parse_rubricator_id(self.rubricator_id)
        self.text_search = attribute_parser.parse_text_search(self.text_search)

        self.text_search = self.text_search.replace(' ', '+')

        self.url = f'https://company.rzd.ru/ru/9397/page/13307?' \
                   f'f810_pagesize={self.f810_pagesize}&' \
                   f'&date_publication_0={self.date_publication_0}' \
                   f'&date_publication_1={self.date_publication_1}' \
                   f'&rubricator_id={self.rubricator_id}' \
                   f'&text_search={self.text_search}' \
                   f'&f810_pagenumber={self.f810_pagenumber}'
