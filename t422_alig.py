LINELENGHT = 36

def a_center(txt):
    ss = '123'
    f = '{:^%d}' % LINELENGHT
    return f.format(txt)
