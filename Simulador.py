import CPU
#Esse classe é onde o simulador vai começar a executar
#nela devemos ler os dados do arquivo de instrução e começar a executar as operações
#chamando os metódos da classe CPU nas respectivas operações

class Simulador:
    def __init__(self, arquivo_instrucao) -> None:
        self.arquivo_instrucao = open(arquivo_instrucao, 'r')
        #Ainda tem mais coisa para colocar aqui!

        #Receber aqui tambem a configuração do tamanho de memória entre outra configurações que
        #devem ser feitas


    '''
    TO-DO: Fazer uma função para carregar o programa para memória
    Todas as instruçãoes devem estar carregadas em memória, somente depois disso o programa é executado 
    '''


    
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


    def ler_linha(self, arquivo):
        try:
            linha = arquivo.readline()
            linha = linha.split(" ")
            instrucao = linha[0]
            dados = linha[1].split(",")
            return instrucao, dados
        except:
            return None, None