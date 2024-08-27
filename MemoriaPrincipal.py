'''
Essa uma implementação bem básica da memória principal
contendo as funções basicas de uma memoria
A memoria armazena uma instrução ou um inteiro de 64 bits (8 bytes)
'''

class MemoriaPrincipal:
    def __init__(self, tamanho):
        #TO-DO: Rever o calculo do tamanho da memória
        self.memoria = [0] * tamanho  # Inicializa a memória com zeros

    def ler(self, endereco):
        #Recebe o endereço onde será realizada a leitura
        if endereco < 0 or endereco >= len(self.memoria):
            #Verifica se o endereço está dento do limite da memória
            raise ValueError("Endereço fora do limite da memória")
        #Retorna o dado armazena no endereço informado
        return self.memoria[endereco]

    def escrever(self, endereco, valor):
        #Recebe o endereço de memória e o valor a ser escrito nesse endereço  
        if endereco < 0 or endereco >= len(self.memoria):
            #Verifica se o endereço está dento do limite da memória
            raise ValueError("Endereço fora do limite da memória")
        #Escreve o valor no endereço informado
        #O dado que era armazenado nesse endereço será sobrescrito
        self.memoria[endereco] = valor
