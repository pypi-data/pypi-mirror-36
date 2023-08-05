#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='zzzutils',
    version='0.1.7',
    description='Time utils for Humans.',
    long_description=open('README.rst').read(),
    long_description_content_type='text/x-rst',
    author='ZhiZhi Zhang',
    author_email='zhangzhizhibit@163.com',
    url='https://github.com/zzzbit/zzz-utils',
    packages=find_packages(),
    license='Apache 2.0',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
)
