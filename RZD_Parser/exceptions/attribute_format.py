from .base_exception import RZDException


class RZDInvalidDateFormat(RZDException):
    def __init__(self, date):
        super().__init__(f'Invalid date format: {date}. Please use DD.MM.YYYY')


class RZDTypeError(RZDException):
    def __init__(self, date):
        super().__init__(f"Date publication should be either a string or a datetime object, implemented: {type(date) = }")
