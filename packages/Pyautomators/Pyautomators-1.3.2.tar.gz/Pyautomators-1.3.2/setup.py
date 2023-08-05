# -*- coding: utf-8 -*-
from setuptools import setup,find_packages

setup(name='Pyautomators',
      version='1.3.2',
      url='',
      license='MIT',
      author='Kaue_Bonfim',
      author_email='koliveirab@indracompany.com',
      description='Biblioteca de automação para geracao completa de ambientacao de testes',
      packages=['Pyautomators'],
	  install_requires=["pytesseract","pillow","pyyaml","peewee","pyautogui","assertpy","cx_Oracle","selenium","pytractor","numpy","PyMySQL==0.7.8","opencv-python","Appium-Python-Client","behave2cucumber","python-jenkins","behave","django","pandas","pymongo","beautifulsoup4","nltk","TestLink-API-Python-client","sqlalchemy","argparse"],
      zip_safe=True)
	  


