#!/usr/bin/env python

from setuptools import setup

# Work around mbcs bug in distutils.
# http://bugs.python.org/issue10945
import codecs
try:
    codecs.lookup('mbcs')
except LookupError:
    ascii = codecs.lookup('ascii')
    codecs.register(lambda name, enc=ascii: {True: enc}.get(name == 'mbcs'))

VERSION = '0.1.2'

setup(
    name='dpay-graphenelib',
    version=VERSION,
    description='Python library for graphene-based blockchains',
    long_description=open('README.md').read(),
    download_url='https://github.com/dpays/dpay-python-graphenelib/tarball/' + VERSION,
    author='dPay DAO',
    author_email='jared@benchx.io',
    maintainer='dPay DAO',
    maintainer_email='jared@benchx.io',
    url='http://www.github.com/dpays/dpay-python-graphenelib',
    keywords=[
        'graphene',
        'api',
        'rpc',
        'ecdsa',
        'secp256k1'
    ],
    packages=["grapheneapi",
              "graphenebase",
              ],
    install_requires=["ecdsa",
                      "requests",
                      "websocket-client",
                      "pylibscrypt",
                      "pycryptodome",
                      ],
    classifiers=['License :: OSI Approved :: MIT License',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python :: 3',
                 'Development Status :: 3 - Alpha',
                 'Intended Audience :: Developers',
                 ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    include_package_data=True,
)
