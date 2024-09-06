'''
EXECUTAR ESSE ARQUIVO PARA INICIAR A SIMULAÇÃO
Dependencias:
    - Cache.py
    - CPU.py
    - MemoriaPrincipal
    - Registrador.py
'''
from CPU import CPU

class Configuracao:
    def __init__(self):
        self.tamanho_bloco = self.receber_tamanho_bloco()
        self.linhas_por_conjunto = self.receber_linhas_por_conjunto()
        self.num_conjuntos = self.receber_num_conjuntos()
        self.tamanho_total_cache = self.calcular_tamanho_total_cache()
        self.tamanho_memoria_principal = self.receber_tamanho_memoria_principal()

    def receber_tamanho_bloco(self):
        while True:
            tamanho_bloco = int(input("Digite o número de bytes por linha (múltiplo de 8, máximo 1024): "))
            if tamanho_bloco % 8 == 0 and tamanho_bloco <= 1024:
                return tamanho_bloco
            else:
                print("Valor inválido. Certifique-se de que é múltiplo de 8 e não excede 1024 bytes.")

    def receber_linhas_por_conjunto(self):
        linhas_por_conjunto = int(input("Digite o número de linhas por conjunto: "))
        return linhas_por_conjunto

    def receber_num_conjuntos(self):
        num_conjuntos = int(input("Digite o número de conjuntos: "))
        return num_conjuntos

    def calcular_tamanho_total_cache(self):
        return self.tamanho_bloco * self.linhas_por_conjunto * self.num_conjuntos

    def receber_tamanho_memoria_principal(self):
        while True:
            tamanho_memoria_principal = int(input(f"Digite o tamanho da memória principal em bytes (múltiplo de 8, maior que {self.tamanho_total_cache}): "))
            if tamanho_memoria_principal % 8 == 0 and tamanho_memoria_principal > self.tamanho_total_cache:
                return tamanho_memoria_principal
            else:
                print(f"Valor inválido. Certifique-se de que é múltiplo de 8 e maior que {self.tamanho_total_cache} bytes.")


class Simulador:
    def __init__(self, arquivo_instrucao) -> None:
        self.arquivo_instrucao = open(arquivo_instrucao, 'r')
        self.configuracao = Configuracao()
        self.cpu = CPU(self.configuracao.tamanho_memoria_principal, self.configuracao.num_conjuntos, self.configuracao.linhas_por_conjunto, self.configuracao.tamanho_bloco)

    def carregar_programa(self):
        '''
        Carrega para memória as instruções do arquivo de instruções (.as)
        '''
        endereco_atual = self.cpu.pc.get_valor()
        linha = self.ler_linha()

        while linha is not None and linha != "":
            # Converte a instrução para um formato de 64 bits se necessário
            # Aqui assumimos que 'linha' já está no formato correto para armazenamento de 64 bits
            self.cpu.memoria_principal.escrever(endereco_atual, linha)

            # Incrementa o PC para a próxima posição
            endereco_atual += 1  # Incremento por 1, já que estamos tratando 64 bits por posição

            # Atualiza o PC na CPU
            self.cpu.pc.set_valor(endereco_atual)

            # Lê a próxima linha de instrução
            linha = self.ler_linha()

        # Reseta o PC após carregar o programa e max_pc recebe o valor maximo de pc
        self.cpu.max_pc = self.cpu.pc.get_valor()
        self.cpu.pc.set_valor(0)
        self.cpu.rsp.set_valor(self.cpu.max_pc * 4) #inicio da pilha na memoria

    def iniciar_execucao(self):
        self.cpu.executar()

    def ler_linha(self):
        try:
            linha = self.arquivo_instrucao.readline()
            return linha
        except:
            return None
        
file_path = input("Informe o nome/caminho do arquivo de opereções .as: ")
simulador = Simulador(file_path)
simulador.carregar_programa()
simulador.iniciar_execucao()