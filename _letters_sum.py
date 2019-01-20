#!/usr/bin/python3
# -*- coding: utf-8 -*-


from t422 import *

x = T422()
x.cp866()
x.head()
x.print_bold('BOLD')
x.LF()
x.print_txt('1234567890123456789012345678901234567890')
x.LF()
x.print_bold('1234567890123456789012345678901234567890')
x.LF()
x.print_txt('EAN13')
x.LF()
x.barcodeEAN13('123456789012')
#x.print_txt('PDF417')
#x.LF()
#x.barcodePDF('110033445566')
#
x.print_txt('CODE128')
#
x.LF()
#
x.barcode128('112233445566')    #not work on ep60? work fine on t422
x.footer()
