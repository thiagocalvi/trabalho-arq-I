class MemoriaPrincipal:
    def __init__(self, tamanho_bytes):
        if tamanho_bytes % 8 != 0:
            raise ValueError("O tamanho da memória deve ser múltiplo de 8 bytes")
        self.tamanho = tamanho_bytes
        self.dados = [0] * (tamanho_bytes // 8)  # Cada elemento representa 8 bytes

    def ler(self, endereco):
        if endereco % 8 != 0 or endereco >= self.tamanho:
            raise ValueError(f"Endereço inválido: {endereco}")
        return self.dados[endereco // 8]

    def escrever(self, endereco, valor):
        if endereco % 8 != 0 or endereco >= self.tamanho:
            raise ValueError(f"Endereço inválido: {endereco}")
        if not -2**63 <= valor < 2**63:
            raise ValueError(f"Valor fora do intervalo de 64 bits: {valor}")
        self.dados[endereco // 8] = valor

    def carregar_programa(self, programa, endereco_inicial=0):
        if endereco_inicial % 8 != 0:
            raise ValueError("O endereço inicial deve ser múltiplo de 8")
        for i, instrucao in enumerate(programa):
            self.escrever(endereco_inicial + i*8, instrucao)

    def __str__(self):
        return f"Memória Principal: {self.tamanho} bytes, {len(self.dados)} endereços de 64 bits"