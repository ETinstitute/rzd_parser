"""
Validate and parse attributes in initialization

"""


import re
from datetime import datetime

from RZD_Parser.exceptions import (
    RZDInvalidDateFormat,
    RZDTypeError
)


def parse_date_publication(date_publication, date_re):
    """
    Parse date publication.

    If the date_publication is a string, it will check that it is in the format DD.MM.YYYY
    """

    if isinstance(date_publication, str):
        # TODO: сделать так, чтобы даты позже настоящего момента не принимались
        if re.match(date_re, date_publication):
            return date_publication
        raise RZDInvalidDateFormat(date_publication)

    elif isinstance(date_publication, datetime):
        return f'{date_publication.day:02}.{date_publication.month:02}.{date_publication.year}'
    raise RZDTypeError(date_publication)


def parse_rubricator_id(rubricator_id):
    """Will be implemented in the future"""
    return rubricator_id


def parse_text_search(text_search):
    return text_search.replace(' ', '+')
