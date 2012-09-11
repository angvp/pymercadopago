#!/usr/bin/python
"""
Mercadopago Class:
==================

This class is intended to be used as simplifier of handling several http
connections to the mercadopago payment gateway.

Feel free to modify this code and improve it, this is licenced by GPL v2

More information about GPL License: http://www.gnu.org/licenses/gpl-2.0.html

Angel 'angvp' Velasquez <angvp@archlinux.org>

"""
import requests
import json


class NoAccessTokenError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Mercadopago:

    def __init__(self, client_id, client_secret):
        self.url_base = 'https://api.mercadolibre.com'
        self.url_oauth_token = "%s/oauth/token" % self.url_base
        self.url_preference = "%s/checkout/preferences?access_token=" % self.url_base
        self.url_status_preference = "%s/checkout/preferences/ping" % self.url_base
        self.client_id = client_id
        self.client_secret = client_secret
        self.pending_url = ''
        self.succes_url = ''
        self.payments = []
        self.access_token = self.get_access_token()

        if not self.access_token:
            raise NoAccessTokenError('gil')

    def add_pending(self, url):
        self.pending_url = url

    def add_succesful(self, url):
        self.successful = url

    def add_payment(self, payment):
        pass

    def post_data(self, data, rcode, url, type):
        if type == 'json':
            headers = {'Content-type': 'application/json',
                    'Accept': 'application/json'}
            data = json.dumps(data)
        else:
            headers = {'Content-type': 'application/x-www-form-urlencoded',
                    'Accept': 'application/json'}
        r = requests.post(url, data=data, headers=headers)
        if r.status_code == rcode:
            return r.content
        print(r.content)
        return False

    def get_access_token(self):
        data = {
                'grant_type': 'client_credentials',
                'client_id': self.client_id,
                'client_secret': self.client_secret
                }
        url = self.url_oauth_token
        response = self.post_data(data, 200, url, 'text')
        if response:
            resp_dict = json.loads(response)
            return resp_dict['access_token']
        return False

    def get_or_create_item(self, data, access_token):
        url = "%s%s" % (self.url_preference, access_token)
        rcode = 201
        preference = self.post_data(data, rcode, url, 'json')
        if preference:
            return json.loads(preference)
        return False
