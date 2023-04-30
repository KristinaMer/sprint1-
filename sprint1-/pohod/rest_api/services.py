import io
from enum import Enum

from rest_framework.parsers import JSONParser
from .serializers import UserTouristSerializer



class PerevalData:
    def __init__(self, data_in):
        self.data_in_raw = data_in
        self.data_in_decode = {}
        self.status = 0
        self.message = ''
        self.new_id = 0
        self.serializer = UserTouristSerializer()
        super().__init__()

    class ResultCode(Enum):
        Error = '500'
        BadRequest = '400'
        Succes = '200'

    def check_data(self):
        stream = io.BytesIO(bytes(self.data_in_raw))
        data = JSONParser().parse(stream)
        if not self.serializer.is_valid():
            self.status = self.ResultCode.BadRequest.value
            self.message = f'Bad request - {self.serializer.errors}'
            self.new_id = 'Null'
            return False
        self.data_in_decode = self.serializer.validated_data
        return True

    def submit_data(self):
        pass

    def format_result(self):
        pass

    def get_email(self, email):
        pass
















