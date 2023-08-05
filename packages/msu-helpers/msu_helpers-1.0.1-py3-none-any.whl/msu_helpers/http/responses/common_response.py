#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import TypeVar, Generic
from django.http.response import JsonResponse
from ..http_constants import Status, Code

T = TypeVar('T')
BASIC_TYPES = ['list', 'str', 'dict', 'int', 'float', 'tuple', 'bool', 'NoneType']


class CommonResponse(Generic[T]):

    def __init__(self, data: T, status: str = Status.SUCCESS, code: int = Code.SUCCESS, message: str = None):
        self.status: str = status
        self.code: int = code
        self.message: str = message
        self.data: T = data

    @property
    def serialized(self) -> dict:
        return self._serialize()

    def _serialize(self) -> dict:
        if type(self.data).__name__ in BASIC_TYPES:
            data = self.data
        else:
            try:
                data = self.data.serialized
            except AttributeError:
                raise TypeError('Data should be serializable object or should have implemented property "serialized"')
        return {
            'status': self.status,
            'code': self.code,
            'message': self.message,
            'data': data,
        }

    @property
    def json_response(self) -> JsonResponse:
        return JsonResponse(self.serialized)

    @classmethod
    def success(cls, data: T = None, code: int = Code.SUCCESS, message: str = None):
        return CommonResponse(data, Status.SUCCESS, code, message)

    @classmethod
    def failed(cls, code: int = Code.FAILED, message: str = None):
        return CommonResponse(None, Status.FAILED, code, message)

    @classmethod
    def not_found(cls):
        return CommonResponse(None, Status.FAILED, Code.NOT_FOUND, 'Not Found')

    @classmethod
    def unauthorized(cls):
        return CommonResponse(None, Status.FAILED, Code.UNAUTHORIZED, 'Unauthorized')

    @classmethod
    def forbidden(cls):
        return CommonResponse(None, Status.FAILED, Code.FORBIDDEN, 'Forbidden')

    @classmethod
    def server_error(cls):
        return CommonResponse(None, Status.FAILED, Code.INTERNAL_SERVER_ERROR, 'Internal server error')
