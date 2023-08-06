from setuptools import setup

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='scaling',
    version='0.2.1',
    packages=['scaling'],
    install_requires=['pint'],
    author='Dan Howe',
    author_email='d.howe@wrl.unsw.edu.au',
    url='https://github.com/onewhaleid/scaling',
    description='convert units using Froude and Reynolds similitude')
