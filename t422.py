#!/usr/bin/python3
# -*- coding: utf-8 -*-

import serial, time 
from t422_alig import *

DEVICE_PORT = '/dev/ttyS0'
DEVICE_SPEED = 38400
STR_WIDTH = 36

ESC = 0x1b
BOLD = 0x47
DOUBLE = 0x21
CUT = 0x69
LF = 0x0a      # print end feed
CR = 0x0d      # print, N.B. This command is ignored.
STATUS = 0x76
BEEP = 0x07
GS_k = [0x1d,0x6b]
GS_B = [0x1d,0x42]
CODE_EAN13 = 67
CODE128 = 73
AT = 0x40
GS_V = [0x1d,0x56]

HEAD0 = 'ТЗОВ "ГАЛ-ВСЕСВІТ"'
HEAD1 = 'АВТОВОКЗАЛ "ПІВНІЧНИЙ"'
HEAD2 = 'М.ЛЬВІВ,ВУЛ.Б.ХМЕЛЬНИЦЬКОГО,225'
FOOTER0 = '------------------------------------'
FOOTER1 = 'ЧЕК НЕ ФІСКАЛЬНИЙ'
FOOTER2 = 'Вдалої поїздки'

class T422:
        
    bold = False
    state = 0

    def __init__(self):
        ser = serial.Serial()
        ser.baudrate = DEVICE_SPEED
        ser.port = DEVICE_PORT 
        ser.timeout = 0.1
        ser.close()
        ser.open()   
        self.printer = ser

    def utf_to_866bytes(self, txt):
        with open('/tmp/prn.txt', 'w', encoding='cp866') as f:
            f.write(txt.replace('і','i').replace('І','I'))
        with open('/tmp/prn.txt', 'rb') as f:
            arr = f.read()
        return arr

    def barcodePDF(self, code):
        arr = self.utf_to_866bytes(code)
        str_prn = bytearray()
        str_prn.extend(GS_k)
        str_prn.extend([9,0])
#        str_prn.append(len(code)+2)
        str_prn.extend([123,65])
        str_prn.extend(arr)
        str_prn.append(0x0)
        for i in str_prn:
#            print(i)
            print('hex: {0:02x} - {1}  - {2}'.format(i,i,i.to_bytes(1,byteorder='big')))
        self.printer.write(str_prn)

    def barcode128(self, code):
        arr = self.utf_to_866bytes(code)
        arr128 = []
        count = 0
        for i in arr:
            print(i)
            x = int(i) - 48
            print(x)
            if count % 2 == 0:
                left = x * 10
            else:
                arr128.append(x + left)
            count += 1
        str_prn = bytearray()
        str_prn.extend(GS_k)
        str_prn.append(CODE128)
#        str_prn.append(len(code) +2)
        str_prn.append(len(arr128) + 2)
        str_prn.extend([123,67])
        str_prn.extend(bytes(arr128))
#        str_prn.append(0x0)
        for i in str_prn:
#            print(i)
            print('hex: {0:02x} - {1}  - {2}'.format(i,i,i.to_bytes(1,byteorder='big')))
        self.printer.write(str_prn)

    def barcodeEAN13(self, code):
        arr = self.utf_to_866bytes(code)
        str_prn = bytearray()
        str_prn.extend(GS_k)
        str_prn.append(CODE_EAN13)
        str_prn.append(len(code))
        str_prn.extend(arr)
        for i in str_prn:
#            print(i)
            print('hex: {0:02x} - {1}'.format(i,i))
        self.printer.write(str_prn)



    def print_bold(self, txt):
        arr = self.utf_to_866bytes(txt)
        str_prn = bytearray()
        str_prn.append(ESC)
        str_prn.append(BOLD)
        str_prn.append(1)
        str_prn.extend(arr)
        str_prn.append(ESC)
        str_prn.append(BOLD)
        str_prn.append(0)
        self.printer.write(str_prn)

    def print_double(self, txt):
        arr = self.utf_to_866bytes(txt)
        str_prn = bytearray()
        str_prn.append(ESC)
        str_prn.append(DOUBLE)
        str_prn.append(32)
        str_prn.extend(arr)
        str_prn.append(ESC)
        str_prn.append(DOUBLE)
        str_prn.append(0)
        self.printer.write(str_prn)

    def print_BW_invert(self, txt):
        arr = self.utf_to_866bytes(txt)
        str_prn = bytearray()
        str_prn.extend(GS_B)
        str_prn.append(1)
        str_prn.extend(arr)
        str_prn.extend(GS_B)
        str_prn.append(0)
        self.printer.write(str_prn)


    def print_txt(self, txt):
        arr = self.utf_to_866bytes(txt)
        str_prn = bytearray()
        str_prn.extend(arr)
        self.printer.write(str_prn)

    def cutOLD(self):
        str_prn = bytearray()
        str_prn.append(ESC)
        str_prn.append(CUT)
        self.printer.write(str_prn)

    def cut(self):
        str_prn = bytearray()
        str_prn.extend(GS_V)
        str_prn.append(66)
        str_prn.append(1)
        self.printer.write(str_prn)
   
    def LF(self):
        str_prn = bytearray()
        str_prn.append(LF)
        self.printer.write(str_prn)


    def reset(self):
        str_prn = bytearray()
        str_prn.append(ESC)
        str_prn.append(AT)
        self.printer.write(str_prn)

    def continue_work(self):
        str_prn = bytearray()
        str_prn.append(0x10)
        str_prn.append(0x05)
        str_prn.append(0x01)
        self.printer.write(str_prn)

    def cp866(self):
        str_prn = bytearray()
        str_prn.append(ESC)
        str_prn.append(AT)
        self.printer.write(str_prn)
        time.sleep(0.5)
        str_prn = bytearray()
        str_prn.append(ESC)
        str_prn.append(0x74)
        str_prn.append(17)
        self.printer.write(str_prn)


    def statusOLD(self):
        str_prn = bytearray()
        str_prn.append(ESC)
        str_prn.append(0x76)
        self.printer.write(str_prn)
        time.sleep(0.5)
        state = self.printer.read(1) 
        return state

    def status(self):
        str_prn = bytearray()
        str_prn.append(0x1d)
        str_prn.append(0x72)
        str_prn.append(0x1)
        self.printer.write(str_prn)
        time.sleep(0.5)
        state = self.printer.read(1)
#        print(state)
        if state == b'`':
            return 0
        else: 
            return state


    def head(self):
        if not HEAD0 == '':
            str_prn = bytearray()
            arr = self.utf_to_866bytes(a_center(HEAD0))
            str_prn.extend(arr)
            self.printer.write(str_prn)
            self.LF()
        if not HEAD1 == '':
            str_prn = bytearray()
            arr = self.utf_to_866bytes(a_center(HEAD1))
            str_prn.extend(arr)
            self.printer.write(str_prn)
            self.LF()
        if not HEAD2 == '':
            str_prn = bytearray()
            arr = self.utf_to_866bytes(a_center(HEAD2))
            str_prn.extend(arr)
            self.printer.write(str_prn)
            self.LF()

    def footer(self):
        if not FOOTER0 == '':
            str_prn = bytearray()
            arr = self.utf_to_866bytes(a_center(FOOTER0))
            str_prn.extend(arr)
            self.printer.write(str_prn)
            self.LF()
        if not FOOTER1 == '':
            str_prn = bytearray()
            arr = self.utf_to_866bytes(a_center(FOOTER1))
            str_prn.extend(arr)
            self.printer.write(str_prn)
            self.LF()
        if not FOOTER2 == '':
            str_prn = bytearray()
            arr = self.utf_to_866bytes(a_center(FOOTER2))
            str_prn.extend(arr)
            self.printer.write(str_prn)
            self.LF()
        self.cut()
        
'''     
    
ser.write(my_bytes_2)
time.sleep(0.5)
bytes = ser.read(32)  
print (bytes)      
    
ser.write(my_bytes_3)
time.sleep(0.5)
bytes = ser.read(2)  
print (bytes)      
    
ser.write(my_bytes_4)
time.sleep(0.5)
bytes = ser.read(1)  
print (bytes)    
'''
    






