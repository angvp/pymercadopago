'''
Created on Sep 11, 2012

@author: diego
'''
import unittest
from pymercadopago import Mercadopago , NoAccessTokenError, UndefinedResponseError



class PyMercadopagoTest(unittest.TestCase):


    def setUp(self):
            
        data = {
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
        self.data = data
        self.client_id = 3805
        self.client_secret = 'PwZ6B94AlYdOYyJ4xWr2Rl87tVPPeIlw'



    def testAccessToken(self):
        try:
            mp = Mercadopago(self.client_id,self.client_secret)
        except NoAccessTokenError :
            self.fail("No Access Token")
        except UndefinedResponseError :
            self.fail("Bad response")

    def tearDown(self):
        pass

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    
    
    """
# Comienzo de la implementacion
"""
"""

if __name__ == '__main__':


    clientID = 3803
    clientSecret = 'PwZ6B94AlYdOYyJ4xWr2Rl87tVPPeIlw'
    mp = Mercadopago(clientID, clientSecret)
    access_token = mp.get_access_token()

    if access_token:
        preference = mp.create_preference(data, access_token)
        if preference:
            print "Preferencia creada con exito: " + preference["init_point"]
        else:
            print "Error creando la preferencia"
    else:
        print "Error al obtener el access token"
"""