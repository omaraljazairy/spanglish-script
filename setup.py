import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='Spanish_English_learning_own_way',
      version='3.1',
      py_modules=['spanglish'],
      description='a script where i add and test my self with the words and sentences I added',
      author='Omar Aljazairy',
      author_email='omar@fedal.nl',
      url='https://fedal.nl',
      long_description=read('README.md'),
      packages=['spanglish'],
      install_requires=[
          'Click==7.0',
          'tabulate==0.8.3',
          'psycopg2-binary',
      ],
      package_dir = {},
     )
