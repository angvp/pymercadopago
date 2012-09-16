import os
from setuptools import setup


required = [
    'requests',
]

packages = [
    'pymercadopago',
]

setup(
    name = "pymercadopago",
    version = "0.0.1",
    author = "Angel Velasquez, Diego Ramirez",
    author_email = "angel.velasquez@elo7.com, diego.ramirez@elo7.com",
    description = ("A library to interact with the Mercadopago gateway payment "),
    license = "MIT",
    keywords = "mercadopago pymercadopago",
    url = "https://bitbucket.org/angvp/pymercadopago",
    package_data={'pymercadopago': ['tests/*', ]},
    include_package_data=True,
    platforms=['Platform Independent'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Topic :: Software Development, Libraries, Python Modules',
        'License :: OSI Approved :: MIT License',
    ],
    install_requires=required,
    packages=packages,
)
