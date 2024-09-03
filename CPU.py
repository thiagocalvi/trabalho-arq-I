'''
TO DO 
Fazer um função para imprimir a memoria principal 
'''

from Registrador import Registrador
from MemoriaPrincipal import MemoriaPrincipal 
from Cache import MemoriaCache

class CPU:
    def __init__(self, tam_memoria):
        self.registradores: list = [Registrador() for _ in range(32)]
        self.pc = Registrador()
        self.rsp = Registrador()
        self.ra = Registrador()
        self.memoria_principal = MemoriaPrincipal(tam_memoria)
        self.cache_instrucao = MemoriaCache(num_conjuntos=64, linhas_por_conjunto=4, tamanho_bloco=16, memoria_principal=self.memoria_principal)
        self.cache_dados = MemoriaCache(num_conjuntos=64, linhas_por_conjunto=4, tamanho_bloco=16, memoria_principal=self.memoria_principal)
        self.of = Registrador() #Overflow Flag
        self.max_pc = 0 #controlar quando a execução chegou ao fim


    def imprimir_registradores(self):
        """Imprime o valor de todos os registradores e dos especiais PC, RSP e RA."""
        print("Valores dos Registradores:")
        for i, registrador in enumerate(self.registradores):
            print(f"R{i}: {registrador.get_valor()}")
        
        print("----------------------------------------")
        print(f"PC: {self.pc.get_valor()}")
        print(f"RSP: {self.rsp.get_valor()}")
        print(f"RA: {self.ra.get_valor()}")
        print(f"Overflow: {self.of.get_valor()}")
        print("----------------------------------------")
        print("Memória principal")
        self.memoria_principal.imprimir_memoria()    

        
        print("********************************************************************************************\n")
    
    def parse_riscv_instruction(self, instruction):
        parts = instruction.split(',')
        numbers = []

        for part in parts:
            part = part.strip()
            
            # Caso de acesso à memória com endereçamento indireto
            if '(' in part and ')' in part:
                offset, reg = part.split('(')
                reg = reg.rstrip(')')
                
                # Processa o offset
                if offset:
                    try:
                        numbers.append(int(offset))
                    except ValueError:
                        pass
                
                # Processa o registrador base
                if reg.startswith('r'):
                    try:
                        numbers.append(int(reg[1:]))
                    except ValueError:
                        pass
            
            # Caso de registrador
            elif part.startswith('r'):
                try:
                    numbers.append(int(part[1:]))
                except ValueError:
                    pass
            
            # Caso de valor imediato
            else:
                try:
                    numbers.append(int(part))
                except ValueError:
                    pass

        return numbers

    def executar(self):
        for _ in range(1024):
            endereco_instrucao = self.pc.get_valor()
            
            if endereco_instrucao >= self.max_pc:
                print("FIM DA EXECUÇÃO")
                return
            
            instrucao = self.cache_instrucao.ler(endereco_instrucao)
            # if instrucao is None:
            #     instrucao = self.memoria_principal.ler(endereco_instrucao)
            #     self.cache_instrucao.escrever(endereco_instrucao, instrucao)
            
            # Decodificar e executar a instrução
            print("Instrução sendo executada:", instrucao)
            partes = instrucao.split(" ")
            comando = partes[0]
            parametros = self.parse_riscv_instruction(partes[1])

            match(comando):
                case "add":
                     self.add(parametros[0], parametros[1], parametros[2])

                case "addi":
                    self.addi(parametros[0], parametros[1], parametros[2])
                
                case "sub":
                    self.sub(parametros[0], parametros[1], parametros[2])

                case "subi":
                    self.subi(parametros[0], parametros[1], parametros[2])
                
                case "mul":
                    self.mul(parametros[0], parametros[1], parametros[2])

                case "div":
                    self.div(parametros[0], parametros[1], parametros[2])
                    
                case "not":
                    self.not_(parametros[0], parametros[1])
                    
                case "or":
                    self.or_(parametros[0], parametros[1], parametros[2])

                case "and":
                    self.and_(parametros[0], parametros[1], parametros[2])
                    
                case "blti":
                    self.blti(parametros[0], parametros[1], parametros[2])
                    
                case "bgti":
                    self.bgti(parametros[0], parametros[1], parametros[2])

                case "beqi":
                    self.beqi(parametros[0], parametros[1], parametros[2])
                    
                case "blt":
                    self.blt(parametros[0], parametros[1], parametros[2])

                case "beq":
                    self.beq(parametros[0], parametros[1], parametros[2])

                case "jr":
                    self.jr(parametros[0])

                case "jof":
                    self.jof(parametros[0])
                    
                case "jal":
                    self.jal(parametros[0])
                    
                case "ret":
                    self.ret()
                
                case "lw":
                    self.lw(parametros[0], parametros[1], parametros[2])
                    
                case "sw":
                    self.sw(parametros[0], parametros[1], parametros[2])
                
                case "mov":
                    self.mov(parametros[0], parametros[1])

                case "movi":
                    self.movi(parametros[0], parametros[1])
                    
            self.pc.set_valor(self.pc.get_valor() + 1)
            self.imprimir_registradores()
            #self.imprimir_memoria()
            self.of.set_valor(0)

    #Operações aritméticas    
    def add(self, rd, rs, rt):
        #Executa a operação de adição entre dois registradores e armazena o resultado em um terceiro registrador.
        valor_rs = self.registradores[rs].get_valor()
        valor_rt = self.registradores[rt].get_valor()
        resultado = valor_rs + valor_rt
        
        # Verificar overflow
        if not (-2**63 <= resultado <= 2**62 - 1):
            self.of.set_valor(1)
        else:
            self.registradores[rd].set_valor(resultado)

    def addi(self, rd, rs, imediato):
        #Executa a operação de adição entre um registradore e um valor imediato e armazena o valor em um segundo registrador.
        
        resultado = self.registradores[rs].get_valor() + imediato

        # Verificar overflow
        if not (-2**63 <= resultado <= 2**62 - 1):
            self.of.set_valor(1)
        else:
            self.registradores[rd].set_valor(resultado)

    def sub(self, rd, rs, rt):
        #Executa a operação de subtração entre dois registradores e armazena o resultado em um terceiro registrador.

        resultado = self.registradores[rs].get_valor() - self.registradores[rt].get_valor()
        
        # Verificar overflow
        if not (-2**63 <= resultado <= 2**62 - 1):
            self.of.set_valor(1)
        else:
            self.registradores[rd].set_valor(resultado)

    def subi(self, rd, rs, imediato):
        #Executa a operação de subtração entre um registradore e um valor imediato e armazena o valor em um segundo registrador.
        
        resultado = self.registradores[rs].get_valor() - imediato
        
        # Verificar overflow
        if not (-2**63 <= resultado <= 2**62 - 1):
            self.of.set_valor(1)
        else:
            self.registradores[rd].set_valor(resultado)

    def mul(self, rd, rs, rt):
        #Executa a operação de multiplicação entre dois registradores e armazena o resultado em um terceiro registrador.

        resultado = self.registradores[rs].get_valor() * self.registradores[rt].get_valor()
        
        # Verificar overflow
        if not (-2**63 <= resultado <= 2**62 - 1):
            self.of.set_valor(1)
        else:
            self.registradores[rd].set_valor(resultado)

    def div(self, rd, rs, rt):
        #Executa a operação de divisão entre dois registradores e armazena o resultado em um terceiro registrador.

        resultado = self.registradores[rs].get_valor() / self.registradores[rt].get_valor()
        
        # Verificar overflow
        if not (-2**63 <= resultado <= 2**62 - 1):
            self.of.set_valor(1)
        else:
            self.registradores[rd].set_valor(resultado)                                                              

    #Operações lógicas
    def not_(self, rd, rs):
        """Realiza a operação NOT bit a bit no registrador `rs` e armazena o resultado em `rd`."""
        valor_rs = self.registradores[rs].get_valor()
        resultado = ~valor_rs
        self.registradores[rd].set_valor(resultado)

    def or_(self, rd, rs, rt):
        """Realiza a operação OR bit a bit entre os registradores `rs` e `rt` e armazena o resultado em `rd`."""
        valor_rs = self.registradores[rs].get_valor()
        valor_rt = self.registradores[rt].get_valor()
        resultado = valor_rs | valor_rt
        self.registradores[rd].set_valor(resultado)

    def and_(self, rd, rs, rt):
        """Realiza a operação AND bit a bit entre os registradores `rs` e `rt` e armazena o resultado em `rd`."""
        valor_rs = self.registradores[rs].get_valor()
        valor_rt = self.registradores[rt].get_valor()
        resultado = valor_rs & valor_rt
        self.registradores[rd].set_valor(resultado)

    #Operações de desvios - Implementar o gerenciamento da pilha
    def blti(self, rs, rt, imediato):
        if self.registradores[rs].get_valor() < self.registradores[rt].get_valor():
            self.pc.set_valor(imediato - 1)
    
    def bgti(self, rs, rt, imediato):
        if self.registradores[rs].get_valor() > self.registradores[rt].get_valor():
            self.pc.set_valor(imediato - 1)

    def beqi(self, rs, rt, imediato):
        if self.registradores[rs].get_valor() == self.registradores[rt].get_valor():
            self.pc.set_valor(imediato - 1)

    def blt(self, rs, rt, rd):
        if self.registradores[rs].get_valor() < self.registradores[rt].get_valor():
            self.pc.set_valor(self.pc.get_valor() + (rd-1))

    def bgt(self, rs, rt, rd):
        if self.registradores[rs].get_valor() > self.registradores[rt].get_valor():
            self.pc.set_valor(self.registradores[rd].get_valor())

    def beq(self, rs, rt, imediato):
        if self.registradores[rs].get_valor() == self.registradores[rt].get_valor():
            self.pc.set_valor(imediato - 1)

    def jr(self, rd):
        self.pc.set_valor(self.registradores[rd].get_valor())

    def jof(self, rd):
        if self.of.get_valor() == 1:
            self.pc.set_valor(self.registradores[rd].set_valor())             

    def jal(self, imediato):
        self.pc.set_valor(imediato - 1)

    def ret(self):        
        self.pc.set_valor(self.ra.get_valor())
                
    #Operações de memória
    def lw(self, rd, imediato, rs):
        endereco = self.registradores[rs].get_valor() + imediato
        valor = self.cache_dados.ler(endereco)
        self.registradores[rd].set_valor(valor)

    def sw(self, rs, imediato, rt):
        endereco = self.registradores[rt].get_valor() + imediato
        self.memoria_principal.escrever(endereco, self.registradores[rs].get_valor())
        self.cache_dados.escrever(endereco, self.registradores[rs].get_valor())
        
    #Operações de movimentação
    def mov(self, rd, rs):
        self.registradores[rd].set_valor(self.registradores[rs].get_valor())

    def movi(self, rd, imediato):
        self.registradores[rd].set_valor(imediato)