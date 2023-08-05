#!/usr/bin/env python
# ------------------------------------
#  Author: YAOYAO PEI
#  E-mail: yaoyao.bae@foxmail.com
# -------------------------------------
from setuptools import setup

setup(name='feon',
      version='1.0.3',
      description='FEA python-based framework',
      author='YAOYAO PEI',
      author_email='yaoyao.bae@foxmail.com',
      url = 'https://github.com/YaoyaoBae/Feon',
      packages=['feon','feon.sa','feon.ffa',"feon.derivation"],
      install_requires=['numpy'],
      
      )
