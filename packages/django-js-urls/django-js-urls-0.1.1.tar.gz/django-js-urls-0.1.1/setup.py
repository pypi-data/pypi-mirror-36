# -*- coding: utf-8 -*-

import codecs
from os.path import abspath
from os.path import dirname
from os.path import join
from setuptools import find_packages
from setuptools import setup

import js_urls


def read_relative_file(filename):
    """ Returns contents of the given file, whose path is supposed relative to this module. """
    with codecs.open(join(dirname(abspath(__file__)), filename), encoding='utf-8') as f:
        return f.read()


setup(
    name='django-js-urls',
    version=js_urls.__version__,
    author='impak Finance',
    author_email='tech@impakfinance.com',
    packages=find_packages(exclude=['tests.*', 'tests']),
    include_package_data=True,
    url='https://github.com/impak-finance/django-js-urls',
    license='MIT',
    description='A convenient helper to use Django URLs in Javascript.',
    long_description=read_relative_file('README.rst'),
    keywords='django javascript js url urls helper',
    zip_safe=False,
    install_requires=[
        'django>=1.11',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
