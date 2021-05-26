from setuptools import setup

import fitit

setup(
    name='fitit',
    version=str(fitit.VERSION),
    py_modules=['fitit'],

    description = 'A helper class for curve fitting',
    url = 'https://github.com/cdoolin/fitit',
    author = 'Callum Doolin',
    author_email = 'doolin@ualberta.ca',
    license = 'MIT',
    install_requires = ['numpy', 'scipy'],
    
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Scientific/Engineering',
    ],
)