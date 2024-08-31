'''
by: @thiagocalvi
A principio o codigo do registrador eh isso 
'''

import struct

class Registrador:
    def __init__(self):
        self.set_valor(0)
        self.valor
    
    def set_valor(self, valor):
        self.valor = valor
    
    def get_valor(self):
        return self.valor