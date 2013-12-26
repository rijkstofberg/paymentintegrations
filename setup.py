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

import pdb;pdb.set_trace()
from setuptools import setup, find_packages
import sys, os

version = '0.1'

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
CHANGES = open(os.path.join(here, 'CHANGES.md')).read()
LICENSE = open(os.path.join(here, 'LICENSE.md')).read()

# put external required package here
requires = [
        'lxml',
        'unittest2',
        'suds',
    ]

setup(name='paymentintegrations',
      version=version,
      description="Python payment integration examples and demos",
      long_description=README + '\n\n' + CHANGES,
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: Payment :: Payment integrations",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='Rijk Stofberg',
      author_email='rijk.stofberg@gmail.com',
      url='',
      license=LICENSE,
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='paymentintegrations',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = paymentintegrations:main
      [console_scripts]
      payu_cli = paymentintegrations.scripts.payu_cli:main
      """,
      )
