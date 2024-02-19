from .base_exception import RZDException


class RZhDBadRequest(RZDException):
    def __init__(self, status_code, message):
        super().__init__(f'Bad request with status code: {status_code}, and message: {message}')


class RZDConnectionError(RZDException):
    def __init__(self, url):
        super().__init__(f"Can't connect to the server: {url}")
