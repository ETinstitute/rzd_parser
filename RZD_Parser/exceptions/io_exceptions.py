import os

from .base_exception import RZDException


class RZDFileNotFound(RZDException):
    project_path = os.getcwd()

    def __init__(self, file_path):
        super().__init__(f'CSV file not found at the specified path: {os.path.join(self.project_path, file_path)}')


class RZDDataFrameNotCreatedError(RZDException):
    def __init__(self):
        super().__init__('DataFrame has not been created. Please call the parse() method to create the DataFrame.')
