'''
Created on Sep 11, 2012

@author: diego
'''
import unittest
from py_mercadopago import PyMercadopagoHandler, NoAccessTokenError, UndefinedResponseError,\
    Order, Item, Payer, Back_Urls, Preference
from urlparse import urlparse


class PyMercadopagoTest(unittest.TestCase):

    data = ''

    def setUp(self):

        self.client_id = 12823
        self.client_secret = '4zDgtKDKzC2krZw7FplnYVhTWbWkEMM0'
        self.mercadopago_handler = None

    def test_access_token(self):
        try:
            self.mercadopago_handler = PyMercadopagoHandler(self.client_id,
                                                            self.client_secret)
        except NoAccessTokenError:
            self.fail("No Access Token")
        except UndefinedResponseError:
            self.fail("Bad response creating token")

        self.assertTrue(len(self.mercadopago_handler.access_token) == 63,
                        "Invalid token size!!")

    def test_create_preference(self):
        preference = Preference(collector_id='12344',
                                init_point='url',
                                expiration_date_from='date string',
                                back_urls='"back_urls":{}',
                                date_created='date string',
                                subscription_plan_id='string',
                                id='valor retornado por MP',
                                expires='string date',
                                expiration_date_to='date string',
                                external_reference='string date',
                                payer='"payer":{}',
                                items='"items":[{}]')
        self.assertFalse(preference == None, "Error creating preference")

    def test_list_order_creation(self):
        #batchMode
        mp_handler = PyMercadopagoHandler(self.client_id, self.client_secret)
        orders = list()

        order = Order(external_reference="OP1234", internal_id='1ZQM2',
                      collector_id='5879')
        item = Item(title='Cuadro con Mother', quantity=100, unit_price=520,
                     currency_id='ARS')
        item.picture_url = "https://www.mercadopago.com/org-img/MP3/home/logomp3.gif"
        item.id = "12345"
        item.description = "esta es la descripcion que quiero mandar con el producto"
        order.add_item(item)

        payer = Payer()     # TODO factory for this
        order.add_payer(payer)

        back_urls = Back_Urls()
        back_urls.pending = "http://www.pending.com"
        back_urls.success = "http://www.success.com"
        order.back_urls = back_urls

        orders.append(order)
        mp_handler.push_orders(orders)
        print mp_handler.result
        self.assertFalse(mp_handler.result == None,
                          "Get MercadoPago result Failed ")
        for preference in mp_handler.result:
            print preference

    def tearDown(self):
        pass

if __name__ == "__main__":
    import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
