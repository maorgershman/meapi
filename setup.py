from setuptools import find_packages, setup
from re import search, M

VERSIONFILE = 'meapi/_version.py'

version_line = open(VERSIONFILE).read()
version_re = r"^__version__ = ['\"]([^'\"]*)['\"]"
match = search(version_re, version_line, M)
if match:
    version = match.group(1)
else:
    raise RuntimeError("Could not find version in '%s'" % VERSIONFILE)

setup(
    name='meapi',
    packages=find_packages(),
    version=version,
    description="Unofficial api for 'Me - Caller ID & Spam Blocker' app",
    long_description=(open('README.rst').read()),
    long_description_content_type="text/x-rst",
    author_email='davidlev@telegmail.com',
    url='https://meapi.readthedocs.io',
    author='David lev',
    license='MIT',
    install_requires=['requests'],
)
