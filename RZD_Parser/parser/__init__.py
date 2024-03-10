import pandas as pd
from typing import Union, Optional
from datetime import datetime

from RZD_Parser.exceptions.io_exceptions import RZDFileNotFound, RZDDataFrameNotCreatedError
from RZD_Parser.parser.html_utils import HTMLUtils
from RZD_Parser.url import URLFactory


class RZDParser:
    def __init__(self):
        """Parser for shipments data from the Russian Railways website

        Args:
            date_publication_0: the left boundary of time
            date_publication_1: the right boundary of time. Defaults to datetime.now().

        Methods:
            parse_data: parsing data and returns dataframe
            update_data: checking difference with your data and data in RZD site
        """

        self.url_factory = None
        self.html_utils = HTMLUtils()

        self.df = None

    def parse_data(
            self,
            date_publication_0: Union[str, datetime],
            date_publication_1: Union[str, datetime] = datetime.now()
    ) -> pd.DataFrame:

        """Returns pandas.DataFrame with the following data: shipments and dates"""
        self.url_factory = URLFactory(date_publication_0=date_publication_0, date_publication_1=date_publication_1)

        data, index = self.html_utils.get_data(url_factory=self.url_factory)

        self.df = pd.DataFrame(data=data, index=index)

        return self.df

    def update_data(self, csv_filepath: Optional[str] = None):
        if csv_filepath:
            try:
                self.df = pd.read_csv(csv_filepath, index_col='Unnamed: 0')
            except FileNotFoundError:
                raise RZDFileNotFound(file_path=csv_filepath)

        else:
            if self.df is None:
                raise RZDDataFrameNotCreatedError()

        self.url_factory = URLFactory(date_publication_0=self.df.index[0], date_publication_1=datetime.now())

        new_data, index = self.html_utils.get_data(url_factory=self.url_factory)
        new_data = pd.DataFrame(data=new_data, index=index)

        return pd.concat([new_data, self.df])
