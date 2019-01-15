from setuptools import setup

import fitit

setup(name='fitit',
      version=str(fitit.VERSION),
      description='A helper class for curve fitting',
      url='https://github.com/cdoolin/fitit',
      author='Callum Doolin',
      author_email='doolin@ualberta.ca',
      license='MIT',
      py_modules=['fitit'])