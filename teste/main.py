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

class CPU:
    def __init__(self):
        self.registradores = [0] * 32
        self.pc = 0
        self.rsp = 0
        self.ra = 0
        self.of = False

class LinhaCache:
    def __init__(self, tamanho_linha):
        self.valido = False
        self.tag = None
        self.dados = [0] * (tamanho_linha // 8)  # Cada elemento representa 8 bytes

class Cache:
    def __init__(self, tamanho_linha, linhas_por_conjunto, num_conjuntos):
        if tamanho_linha % 8 != 0 or tamanho_linha > 1024:
            raise ValueError("Tamanho de linha inválido")
        
        self.tamanho_linha = tamanho_linha
        self.linhas_por_conjunto = linhas_por_conjunto
        self.num_conjuntos = num_conjuntos
        self.cache = [[LinhaCache(tamanho_linha) for _ in range(linhas_por_conjunto)] 
                      for _ in range(num_conjuntos)]
        
        self.hits = 0
        self.misses = 0

    def ler(self, endereco):
        conjunto = self.obter_conjunto(endereco)
        tag = self.obter_tag(endereco)
        offset = self.obter_offset(endereco)
        
        for linha in self.cache[conjunto]:
            if linha.valido and linha.tag == tag:
                self.hits += 1
                return linha.dados[offset // 8]
        
        self.misses += 1
        return None  # Cache miss

    def escrever(self, endereco, valor):
        conjunto = self.obter_conjunto(endereco)
        tag = self.obter_tag(endereco)
        offset = self.obter_offset(endereco)
        
        for linha in self.cache[conjunto]:
            if not linha.valido or linha.tag == tag:
                linha.valido = True
                linha.tag = tag
                linha.dados[offset // 8] = valor
                return
        
        # Se chegou aqui, o conjunto está cheio. Implementar política de substituição.
        # Por simplicidade, vamos substituir a primeira linha do conjunto.
        linha = self.cache[conjunto][0]
        linha.tag = tag
        linha.dados[offset // 8] = valor

    def obter_conjunto(self, endereco):
        return (endereco // self.tamanho_linha) % self.num_conjuntos

    def obter_tag(self, endereco):
        return endereco // (self.tamanho_linha * self.num_conjuntos)

    def obter_offset(self, endereco):
        return endereco % self.tamanho_linha

    def __str__(self):
        return f"Cache: {self.num_conjuntos} conjuntos, {self.linhas_por_conjunto} linhas por conjunto, {self.tamanho_linha} bytes por linha"

class Simulador:
    def __init__(self, tamanho_memoria, tamanho_linha_cache, linhas_por_conjunto, num_conjuntos):
        self.memoria = MemoriaPrincipal(tamanho_memoria)
        self.cache_dados = Cache(tamanho_linha_cache, linhas_por_conjunto, num_conjuntos)
        self.cache_instrucoes = Cache(tamanho_linha_cache, linhas_por_conjunto, num_conjuntos)
        self.cpu = CPU()

    def carregar_programa(self, programa):
        self.memoria.carregar_programa(programa)
        # Pré-carregar o programa na cache de instruções
        for i, instrucao in enumerate(programa):
            endereco = i * 8
            self.cache_instrucoes.escrever(endereco, instrucao)

    def executar(self):
        while self.cpu.pc < len(self.memoria.dados) * 8:
            instrucao = self.ler_instrucao(self.cpu.pc)
            self.executar_instrucao(instrucao)
            self.cpu.pc += 8  # Avança para a próxima instrução

    def ler_instrucao(self, endereco):
        instrucao = self.cache_instrucoes.ler(endereco)
        if instrucao is None:
            instrucao = self.memoria.ler(endereco)
            self.cache_instrucoes.escrever(endereco, instrucao)
        return instrucao

    def ler_dados(self, endereco):
        dados = self.cache_dados.ler(endereco)
        if dados is None:
            dados = self.memoria.ler(endereco)
            self.cache_dados.escrever(endereco, dados)
        return dados

    def escrever_dados(self, endereco, valor):
        self.cache_dados.escrever(endereco, valor)
        self.memoria.escrever(endereco, valor)

    def executar_instrucao(self, instrucao):
        # Implementação simplificada, apenas para demonstração
        opcode = instrucao >> 58
        if opcode == 0:  # add
            rd = (instrucao >> 52) & 0x1F
            rs = (instrucao >> 47) & 0x1F
            rt = (instrucao >> 42) & 0x1F
            valor1 = self.ler_dados(self.cpu.registradores[rs])
            valor2 = self.ler_dados(self.cpu.registradores[rt])
            resultado = valor1 + valor2
            self.escrever_dados(self.cpu.registradores[rd], resultado & ((1 << 64) - 1))
            self.cpu.of = resultado > 2**63 - 1 or resultado < -2**63

    def exibir_estado(self):
        print("Estado da CPU:")
        for i, reg in enumerate(self.cpu.registradores):
            print(f"r{i}: {reg}")
        print(f"PC: {self.cpu.pc}")
        print(f"RSP: {self.cpu.rsp}")
        print(f"RA: {self.cpu.ra}")
        print(f"OF: {self.cpu.of}")
        print("\nEstatísticas da Cache:")
        print(f"Cache de Dados - Hits: {self.cache_dados.hits}, Misses: {self.cache_dados.misses}")
        print(f"Cache de Instruções - Hits: {self.cache_instrucoes.hits}, Misses: {self.cache_instrucoes.misses}")

# Exemplo de uso
if __name__ == "__main__":
    # Cria um simulador com 1MB de memória e cache de 4KB (64 bytes por linha, 4 linhas por conjunto, 16 conjuntos)
    simulador = Simulador(1024 * 1024, 64, 4, 16)

    # Programa de exemplo (instruções fictícias de 64 bits)
    programa = [
        0x0000000000000000,  # add r1, r2, r3
        0x0100000000000000,  # sub r4, r5, r6
        0x0200000000000000,  # mul r7, r8, r9
    ]

    simulador.carregar_programa(programa)
    print(simulador.memoria)
    print(simulador.cache_dados)
    print(simulador.cache_instrucoes)

    # Configura alguns valores nos registradores para teste
    simulador.cpu.registradores[2] = 10
    simulador.cpu.registradores[3] = 20

    # Executa o programa
    simulador.executar()



    # Exibe o estado final
    simulador.exibir_estado()