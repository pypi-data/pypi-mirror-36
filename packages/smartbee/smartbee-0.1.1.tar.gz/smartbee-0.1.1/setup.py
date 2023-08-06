from distutils.core import setup

setup(
  name = 'smartbee',
  packages = ['smartbee'], # this must be the same as the name above
  version = '0.1.1',
  description = 'Biblioteca para o projeto smartbee',
  author = 'Rhaniel Magalhães',
  author_email = 'rhaniel@alu.ufc.br',
  url = 'https://github.com/rhanielmx/smartbee', # use the URL to the github repo
  download_url = 'https://github.com/rhanielmx/smartbee/tarballl/0.1.1.tar.gz', # I'll explain this in a second
  install_requires=[
        'numpy==1.15.2',
        'pandas==0.23.4',
        'matplotlib==3.0.0'
    ],
  classifiers = [
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3'],
)