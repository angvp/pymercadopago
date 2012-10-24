import os
from setuptools import setup
from version import __version__


required = [
    'requests',
]

packages = [
    'pymercadopago',
]

description = "A library to interact with the MercadoPago gateway payment"

setup(
    name="pymercadopago",
    version=__version__,
    author="Angel Velasquez, Diego Ramirez",
    author_email="angel.velasquez@elo7.com, diego.ramirez@elo7.com",
    description=description,
    license="MIT",
    keywords="mercadopago pymercadopago",
    url="https://bitbucket.org/angvp/pymercadopago",
    packages=packages,
    package_data={'pymercadopago':
        [
            'pymercadopago/*',
            'LICENSE.txt',
            'README',
            'CHANGES.txt',
        ]
        },
    include_package_data=True,
    platforms=['Platform Independent'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
    ],
    install_requires=required,
)
