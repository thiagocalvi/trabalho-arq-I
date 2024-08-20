import Registrador, MemoriaPrincipal, Cache

class CPU:
    def __init__(self):
        self.registradores: list = [Registrador() for _ in range(32)]
        self.pc = Registrador()
        self.rsp = Registrador()
        self.ra = Registrador()
        self.of = False #Overflow Flag



    #Ler da memoria a instrução na posisão de pc
    
    #Decodificar a instrução tamanho de 64 bits (8 bytes)
    #00000    00000     00000    00000   00000000000000000000000000000000000000000000    
    #OPCODE   REG       REG      REG

    #Operações aritméticas

    #Operações lógicas
        
    #Operações de desvios
        
    #Operações de memória
        
    #Operações de movimentação
    
    