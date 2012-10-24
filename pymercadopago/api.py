#!/usr/bin/python
"""
PyMercadopagoHandler Class:
==================
"""
from mpexceptions import *

import requests
import json
import time


class Handler:

    orders = list()
    notifications = list()
    TOKEN_GENERATION_STATUS_EXPECTED = 200
    CREATE_ITEM_STATUS_EXPECTED = 201
    NOTIFICATION_STATUS_EXPECTED = 200
    result = None
    authenticated = False
    access_token = False

    def __init__(self, client_id, client_secret):
        self.url_base = 'https://api.mercadolibre.com'
        self.url_oauth_token = "%s/oauth/token" % self.url_base
        self.url_preference = "%s/checkout/preferences?access_token=" \
            % self.url_base

        self.url_status_preference = "%s/checkout/preferences/ping" \
            % self.url_base

        self.url_payment_info = "%s/collections/notifications" % self.url_base

        self.client_id = client_id
        self.client_secret = client_secret
        if self.client_id == '' or self.client_secret == '':
            raise EmptyCredentialsError()

        if not self.authenticated:
            self.get_access_token()

        if not self.access_token:
            raise NoAccessTokenError()

        self.result = list()

    def post_data(self, data, rcode, url, utype):
        if utype == 'json':
            headers = {'Content-type': 'application/json',
                       'Accept': 'application/json'}
            data = json.dumps(data)
        else:
            headers = {'Content-type': 'application/x-www-form-urlencoded',
                       'Accept': 'application/json'}

        if data is not None:
            r = requests.post(url, data=data, headers=headers)
        else:
            r = request.post(url, headers=headers)
        if r.status_code == rcode:
            return r.content
        else:
            raise UndefinedResponseError(r)

    def get_access_token(self):
        data = {'grant_type': 'client_credentials',
                'client_id': self.client_id,
                'client_secret': self.client_secret}
        url = self.url_oauth_token
        response = self.post_data(data, self.TOKEN_GENERATION_STATUS_EXPECTED,
                                  url, 'text')
        if response:
            resp_dict = json.loads(response)
            self.access_token = resp_dict['access_token']
            self.authenticated = True
            self.authentication_time = time.time()
            self.authentication_expires = resp_dict['expires_in']

    def authenticate(func):
        def wrapped(self, data):
            auth_dif = time.time() - self.authentication_time
            if not self.authenticated or auth_dif < self.authentication_expires:
                self.get_access_token()
            return func(self, data)

        return wrapped

    @authenticate
    def get_or_create_item(self, data):
        url = "%s%s" % (self.url_preference, self.access_token)
        preference = self.post_data(data, self.CREATE_ITEM_STATUS_EXPECTED,
                                    url, 'json')
        if preference:
            return json.loads(preference)
        return False

    def push_orders(self, orders):
        for order in orders:
            result = self.get_or_create_item(order.to_dict())
            self.result.append(MPPreference(result))

    @authenticate
    def get_payment(self, data):
        url = "%s/%s?access_token=%s" % (self.url_payment_info, data, self.access_token)
        payment = self.post_data(None, self.NOTIFICATION_STATUS_EXPECTED,
                                 url, 'json')
        if payment:
            return json.loads(payment)
        return False


class MPOrder:
    items = None
    payer = None
    external_reference = ''
    suscription_plan_id = ''
    id = ''
    collector_id = ''
    init_point = ''
    expires = ''
    expiration_date_to = ''
    expiration_date_from = ''
    back_urls = None

    def __init__(self, external_reference, internal_id, collector_id):
        #At constructor should be all required fields
        self.external_reference = external_reference
        self.collector_id = collector_id
        self.id = internal_id
        self.items = list()
        self.payer = MPPayer()

    def add_item(self, item):
        if self.items is None:
            self.items = list()

        self.items.append(item)

    def add_payer(self, payer):
        self.payer = payer

    def add_successUrl(self, url):
        if self.back_urls is None:
            self.back_urls = MPBackUrls
        self.back_urls.success = url

    def add_pending_url(self, url):
        if self.back_urls is None:
            self.back_urls = MPBackUrls()
        self.back_urls.pending = url

    def to_dict(self):
        value = {}
        value['external_reference'] = self.external_reference
        items = []
        item_dict = {}
        for item in self.items:
            if item.id != '':
                item_dict['id'] = item.id
            if item.description != '':
                item_dict['description'] = item.description
            if item.picture_url != '':
                item_dict['picture_url'] = item.picture_url
            item_dict['title'] = item.title
            item_dict['quantity'] = item.quantity
            item_dict['unit_price'] = item.unit_price
            item_dict['currency_id'] = str(item.currency_id)
            items.append(item_dict)
        value['items'] = items

        if self.payer is not None:
            payer = {}
            if self.payer.name != '':
                payer['name'] = self.payer.name
            if self.payer.surname != '':
                payer['surname'] = self.payer.surname
            if self.payer.email != '':
                payer['email'] = self.payer.email
            value['payer'] = payer
        if self.back_urls is not None:
            back_urls = {}
            back_urls['success'] = self.back_urls.success
            back_urls['pending'] = self.back_urls.pending
            value['back_urls'] = back_urls
        return value


class MPItem:
    id = ''
    title = ''
    description = ''
    quantity = 0
    unit_price = 0
    currency_id = ''
    picture_url = ''

    def __init__(self, title, quantity, unit_price, currency_id):
        self.title = title
        self.quantity = quantity
        self.unit_price = unit_price
        self.currency_id = currency_id


class MPPayer:
    name = ''
    surname = ''
    email = ''


class MPBackUrls:
    pending = ''
    success = ''


class MPPreference:
    collector_id = ''
    init_point = ''
    back_urls = None
    expiration_date_from = ''
    date_created = ''
    subscription_plan_id = ''
    id = ''
    expires = ''
    expiration_date_to = ''
    external_reference = ''
    payer = None
    items = None

    def __init__(
            self, result):
        self.collector_id = result['collector_id']
        self.init_point = result['init_point']
        self.back_urls = result['back_urls']
        self.expiration_date_from = result['expiration_date_from']
        self.date_created = result['date_created']
        self.subscription_plan_id = result['subscription_plan_id']
        self.id = result['id']
        self.expires = result['expires']
        self.expiration_date_to = result['expiration_date_to']
        self.external_reference = result['external_reference']
        self.payer = result['payer']
        self.items = result['items']

    def __repr__(self):
        return("Collector_id: %s Preference_id: %s Init_point: %s" %
                (str(self.collector_id), self.id, self.init_point))


class MPPaymentMethods:
    excluded_payment_types = ''
    excluded_payment_methods = ''
    installments = 0

    def __init__(self, excluded_payment_types, excluded_payment_methods,
                 installments):
        self.excluded_payment_types = excluded_payment_types
        self.excluded_payment_methods = excluded_payment_methods
        self.installments = installments
