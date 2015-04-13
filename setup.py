#encoding: utf-8

"""
#Lulu

A web microframework inspired by Cuba, from Ruby.
"""
from setuptools import setup

setup(
    name=u'Lulu',
    version=u'0.0.1',
    license=u'MIT',
    author=u'Joaquín Muñoz',
    install_requires=[
        u'webob>=1.4',
        u'wheezy.routing>=0.1.157',
        u'beaker>=1.6.5.post1'
    ],
    packages=[u'Lulu'],
    platforms=u'any'
)