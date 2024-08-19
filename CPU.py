import Registrador, MemoriaPrincipal, Cache

class CPU:
    def __init__(self):
        self.registradores: list = [Registrador() for _ in range(32)]
        self.pc = Registrador()
        self.rsp = Registrador()
        self.ra = Registrador()
        self.of = False #Overflow Flag
