from setuptools import setup, find_packages

setup(
    name='ptx_api',
    version='1.0.2',
    description='A Python Module for get data from PTX.',
    author='pinlin',
    author_email='moneycat711@gmail.com',
    license='MIT License',
    packages=find_packages(),
    install_requires=['requests'],
    platforms=["all"],
    url='https://github.com/PinLin/ptx_api',)
