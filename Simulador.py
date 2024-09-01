from CPU import CPU
#Esse classe é onde o simulador vai começar a executar
#nela devemos ler os dados do arquivo de instrução e começar a executar as operações
#chamando os metódos da classe CPU nas respectivas operações

class Simulador:
    def __init__(self, arquivo_instrucao) -> None:
        self.arquivo_instrucao = open(arquivo_instrucao, 'r')
        self.cpu = CPU(1024)
        #Ainda tem mais coisa para colocar aqui!

        #Receber aqui tambem a configuração do tamanho de memória entre outra configurações que
        #devem ser feitas

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
        
# simulador = Simulador("./.as/add_mov.as")
simulador = Simulador("./.as/loop_mem.as")

simulador.carregar_programa()
simulador.iniciar_execucao()