#!/usr/bin/python3
# -*- coding: utf-8 -*-


from t422 import *

x = T422()
st = x.status()
print(st)
print('{0:b}'.format(ord(str(st))))