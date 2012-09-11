# -*- coding: utf-8 -*-
"""
MercadoPago utils
"""

import urllib2
import urllib
import json

"""
Some settings
"""


class Mercadopago:

    def __init__(self, client_id, client_secret):
        self.url_base = 'https://api.mercadolibre.com'
        self.url_oauth_token = "%s/oauth/token" % self.url_base
        self.url_preference = "%s/checkout/preferences?access_token=" % self.url_base
        self.url_status_preference = "%s/checkout/preferences/ping" % self.url_base
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = self.get_access_token()


    def post_json(self, data, rcode, url):
        return self.post_data_type(data, rcode, url, 'json')


    def post_data(self, data, rcode, url):
        return self.post_data_type(data, rcode, url, 'text')


    def post_data_type(self, data, rcode, url, type):
        if type == 'json':
            headers = {"Content-type": "application/json",
                    "Accept": "application/json"}
            data = json.dumps(data)
        else:
            headers = {"Content-type": "application/x-www-form-urlencoded",
                    "Accept": "application/json"}
            data = urllib.urlencode(data)

        req = urllib2.Request(url, data, headers)
        response_stream = urllib2.urlopen(req)
        response = json.loads(response_stream.read())
        return response


    def get_access_token(self):
        data = {
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret
                }
        url = self.url_oauth_token
        response = self.post_data(data, 200, url)
        if 'error' not in response:
            return response['access_token']
        Return None


    def check_status_preference():
        url = self.url_status_preference
        req = urllib2.Request(url)
        req.add_header('Accept', 'application/json')
        response_stream = urllib2.urlopen(req)
        response = json.loads(response_stream.read())
        if "error" not in response:
            return True
        return False


    def create_preference(self, data, access_token):
        url = "%s%s" % (self.url_preference, access_token)
        rcode = 201
        return self.post_json(data, rcode, url)


    def get_mp_url(self, data, access_token):
        preference = self.create_preference(data, access_token)
        return preference['init_point']


