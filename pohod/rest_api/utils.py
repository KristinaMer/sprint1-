from rest_framework.exceptions import APIException


class EncodeException(APIException):
    status_code = 500
    default_detail = 'Image error'


class DatabaseException(APIException):
    status_code = 500
    default_detail = 'Database error'


class ObjectException(APIException):
    status_code = 403
    default_detail = 'Object error'




