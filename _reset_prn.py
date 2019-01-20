#!/usr/bin/python3
# -*- coding: utf-8 -*-


from t422 import *

x = T422()
x.continue_work()
x.reset()
st = x.status()
print(st)
print('{0:b}'.format(ord(st)))