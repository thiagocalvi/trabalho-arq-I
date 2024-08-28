from Registrador import Registrador
from MemoriaPrincipal import MemoriaPrincipal
from Cache import MemoriaCache

class CPU:
    def __init__(self, tamanho_memoria_princiapal):
        self.registradores: list = [Registrador() for _ in range(32)]
        self.pc = Registrador()
        self.rsp = Registrador()
        self.ra = Registrador()
        self.of = False #Overflow Flag
        self.memoriaPrincipal = MemoriaPrincipal(tamanho_memoria_princiapal)


    def executar(self):
        #Praticamente todo o programa será executado aqui dentro
        #Buscar na cache de instrução no endereço de PC
        #TO-DO: Desenvolver mais o fluxo de execução do progra
        
        match(None):
            case "add":
                pass

            case "addi":
                pass

            case "sub":
                pass

            case "subi":
                pass
                    

            case "mul":
                pass
                    

            case "div":
               pass

            case "not":
                pass
                    
                
            case "or":
                pass
                    

            case "and":
                pass
                    

            case "blti":
                pass
                    

            case "bgti":
                pass
                    

            case "beqi":
                pass
                    

            case "blt":
                pass
                    

            case "beq":
                pass
                    

            case "beq":
                pass
                    

            case "jr":
                pass
                    

            case "jof":
                pass
                    

            case "jal":
                pass
                    

            case "ret":
                pass
                    

            case "lw":
                pass
                    

            case "sw":
                pass
                    

            case "mov":
                pass
                    

            case "movi":
                pass


    #Aqui é onde mais temos coisas para fazer

    #Operações aritméticas

    #Operações lógicas
        
    #Operações de desvios
        
    #Operações de memória
        
    #Operações de movimentação
    
    