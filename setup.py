from setuptools import find_packages, setup

setup(
    name='meapi',
    packages=find_packages(),
    version='0.1.0',
    description="Unofficial api for 'Me - Caller ID & Spam Blocker' app",
    long_description=(open('README.rst').read()),
    author_email='davidlev@telegmail.com',
    url='https://meapi.readthedocs.io',
    author='David lev',
    license='MIT',
    install_requires=['requests'],
)
