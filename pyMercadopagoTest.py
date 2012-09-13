'''
Created on Sep 11, 2012

@author: diego
'''
import unittest
from pymercadopago import Mercadopago , NoAccessTokenError, UndefinedResponseError,\
    Order, Item, Payer
from urlparse import urlparse

class PyMercadopagoTest(unittest.TestCase):
    
    data = ''
    def setUp(self):
            
        """        data = {
                    "external_reference": "OP1234",
                    "payer": {
                        "name": "user",
                        "surname": "test",
                        "email": ""
                    },
                    "items": [{
                        "id": "Codigo de item",
                        "title": "item de testeo",
                        "description": "Oferton",
                        "quantity": 1,
                        "unit_price": 50,
                        "currency_id": "ARS",
                        "picture_url":
                        "http://www.mercadolibre.com.ar/jm/img?s=MLA&f=101426566_5989.jpg&v=E"
                    }],
                    "payment_methods": {
                        "excluded_payment_types": [{"id": "ticket"}],
                        "excluded_payment_methods": [{"id": "master"}],
                        "installments": 1
                    },
                    "back_urls": {
                        "pending": "https://www.pending.com",
                        "success": "https://www.success.com"
                    }
                }
        """        
        self.client_id = 12823
        self.client_secret = '4zDgtKDKzC2krZw7FplnYVhTWbWkEMM0'
        self.mercadopagoHandler = None



    def test_AccessToken(self):
        try:
            self.mercadopagoHandler = Mercadopago(self.client_id,self.client_secret)
        except NoAccessTokenError :
            self.fail("No Access Token")
        except UndefinedResponseError :
            self.fail("Bad response creating token")

        self.assertTrue(len(self.mercadopagoHandler.access_token)==63, "Invalid token size!!")
    
    def test_CreateItem(self):
        try:
            self.mercadopagoHandler = Mercadopago(self.client_id,self.client_secret)
            item = self.mercadopagoHandler.get_or_create_item(self.data)
            
            #it should verify init_point property contains a valid url
            validator = urlparse( item['init_point']  )
            print validator.scheme
            print validator.netloc
            print validator.path
            print validator.query
            if validator.scheme == '' or validator.netloc == '' or validator.path == '' or validator.query == '':
                self.fail("Invalid init point generated!!") 
            
        except NoAccessTokenError :
            self.fail("No Access Token")
        except UndefinedResponseError :
            self.fail("Bad response creating item")
        

    def testOrderCreation(self):
        
        #simple User case
        mpHandler = Mercadopago(self.client_id,self.client_secret)
        
        order = Order();
        item = Item() #TODO should be a factory && populate properties in the constructor
        order.addItem(item)
        
        payer = Payer() #TODO factory for this
        order.addPayer(payer)
        
        mpHandler.pushOrder(order)
        
        pass
    
    def testListOrderCreation(self):
        pass
    
    def testOrderMethods(self):
        order = Order()
        order.toJson()    
            

    def tearDown(self):
        pass

if __name__ == "__main__":
    import sys;sys.argv = ['', 'Test.testName']
    unittest.main()