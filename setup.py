from gettext import install
import imp
from importlib.metadata import entry_points
from setuptools import setup, find_packages

setup(
    name='pdfimgrep',
    version='0.0.0',
    packages=find_packages(),
    install_requires=[
        'click'
    ],
    entry_points='''
    [console_scripts]
    pdfimgrep=main:cli
    '''
)