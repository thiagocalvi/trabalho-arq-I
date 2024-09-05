class MemoriaPrincipal:
    def __init__(self, tamanho):
        # O tamanho agora é calculado em bytes
        # Cada posição armazena um dado de 64 bits (8 bytes)
        self.tamanho = tamanho * 8  # Calcula o tamanho real da memória em bytes
        self.memoria = [0] * self.tamanho  # Inicializa a memória com zeros

    def ler(self, endereco):
        # Recebe o endereço onde será realizada a leitura
        if endereco < 0 or endereco >= self.tamanho:
            # Verifica se o endereço está dentro do limite da memória
            raise ValueError("Endereço fora do limite da memória")
        # Retorna o dado armazenado no endereço informado
        return self.memoria[endereco]

    def escrever(self, endereco, valor):
        # Recebe o endereço de memória e o valor a ser escrito nesse endereço  
        if endereco < 0 or endereco >= self.tamanho:
            # Verifica se o endereço está dentro do limite da memória
            raise ValueError("Endereço fora do limite da memória")
        # Escreve o valor no endereço informado
        # O dado que era armazenado nesse endereço será sobrescrito
        self.memoria[endereco] = valor

    def imprimir_memoria(self):
        if self.tamanho > 256:
            colunas = 20
        else:
            colunas = 10

        for i in range(0, len(self.memoria), colunas):
            linha = self.memoria[i:i+colunas]
            # Formata a linha, tratando diferentes tipos de dados
            linha_formatada = [
                f"{dado}" if isinstance(dado, int) else str(dado)
                for dado in linha
            ]
            print(' '.join(linha_formatada))