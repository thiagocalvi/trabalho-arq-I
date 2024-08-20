import CPU

class Simulador:
    def __init__(self):
        pass


    
    #(Simulação de um compilador .as para código de maquina)
    #Ler as instruções do arquivo de .as, converte para instrução correspondete com 64 bits
    #Carregar na memória pricipal
    #Fazer isso antes de começar a executar as instruções
def carrega_programa(arquivo_instrucao):
    #Lê o arquivo .as com as instrução
    arquivo = open(arquivo_instrucao, 'r')
    instrucao, dados = ler_linha(arquivo)
    if instrucao != None:
        #Cada instrução e representada por 5 bits
        match(instrucao):
            case "add":
                opcode = "00000"
            
            case "addi":
                opcode = "00001"

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
                opcode = "10101"
                registrador = format(int(dados[0][1]), "b").zfill(5)
                valor = format(int(dados[1]), "b").zfill(64 - 10)
                print(opcode+registrador+valor)


def ler_linha(arquivo):
    linha = arquivo.readline()
    if linha != " ":
        linha = linha.split(" ")
        instrucao = linha[0]
        dados = linha[1].split(",")
        return instrucao, dados
    return None, None

carrega_programa("add_mov.as")