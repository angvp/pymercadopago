'''
pymercadopago tests
@authors: diego, angvp
'''
import unittest
from urlparse import urlparse

from api import *
from mpexceptions import *

class PyMercadopagoTest(unittest.TestCase):

    data = ''

    def setUp(self):

        self.client_id = 12823
        self.client_secret = '4zDgtKDKzC2krZw7FplnYVhTWbWkEMM0'
        self.mercadopago_handler = None

    def test_access_token(self):
        try:
            self.mercadopago_handler = Handler(self.client_id,
                                               self.client_secret)
        except NoAccessTokenError:
            self.fail("No Access Token")
        except UndefinedResponseError:
            self.fail("Bad response creating token")

        self.assertTrue(self.mercadopago_handler.access_token.startswith('APP'),
                        "Invalid token size!!")

    def test_create_preference(self):

        result_dummie = {'collector_id': '1234',
                         'init_point': 'http://www.mercadolibre.com.ar/path',
                         'expiration_date_from': '2012-02-29',
                         'back_urls': {'pending': "http://www.pending.com",
                         'success': 'http://www.success.com'},
                         'date_created': "2012-02-29",
                         'subscription_plan_id': '23', 'id': 1234,
                         'expires': '2012-03-21',
                         'expiration_date_to': '2012-03-21',
                         'external_reference': 'OP1234',
                         'payer': {'name': 'Diego', 'surname': 'darkipunchi'},
                         'items': {'title': 'Cuadro con Mother',
                                   'quantity': 10, 'unit_price': 50,
                                   'currency_id': 'ARS'}}
        preference = MPPreference(result_dummie)
        self.assertFalse(preference == None, "Error creating preference")

    """
    # In order to run this method you should provide an appropiate client_id
    # and client_secret and id_payment that belongs that ML account
    def test_get_payment(self):
        mp_handler = Handler(self.client_id, self.client_secret)
        result = mp_handler.get_payment(<insert_an_id_payment_here>)
        self.assertFalse(result == False, "Error getting the payment id)
    """

    def test_list_order_creation(self):
        #batchMode
        mp_handler = Handler(self.client_id, self.client_secret)
        orders = list()

        order = MPOrder(external_reference="OP1234", internal_id='1ZQM2',
                      collector_id='5879')
        item = MPItem(title='Cuadro con Mother', quantity=100, unit_price=520,
                     currency_id='ARS')
        item.picture_url = "http://docs.python.org/_static/py.png"
        item.id = "12345"
        item.description = "descripcion que quiero mandar"
        order.add_item(item)

        payer = MPPayer()
        payer.name = 'Angel'
        payer.surname = 'Velasquez'
        payer.email = 'angel@bixti.com'
        order.add_payer(payer)

        back_urls = MPBackUrls()
        back_urls.pending = "http://www.pending.com"
        back_urls.success = "http://www.success.com"
        order.back_urls = back_urls

        orders.append(order)
        mp_handler.push_orders(orders)

        self.assertFalse(mp_handler.result == None,
                          "Getting MercadoPago results Failed ")
        #Url element will be verified for valid url string
        for preference in mp_handler.result:
            print preference
            parsed = urlparse(preference.init_point)
            self.assertTrue(parsed.scheme != '' or parsed.netloc != '' or
                             parsed.path != '' or parsed.query != '',
                              'Error validating result url')

    def test_exclude_payment_method(self):
        exclude_payment_methods = {"id": "visa", "name": "Visa",
        "payment_type_id": "credit_card",
        "thumbnail": "http://img.mlstatic.com/org-img/MP3/API/logos/visa.gif",
        "secure_thumbnail": "https://www.mercadopago.com/org-img/MP3/API/logos/visa.gif"}
        exclude_payment_types = {}

    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()
