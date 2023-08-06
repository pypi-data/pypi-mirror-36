from setuptools import setup
import os
import io


here = os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = '\n' + f.read()

VERSION = '0.1.1'

setup(
    name='gdockutils',
    description='Galaktika Solutions - Docker Utilities',
    long_description=long_description,
    version=VERSION,
    url='https://github.com/galaktika-solutions/gDockUtils',
    author='Richard Bann',
    author_email='richardbann@gmail.com',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6'
    ],
    license='MIT',
    packages=['gdockutils'],
    entry_points={
        'console_scripts': [
            'gprun=gdockutils.gprun:main',
            'ask=gdockutils.ask:main'
        ],
    }
)
