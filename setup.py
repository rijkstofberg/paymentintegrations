from setuptools import setup, find_packages
import sys, os

version = '0.1'

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
CHANGES = open(os.path.join(here, 'CHANGES.md')).read()

# put external required package here
requires = [
    ]

setup(name='paymentintegrations',
      version=version,
      description="",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Rijk Stofberg',
      author_email='rijk.stofberg@gmail.com',
      url='',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      test_suite='paymentintegrations',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = paymentintegrations:main
      [console_scripts]
      payu_cli = paymentintegrations.scripts.payu_cli:main
      """,
      )
