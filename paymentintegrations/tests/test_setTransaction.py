import os
import random
import unittest

from suds.client import Client
from suds.sax.attribute import Attribute
from suds.sax.element import Element
from suds.wsse import UsernameToken

import pdb;pdb.set_trace()
CWD = os.getcwd()
XML_PATH = os.path.join(CWD, os.path.sep.join(__file__.split('/')[:-1]))
WSDL_URL = 'https://staging.payu.co.za/service/PayUAPI?wsdl'

class TestsetTransaction(unittest.TestCase):
    
    def test_advanced_RPP_setTransaction(self):
        file_path = os.path.join(XML_PATH, 'xml', 'set_transaction_advanced_redirect_page.xml')
        xml_file = open(file_path, 'rb')
        xml_template = xml_file.read()
        xml_file.close()
        
        details = dict(
            safekey = '{45D5C765-16D2-45A4-8C41-8D6F84042F8C}',
            transaction_type = 'PAYMENT',
            stage = 'true',
            cancel_url = 'http://www.example.com/cancel',
            demo_mode = 'true',
            merchant_ref = random.randrange(1,10+1),
            notification_url = 'http://www.example.com/notify',
            return_url = 'http://www.example.com/return',
            secure3d = 'false',
            supported_payments = 'CREDITCARD',
            show_budget = 'true',
            merchant_user_id = '7',
            customer_email = 'jane@example.com',
            customer_firstname = 'Jane',
            customer_lastname = 'Doe',
            customer_mobile = '2700000000',
            customer_regional_id = '1234567890',
            customer_country_code = '27',
            basket_amount = '1000',
            basket_currency_code = 'ZAR',
            basket_description = 'Basket description',
            loyalty_amount = '999',
            loyalty_information = 'Loyalty info',
            loyalty_membership_number = '12345',
            merhant_id = '11111111',
        )

        xml = xml_template.format(**details)

        client = Client(WSDL_URL)

    def test_setTransaction(self):
        file_path = os.path.join(XML_PATH, 'xml', 'set_transaction_with_fraud_check.xml')
        xml_file = open(file_path, 'rb')
        xml_template = xml_file.read()
        xml_file.close()

        xml = xml_template.format(
            username = 'Staging Integration Store 1',
            password = '78cXrW1W',
            safekey = '{45D5C765-16D2-45A4-8C41-8D6F84042F8C}',
            merchant_ref = random.randrange(1,10+1),
            cancel_url = 'http://example.com/cancel',
            notification_url = '',
            return_url = 'http://example.com/return',
            customer_email = 'jane@example.com',
            customer_firstname = 'Jane',
            customer_lastname = 'Doe',
            customer_mobile = '27840000000',
            basket_amount = '10000',
            basket_currency_code = 'ZAR',
            basket_description = 'Test basket',
            product_lineitem_amount = '10000',
            product_lineitem_cost = '10000',
            product_lineitem_description = 'Test item',
            product_lineitem_giftmessage = 'Test gift message',
            product_lineitem_productcode = '999',
            product_lineitem_quantity = '1',
            product_lineitem_address = '1 First Aven.',
            product_lineitem_city = 'First city',
            product_lineitem_country_code = '27',
            product_lineitem_postal_code = '0000',
            product_lineitem_firstname = 'Jane',
            product_lineitem_lastname = 'Doe',
            shipping_details_address = '1 First Aven.',
            shipping_details_city = 'First city',
            shipping_details_email = 'jane@example.com',
            shipping_details_country_code = '27',
            shipping_details_method = 'P',
            shipping_details_firstname = 'Jane',
            shipping_details_lastname = 'Doe',
            shipping_details_fax = '27000000000',
            shipping_details_phone = '27000000000',
            check_fraud_override = 'false',
            check_fraud_merchant_website = 'www.example.com',
            check_fraud_pc_fingerprint = 'asdfasdfsdfasdfasdf',
        )

if __name__ == '__main__':
    unittest.main()
