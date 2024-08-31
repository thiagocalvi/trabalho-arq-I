class LinhaCache:
    def __init__(self, tamanho_bloco):
        self.tag = None                  # Tag usada para identificar o bloco
        self.dados = [0] * tamanho_bloco # Bloco de dados
        self.valido = False              # Indica se a linha é válida

class MemoriaCache:
    def __init__(self, num_conjuntos, linhas_por_conjunto, tamanho_bloco, memoria_principal):
        self.num_conjuntos = num_conjuntos            # Quantidade de conjuntos
        self.linhas_por_conjunto = linhas_por_conjunto  # Linhas por conjunto
        self.tamanho_bloco = tamanho_bloco            # Quantidade de palavras por bloco
        self.cache = [[LinhaCache(tamanho_bloco) for _ in range(linhas_por_conjunto)] for _ in range(num_conjuntos)]
        self.acessos_recentemente = [[] for _ in range(num_conjuntos)]  # Gerenciar LRU por conjunto
        self.memoria_principal = memoria_principal    # Referência à memória principal

    def calcular_indice_conjunto(self, endereco):
        # Calcula o índice do conjunto com base no endereço
        return (endereco // self.tamanho_bloco) % self.num_conjuntos

    def calcular_tag(self, endereco):
        # Calcula a tag associada a um bloco de memória
        return endereco // (self.tamanho_bloco * self.num_conjuntos)

    def atualizar_lru(self, indice_conjunto, linha_usada):
        # Atualiza a lista de acessos recentes para o conjunto específico (LRU)
        if linha_usada in self.acessos_recentemente[indice_conjunto]:
            self.acessos_recentemente[indice_conjunto].remove(linha_usada)
        self.acessos_recentemente[indice_conjunto].append(linha_usada)

    def encontrar_linha_vazia_ou_substituir(self, indice_conjunto):
        # Encontra uma linha vazia no conjunto ou substitui a menos recentemente usada
        for i, linha in enumerate(self.cache[indice_conjunto]):
            if not linha.valido:
                return i
        # Se todas as linhas estiverem ocupadas, substitui a menos recentemente usada (LRU)
        return self.acessos_recentemente[indice_conjunto].pop(0)

    def ler(self, endereco):
        indice_conjunto = self.calcular_indice_conjunto(endereco)
        tag = self.calcular_tag(endereco)

        # Percorrer as linhas dentro do conjunto para verificar hit
        for i, linha in enumerate(self.cache[indice_conjunto]):
            if linha.valido and linha.tag == tag:
                # Hit na cache
                offset = endereco % self.tamanho_bloco
                self.atualizar_lru(indice_conjunto, i)
                return linha.dados[offset]

        # Miss na cache, buscar da memória principal
        linha_index = self.encontrar_linha_vazia_ou_substituir(indice_conjunto)
        linha = self.cache[indice_conjunto][linha_index]
        bloco_base = endereco - (endereco % self.tamanho_bloco)
        for i in range(self.tamanho_bloco):
            linha.dados[i] = self.memoria_principal.ler(bloco_base + i)
        linha.tag = tag
        linha.valido = True
        self.atualizar_lru(indice_conjunto, linha_index)
        offset = endereco % self.tamanho_bloco
        return linha.dados[offset]

    def escrever(self, endereco, valor):
        indice_conjunto = self.calcular_indice_conjunto(endereco)
        tag = self.calcular_tag(endereco)

        for i, linha in enumerate(self.cache[indice_conjunto]):
            if linha.valido and linha.tag == tag:
                # Hit na cache
                offset = endereco % self.tamanho_bloco
                linha.dados[offset] = valor
                self.memoria_principal.escrever(endereco, valor)  # Write-Through
                self.atualizar_lru(indice_conjunto, i)
                return

        # Miss na cache, carregar bloco da memória principal
        linha_index = self.encontrar_linha_vazia_ou_substituir(indice_conjunto)
        linha = self.cache[indice_conjunto][linha_index]
        bloco_base = endereco - (endereco % self.tamanho_bloco)
        for i in range(self.tamanho_bloco):
            linha.dados[i] = self.memoria_principal.ler(bloco_base + i)
        linha.tag = tag
        linha.valido = True
        offset = endereco % self.tamanho_bloco
        linha.dados[offset] = valor
        self.memoria_principal.escrever(endereco, valor)  # Write-Through
        self.atualizar_lru(indice_conjunto, linha_index)
