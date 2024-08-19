class Cache:
    def __init__(self, tamanho_linha, linhas_por_conjunto):
        self.tamanho_linha = tamanho_linha
        self.linhas_por_conjunto = linhas_por_conjunto
        self.conjuntos = [{} for _ in range(linhas_por_conjunto)]
