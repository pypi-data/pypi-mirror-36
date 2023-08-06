# -*- coding: utf-8 -*-
import os

from setuptools import setup, find_packages
from codecs import open

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.rst'), encoding='utf-8') as f:
    CHANGES = f.read()

requires = [
    'sqlalchemy',
    'feedparser',
    'requests',
    'pytz',
    'zope.sqlalchemy',
    'transaction',
    'oe_geoutils',
    'oe_utils'
]

setup(
    name='oe_daemonutils',
    version='0.9.1',
    description='Daemon Utility Library',
    long_description=README + '\n\n' + CHANGES,
    url='https://github.com/OnroerendErfgoed/oe_daemonutils',
    author='Flanders Heritage Agency',
    author_email='ict@onroerenderfgoed.be',
    license='MIT',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords='oe daemon utility',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = oe_daemonutils:main
      """,
)
