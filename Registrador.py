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
        #Arrumar essa verificação
        #if not (-2**63 <= valor <= 2**62 - 1):
        #    raise ValueError("Overflow de memória: o dado não pode ser armazenado em 64 bits (8 bytes)")
        
        self.valor = valor
    
    def get_valor(self):
        return self.valor
        #return struct.unpack('q', self.valor)[0]