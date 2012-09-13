#!/usr/bin/python
"""
PyMercadopagoHandler Class:
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

class UndefinedResponseError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class PyMercadopagoHandler:
    
    orders = list()
    notifications = list() 

    def __init__(self, client_id, client_secret):
        self.url_base = 'https://api.mercadolibre.com'
        self.url_oauth_token = "%s/oauth/token" % self.url_base
        self.url_preference = "%s/checkout/preferences?access_token=" % self.url_base
        self.url_status_preference = "%s/checkout/preferences/ping" % self.url_base
        self.client_id = client_id
        self.client_secret = client_secret
        if self.client_id == '' or self.client_secret == '':
            raise NoAccessTokenError()
        
        self.access_token = self.get_access_token()

        if not self.access_token:
            raise NoAccessTokenError('gil')
        
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
        else:
            raise UndefinedResponseError(r)
        
        #Raisear error post data

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

    def get_or_create_item(self, data):
        url = "%s%s" % (self.url_preference, self.access_token)
        expectedOkStatus = 201
        preference = self.post_data(data, expectedOkStatus, url, 'json')
        if preference:
            return json.loads(preference)
        return False

    def pushOrders(self,orders):
            for order in orders:
                self.get_or_create(order.toJson())
        
    def __unicode__(self):
        return 'json: '
    def __str__(self):
        return 'json: '
    
class Order:
    
    items = None
    payer = None
    external_reference = ''
    suscription_plan_id = ''
    id = ''
    collector_id = ''
    init_point = ''
    expires = ''
    expiration_date_to = ''
    expiration_dato_from = ''
    back_urls = None
    
    def __init__(self,externalReference,internalId,collectorId):
        #At constructor should be all required fields.
        
        self.external_reference = externalReference 
        self.collector_id = collectorId
        self.id = internalId
        self.items = list()
        self.payer = Payer()
        
    def addItem(self,item):
        if self.items == None:
            self.items = list()
        
        self.items.append(item)
    
    def addPayer(self,payer):
        self.payer = payer
    
    def addSuccessUrl(self,url):
        if self.back_urls == None:
            self.back_urls = Back_Urls
        self.back_ulrs.success = url 
    
    def addPendingUrl(self,url):
        if self.back_urls == None:
            self.back_urls = Back_Urls()
        self.back_ulrs.pending = url

    def toJson(self):
        return json.dump(self)
    
class Item:
    
    id = ''
    title = ''
    descripcion = ''
    quantity = 0
    unit_price = 0
    currency = ''
    picture_url = ''
    
    def __init__(self, title):
        
class Payer:
    name = ''
    surname = '' 
    email = ''

class Back_Urls:
    pending = ''
    success = ''