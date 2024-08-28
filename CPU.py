import Registrador, MemoriaPrincipal, Cache

class CPU:
    def __init__(self):
        self.registradores: list = [Registrador() for _ in range(32)]
        self.pc = Registrador()
        self.rsp = Registrador()
        self.ra = Registrador()
        self.cache_instrucao = Cache()
        self.cache_dados = Cache()
        self.memoria_principal = MemoriaPrincipal()
        self.of = False #Overflow Flag

    #Aqui é onde mais temos coisas para fazer

    #Operações aritméticas

    def add(self, rd, rs, rt):
        self.registradores[rd].valor = self.registradores[rs].valor + self.registradores[rt].valor
        if not (-2**63 <= self.registradores[rd].valor <= 2**62 - 1):
            self.of = True
    
    def addi(self, rd, rs, imediato):
        divisao = self.cache_instrucao.split(",")
        imediato = divisao[-1]
        self.registradores[rd].valor = self.registradores[rs].valor + imediato
        if not (-2**63 <= self.registradores[rd].valor <= 2**62 - 1):
            self.of = True

    def sub(self, rd, rs, rt):
        self.registradores[rd].valor = self.registradores[rs].valor - self.registradores[rt].valor
        if not (-2**63 <= self.registradores[rd].valor <= 2**62 - 1):
            self.of = True

    def subi(self, rd, rs, imediato):
        divisao = self.cache_instrucao.split(",")
        imediato = divisao[-1]
        self.registradores[rd].valor = self.registradores[rs].valor - imediato
        if not (-2**63 <= self.registradores[rd].valor <= 2**62 - 1):
            self.of = True

    def mul(self, rd, rs, rt):
        self.registradores[rd].valor = self.registradores[rs].valor * self.registradores[rt].valor
        if not (-2**63 <= self.registradores[rd].valor <= 2**62 - 1):
            self.of = True

    def div(self, rd, rs, rt):
        self.registradores[rd].valor = self.registradores[rs].valor / self.registradores[rt].valor
        if not (-2**63 <= self.registradores[rd].valor <= 2**62 - 1):
            self.of = True                                

    #Operações lógicas

    def negacao(self, rd, rs):
        self.registradores[rd].valor = ~self.registradores[rs].valor

    def or_(self, rd, rs, rt):
        self.registradores[rd].valor = self.registradores[rs].valor | self.registradores[rt].valor

    def and_(self, rd, rs, rt):
        self.registradores[rd].valor = self.registradores[rs].valor & self.registradores[rt].valor
        
    #Operações de desvios

    def blti(self, rs, rt, imediato):
        divisao = self.cache_instrucao.split(",")
        imediato = divisao[-1]
        if self.registradores[rs].valor > self.registradores[rt].valor:
            self.pc.valor = self.pc.valor + 1
            # adicionar pilha
        else:
            self.pc.valor = imediato
    
    def bgti(self, rs, rt, imediato):
        divisao = self.cache_instrucao.split(",")
        imediato = divisao[-1]
        if self.registradores[rs].valor < self.registradores[rt].valor:
            self.pc.valor = self.pc.valor + 1
            # adicionar pilha
        else:
            self.pc.valor = imediato

    def blt(self, rs, rt, rd):
        if self.registradores[rs].valor < self.registradores[rt].valor:
            self.pc.valor = self.pc.valor + 1
            # adicionar pilha
        else:
            self.pc.valor = self.registradores[rd].valor

    def bgt(self, rs, rt, rd):
        if self.registradores[rs].valor > self.registradores[rt].valor:
            self.pc.valor = self.pc.valor + 1
            # adicionar pilha
        else:
            self.pc.valor = self.registradores[rd].valor

    def beq(self, rs, rt, imediato):
        divisao = self.cache_instrucao.split(",")
        imediato = divisao[-1]
        if self.registradores[rs].valor == self.registradores[rt].valor:
            self.pc.valor = imediato

    def beqi(self, rs, rt, imediato):
        divisao = self.cache_instrucao.split(",")
        imediato = divisao[-1]
        if self.registradores[rs].valor == self.registradores[rt].valor:
            self.pc.valor = imediato

    def jr(self, rd):
        self.pc.valor = self.registradores[rd].valor

    def jof(self, rd):
        if self.of:
            self.pc.valor = self.registradores[rd].valor            

    def jal(self, imediato):
        divisao = self.cache_instrucao.split(",")
        imediato = divisao[-1]
        self.ra.valor = self.pc.valor + 1
        self.pc.valor = imediato  

    def ret(self):
        self.pc.valor = self.ra.valor          
        
    #Operações de memória

    def lw(self, rd, rs, imediato):
        divisao = self.cache_instrucao.split(",")
        imediato = divisao[-1]
        endereco = self.registradores[rs].valor + imediato
        valor = self.cache_dados.ler(endereco)
        if valor is None:
            valor = self.memoria_principal.ler(endereco)
            self.cache_dados.escrever(endereco, valor)
        self.registradores[rd].valor = valor
        #terminar parte da cache

    def sw(self, rs, rt, imediato):
        divisao = self.cache_instrucao.split(",")
        imediato = divisao[-1]
        endereco = self.registradores[rt].valor + imediato
        self.cache_dados.escrever(endereco, self.registradores[rs].valor)
        self.memoria_principal.escrever(endereco, self.registradores[rs].valor)
        #terminar parte da cache
        
    #Operações de movimentação

    def mov(self, rd, rs):
        self.registradores[rd].valor = self.registradores[rs].valor

    def movi(self, rd, imediato):
        divisao = self.cache_instrucao.split(",")
        imediato = divisao[-1]
        self.registradores[rd].valor = imediato
    
    