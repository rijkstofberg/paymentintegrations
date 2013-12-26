##############################################################################
#
# Copyright (c) 2013 Rijk Stofberg
# All Rights Reserved.
#
# This software is subject to the provisions of the MIT License (MIT),
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
# 
#
##############################################################################

from traceback import print_exc

from suds.client import Client
from suds.xsd.doctor import Import, ImportDoctor
from suds.sax.attribute import Attribute
from suds.sax.element import Element
from suds.wsse import UsernameToken, Security
import logging


WSDL_URL =   'https://staging.payu.co.za/service/PayUAPI?wsdl'
SOAP_ENC_URI = 'http://www.w3.org/2003/05/soap-encoding'

OASIS_BASE = 'http://docs.oasis-open.org/wss/2004/01/'
WSU_URI  =    OASIS_BASE + 'oasis-200401-wss-wssecurity-utility-1.0.xsd'
WSU_UN_URI =  OASIS_BASE + 'oasis-200401-wss-username-token-profile-1.0#PasswordText'
WSSE_URI   =  OASIS_BASE + 'oasis-200401-wss-wssecurity-secext-1.0.xsd'
SOAP_ENC_URI = 'http://www.w3.org/2003/05/soap-encoding'

WSSE_NS    = ('wsse', WSSE_URI)
WSSE_XMLNS = ('xmlns:wsse', WSSE_URI)
WSU_NS  = ('wsu', WSU_URI)
WSU_XMLNS  = ('xmlns:wsu', WSU_URI)
SOAP_ENC_NS = ('SOAP-ENC', SOAP_ENC_URI)


class PayU_Security(Security):
    """
    WS-Security object.
    @ivar tokens: A list of security tokens
    @type tokens: [L{Token},...]
    @ivar signatures: A list of signatures.
    @type signatures: TBD
    @ivar references: A list of references.
    @type references: TBD
    @ivar keys: A list of encryption keys.
    @type keys: TBD
    """
    
    def __init__(self):
        """
        """
        Security.__init__(self)
        self.mustUnderstand = 1
        self.nsprefixes = {}
        
    def addPrefix(self, p, u):
        """
        Add or update a prefix mapping.
        @param p: A prefix.
        @type p: basestring
        @param u: A namespace URI.
        @type u: basestring
        @return: self
        @rtype: L{Element}
        """
        self.nsprefixes[p] = u
        return self

    def xml(self):
        """
        Get xml representation of the object.
        @return: The root node.
        @rtype: L{Element}
        """
        root = Element('Security', ns=WSSE_NS)
        for p, u in self.nsprefixes.items():
            root.addPrefix(p, u)
        root.set('SOAP-ENV:mustUnderstand', self.mustUnderstand)
        for t in self.tokens:
            root.append(t.xml())
        return root


class PayU_UsernameToken(UsernameToken):
    """
    Represents a basic I{UsernameToken} WS-Secuirty token.
    @ivar username: A username.
    @type username: str
    @ivar password: A password.
    @type password: str
    @ivar nonce: A set of bytes to prevent reply attacks.
    @type nonce: str
    @ivar created: The token created.
    @type created: L{datetime}
    """

    def __init__(self, username=None, password=None):
        """
        @param username: A username.
        @type username: str
        @param password: A password.
        @type password: str
        """
        UsernameToken.__init__(self, username, password)
        self.nsprefixes = {}
        
    def addPrefix(self, p, u):
        """
        Add or update a prefix mapping.
        @param p: A prefix.
        @type p: basestring
        @param u: A namespace URI.
        @type u: basestring
        @return: self
        @rtype: L{Element}
        """
        self.nsprefixes[p] = u
        return self

    def xml(self):
        """
        Get xml representation of the object.
        @return: The root node.
        @rtype: L{Element}
        """
        root = Element('UsernameToken', ns=WSSE_NS)
        for p,u in self.nsprefixes.items():
            root.addPrefix(p, u)
        root.append(Attribute('wsu:Id','UsernameToken-9'))
        root.append(Attribute('xmlns:wsu', WSU_URI))

        u = Element('Username', ns=WSSE_NS)
        u.setText(self.username)
        root.append(u)
        p = Element('Password', ns=WSSE_NS)
        p.setText(self.password)
        p.append(Attribute('Type', WSU_UN_URI))
        root.append(p)
        if self.nonce is not None:
            n = Element('Nonce', ns=WSSE_NS)
            n.setText(self.nonce)
            root.append(n)
        if self.created is not None:
            n = Element('Created', ns=WSU_NS)
            n.setText(str(UTC(self.created)))
            root.append(n)
        return root


class PayUProcessor(object):
    """
    """

    def __init__(self, details):
        """
        """
        self.details = details
        # setup the client to return a tuple instead of a WebFault instance
        self.client = Client(WSDL_URL, faults=False)
        security = self.build_security_header(self.username(), self.password())
        self.client.set_options(wsse=security)
        logging.getLogger('suds.client').setLevel(self.client_log_lvl())
        logging.getLogger('suds.transport').setLevel(self.transport_log_lvl())
        logging.getLogger('suds.xsd.schema').setLevel(self.schema_log_lvl())
        logging.getLogger('suds.wsdl').setLevel(self.wsdl_log_lvl())

    def build_security_header(self, username, password):
        """
        """
        security = PayU_Security()
        security.addPrefix(p='SOAP-ENC', u=SOAP_ENC_URI)
        token = PayU_UsernameToken(username, password)
        security.tokens.append(token)
        return security

    def setTransaction(self):
        """
        """
        transaction = dict(
            Api = self.api(),
            Safekey = self.safekey(),
            TransactionType = self.transactionType(),
            AdditionalInformation = self.additionalInformation(),
            Basket = self.basket(),
            Customer = self.customer(),
        )
        try:
            setTransaction = self.client.service.setTransaction(**transaction)
            import pdb;pdb.set_trace()
            return 1, None
        except Exception, e:
            print_exc()
            return 0, self.client.messages
    
    def getTransaction(self):
        """
        """
        return 1, None

    def username(self):
        """
        """
        return self.details['username']

    def password(self):
        """
        """
        return self.details['password']

    def api(self):
        """
        """
        return 'ONE_ZERO'
    
    def safekey(self):
        """
        """
        return self.details['safekey']

    def transactionType(self):
        """
        """
        return self.details['transactionType']
    
    def additionalInformation(self):
        """
        """
        return self.details['additionalInformation']
    
    def basket(self):
        """
        """
        return self.details['basket']
    
    def customer(self):
        """
        """
        return self.details['customer']

    def cancelUrl(self):
        """
        """
        return self.details['additionalInformation']['cancelUrl']

    def demoMode(self):
        """
        """
        return True

    def merchantReference(self):
        """
        """
        return self.details['additionalInformation']['merchantReference']

    def returnUrl(self):
        """
        """
        return self.details['additionalInformation']['returnUrl']

    def secure3d(self):
        """
        """
        return False

    def showBudget(self):
        """
        """
        return False

    def supportedPaymentMethods(self):
        """
        """
        return self.details['additionalInformation']['supportedPaymentMethods']
    
    def client_log_lvl(self):
        """
        """
        return self.details.get('client_log_lvl', )
    
    def transport_log_lvl(self):
        """
        """
        return self.details.get('transport_log_lvl', )
    
    def schema_log_lvl(self):
        """
        """
        return self.details.get('schema_log_lvl', )
    
    def wsdl_log_lvl(self):
        """
        """
        return self.details.get('wsdl_log_lvl', )

    def _build_security_header(self, username, password):
        """ Alternative method for building security header elements to use
            in the SOAP calls.  This method is *not* being used currently, but
            is left here for reference.
        """
        usernameElement = Element('Username', ns=WSSE_NS)
        usernameElement.setText(username)

        passwordElement = Element('Password', ns=WSSE_NS)
        passwordElement.setText(password)
        passwordElement.append(Attribute('Type', WSU_UN_URI))

        userCreds = Element('UsernameToken', ns=WSSE_NS)
        userCreds.append(Attribute('wsu:Id','UsernameToken-9'))
        userCreds.append(Attribute('xmlns:wsu', WSSE_URI))
        userCreds.insert(usernameElement)
        userCreds.insert(passwordElement)

        security = Element('Security', ns=WSSE_NS)
        security.addPrefix(p='SOAP-ENC', u=SOAP_ENC_URI)
        security.append(Attribute('SOAP-ENV:mustUnderstand', '1'))
        security.append(Attribute('xmlns:wsse', WSSE_URI))
        security.insert(userCreds)
        return security
    
    def _setTransaction(self):
        """ Alternative method for building the actual SetTransaction SOAP
            message object.  This method is *not* to be used as it introduces
            a wrapping 'Api' element that complete breaks the SOAP call.  I left
            the method here as I believe it can work, but do not currenlty have
            the time to figure out exactly why the wrapping element is created.
        """
        set_transaction = self.client.factory.create('setTransaction')
        set_transaction.Api = self.api()
        set_transaction.Safekey = self.safekey()
        set_transaction.TransactionType = 'PAYMENT'

        set_transaction.Basket.description = 'Basket Description comes here'
        set_transaction.Basket.amountInCents = '100'
        set_transaction.Basket.currencyCode = 'ZAR'

        set_transaction.AdditionalInformation.merchantReference = self.merchantReference()
        set_transaction.AdditionalInformation.demoMode = self.demoMode()
        set_transaction.AdditionalInformation.returnUrl = self.returnUrl()
        set_transaction.AdditionalInformation.cancelUrl = self.cancelUrl()
        set_transaction.AdditionalInformation.supportedPaymentMethods = 'CREDITCARD'

        set_transaction.Customer.merchantUserId = "7"
        set_transaction.Customer.email = "john@doe.com"
        set_transaction.Customer.firstName = 'John'
        set_transaction.Customer.lastName = 'Doe'
        set_transaction.Customer.mobile = '0211234567'

        try:
            setTransaction = self.client.service.setTransaction(set_transaction)
            return 1, None
        except Exception, e:
            return 0, self.client.messages

