'''
Created on Sep 11, 2012

@author: diego
'''
import unittest
from pyMercadopago import PyMercadopagoHandler, NoAccessTokenError, UndefinedResponseError,\
    Order, Item, Payer, Back_Urls
from urlparse import urlparse


class PyMercadopagoTest(unittest.TestCase):

    data = ''

    def setUp(self):

        self.client_id = 12823
        self.client_secret = '4zDgtKDKzC2krZw7FplnYVhTWbWkEMM0'
        self.mercadopagoHandler = None

    def test_AccessToken(self):
        try:
            self.mercadopagoHandler = PyMercadopagoHandler(self.client_id, self.client_secret)
        except NoAccessTokenError:
            self.fail("No Access Token")
        except UndefinedResponseError:
            self.fail("Bad response creating token")

        self.assertTrue(len(self.mercadopagoHandler.access_token) == 63, "Invalid token size!!")

    def testListOrderCreation(self):
        #batchMode
        mpHandler = PyMercadopagoHandler(self.client_id, self.client_secret)
        orders = list()

        order = Order(externalReference="OP1234", internalId='1ZQM2', collectorId='5879');
        item = Item(title='Cuadro con Mother', quantity=100, unitPrice=520, currencyId='ARS')
        item.picture_url = "https://www.mercadopago.com/org-img/MP3/home/logomp3.gif"
        item.id = "12345"
        item.description = "esta es la descripcion que quiero mandar con el producto"
        order.addItem(item)

        payer = Payer() #TODO factory for this
        order.addPayer(payer)

        back_urls = Back_Urls()
        back_urls.pending = "http://www.pending.com"
        back_urls.success = "http://www.success.com"
        order.back_urls = back_urls

        orders.append(order)
        mpHandler.pushOrders(orders)
        print mpHandler.result

    def tearDown(self):
        pass

if __name__ == "__main__":
    import sys; sys.argv = ['', 'Test.testName']
    unittest.main()
