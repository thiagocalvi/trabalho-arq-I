from CPU import CPU
#Esse classe é onde o simulador vai começar a executar
#nela devemos ler os dados do arquivo de instrução e começar a executar as operações
#chamando os metódos da classe CPU nas respectivas operações

class Simulador:
    def __init__(self, arquivo_instrucao) -> None:
        self.arquivo_instrucao = open(arquivo_instrucao, 'r')
        self.cpu = CPU(124)
        #Ainda tem mais coisa para colocar aqui!

        #Receber aqui tambem a configuração do tamanho de memória entre outra configurações que
        #devem ser feitas


    '''
    TO-DO: Fazer uma função para carregar o programa para memória
    Todas as instruçãoes devem estar carregadas em memória, somente depois disso o programa é executado 
    '''


    def carregar_programa(self):
        '''
        Carrega para memória as instruções do arquivo de instruções (.as)
        '''
        linha = self.ler_linha()
        self.cpu.memoriaPrincipal.escrever(self.cpu.pc.get_valor(), linha)
        while linha != None and linha != "":
            self.cpu.pc.set_valor(self.cpu.pc.get_valor() + 1) 
            self.cpu.memoriaPrincipal.escrever(self.cpu.pc.get_valor(), linha)
            linha = self.ler_linha()
        
        self.cpu.memoriaPrincipal.imprimir_memoria()
        self.cpu.pc.set_valor(0) 



    def iniciar_programa(self):
        pass

    def ler_linha(self):
        try:
            linha = self.arquivo_instrucao.readline()
            return linha
        except:
            return None
        
simulador = Simulador("./.as/add_mov.as")

simulador.carregar_programa()