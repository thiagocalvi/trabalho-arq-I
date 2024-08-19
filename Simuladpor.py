import CPU

class Simulador:
    def __init__(self):
        pass

    #Função para ler as intruções do arquivo de operações
    def ler_operacao(self):
        op_file = open('file_name', 'r')
        linha = op_file.readline()
        #Retorna uma lista 
        return linha.split(' ')[-1]
    
    