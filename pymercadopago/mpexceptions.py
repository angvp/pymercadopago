# -*- coding: utf-8 -*-
"""
Mercadopago API exceptions.
"""


class NoAccessTokenError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class UndefinedResponseError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class EmptyCredentialsError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class ExpiredAuthenticationError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

