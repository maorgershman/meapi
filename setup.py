from setuptools import find_packages, setup

setup(
    name='meapi',
    packages=find_packages(),
    version='0.1.0',
    description='MeAPI - caller id',
    author='David lev',
    license='MIT',
    install_requires=[requests],
)
