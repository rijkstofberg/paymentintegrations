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

import sys
from cmd import Cmd

from paymentintegrations.processors import PayUProcessor

storeDetails = dict(
    soapUsername = 'Staging Integration Store 1',
    soapPassword = '78cXrW1W',
    safekey      = '{45D5C765-16D2-45A4-8C41-8D6F84042F8C}',
    environment  = 'staging',
)

additionalDetails = dict(
    payUReference = 11998836694
)

details = dict(
    store                 = storeDetails,
    additionalInformation = additionalDetails,
)

class PayUCLI(Cmd):
    prompt = '[PayU] '
    intro = 'Command line interface to PayU payment services.'
    processor = PayUProcessor(details)
    
    def do_get_wsdl(self, args):
        print self.processor.__repr__()

    def do_getTransaction(self, args):
        print 'getting a transaction'
        self.processor.process()

    def help_getTransaction(self):
        print 'getTransaction help'

    def do_setTransaction(self, args):
        print 'setting a new transaction'

    def help_setTransaction(self):
        print 'setTransaction help'

    def do_quit(self, args):
        return True
    
    def help_quit(self):
        print 'Immediately quit the program.'
    
    def do_q(self, args):
        return self.do_quit(args)

    def help_q(self):
        return self.help_quit()
    

def main():
    command = PayUCLI()
    Cmd.cmdloop(command)

if __name__ == '__main__':
    main()
