#by: @thiagocalvi

'''
Esse uma implementação generalista da memória cache, como temos que fazer uma memoria cache de dados e
outra de instruções podemos criar duas instancias dessa classe, uma cache_dados e outra cache_instrucoes
'''

class LinhaCache:
    def __init__(self, tamanho_bloco):
        self.tag = None                  #Tag usada para identificar o bloco
        self.dados = [0] * tamanho_bloco #Bloco de dados
        self.valido = False              #Indica se a linha é valida

class MemoriaCache:
    def __init__(self, num_linhas, tamanho_bloco):
        self.num_linhas = num_linhas #Quantidade de linhas da cache
        self.tamanho_bloco = tamanho_bloco  #Quantidade de palavras por bloco
        #Não sei se estou calculando certo o tamanho da chache, talvez esteja errado!
        self.cache = [LinhaCache(tamanho_bloco) for _ in range(num_linhas)] #Inicializa a cache

    def calcular_indice(self, endereco):
        #Recebe o endereço de memória e calcula qual linha será acessada
        return (endereco // self.tamanho_bloco) % self.num_linhas

    def calcular_tag(self, endereco):
        '''
        Calcula a tag associada a um bloco de memória
        Tag serve para identificar se os dados armazenados em 
        uma linha de cache pertencem ao bloco de memória correto
        '''
        return endereco // (self.tamanho_bloco * self.num_linhas)

    def ler(self, endereco):
        '''
        Acessar um dado armazenado em um endereço específico na memória. 
        Verifica se o dado está presente na cache. Se o dado estiver na cache (hit), 
        ele é retornado. Caso contrário (miss), nesse caso buscar os dados na memória principal
        '''
        indice = self.calcular_indice(endereco)
        tag = self.calcular_tag(endereco)
        linha = self.cache[indice]

        if linha.valido and linha.tag == tag:
            #Hit na cache
            offset = endereco % self.tamanho_bloco
            #Retorna o dado
            return linha.dados[offset]
        else:
            #Miss na cache
            return None  #Buscar da memória principal, provavelmente essa implementação não será feita aqui
            #Posivelmente implementar um rotina na classe CPU 

    def escrever(self, endereco, valor):
        '''
        Serve para inserir ou atualizar dados em um endereço específico na memória cache. 
        Ela garante que o dado seja escrito na cache (e na memória principal, dependendo da política de escrita).
        Uma sugestão de política de escrita é o Write-Through, sempre que um dado é atualizado na cache, ele também é imediatamente escrito na memória principal.
        
        !!!!! Nessa implementação não tem nenhuma política de escrita e nem de substituição !!!!!
        TO-DO: Definir uma política de escrita e substituição e implementar
        '''
        indice = self.calcular_indice(endereco)
        tag = self.calcular_tag(endereco)
        linha = self.cache[indice]

        if linha.valido and linha.tag == tag:
            #Hit na cache
            offset = endereco % self.tamanho_bloco
            linha.dados[offset] = valor
        else:
            #Miss na cache, carregar bloco da memória principal
            linha.tag = tag
            linha.valido = True
            offset = endereco % self.tamanho_bloco
            linha.dados[offset] = valor
