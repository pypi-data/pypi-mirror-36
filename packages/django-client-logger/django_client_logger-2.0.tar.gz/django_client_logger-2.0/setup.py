import os
from setuptools import setup

README = """
See the README on `GitHub
<https://github.com/uw-it-aca/django_client_logger>`_.
"""

# The VERSION file is created by travis-ci, based on the tag name
version_path = 'django_client_logger/VERSION'
VERSION = open(os.path.join(os.path.dirname(__file__), version_path)).read()
VERSION = VERSION.replace("\n", "")

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

url = "https://github.com/uw-it-aca/django_client_logger"
setup(
    name='django_client_logger',
    version=VERSION,
    packages=['django_client_logger'],
    author="UW-IT AXDD",
    author_email="aca-it@uw.edu",
    include_package_data=True,
    install_requires=[
        'Django>2.1',
        'mock',
        'django-userservice>=3.1,<4.0',
    ],
    license='Apache License, Version 2.0',
    description=("Client logging application for django"),
    long_description=README,
    url=url,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
    ],
)

