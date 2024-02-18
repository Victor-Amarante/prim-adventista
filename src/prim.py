import pandas as pd
from math import inf
import numpy as np

# abrimos a base de dados de teste
# -- VARIAVEL: COLOCAR A BASE DE DADOS ESCOLHIDA
df = pd.read_csv('data/dados-teste.csv')

# criamos uma lista de vertices da base de dados
V = list(set(df['origem'].tolist() + df['destino'].tolist()))

# criamos uma lista de arestas da base de dados
E = [(row['origem'], row['destino']) for index, row in df.iterrows()]

# criamos uma lista de pesos das arestas do grafo
W = df['peso'].tolist()

# criamos uma funcao para localizar os vertices adjacentes ao vertice atual
def adjacentes(v, G):
    (V, E, w) = G
    adj = []
    for aresta in E: 
        (pred, suc) = aresta 
        if v == pred: 
            adj.append(suc) 
    return adj 

# criamos uma funcao para retirar o vertice de menor chave de Q
def retire_vertice_menor_chave(Q):
    menor_vertice = list(Q.keys())[0]
    menor_chave   = Q[menor_vertice]

    # buscamos pela menor chave
    for vertice in Q:
        chave = Q[vertice]
        if chave < menor_chave:
            menor_chave   = chave
            menor_vertice = vertice
    
    chave_x_valor = Q.pop(menor_vertice)
    return menor_vertice

# criamos a funcao Prim para aplicar o algoritmo de Prim recebendo um grafo, um conjunto de arestas ponderadas e uma raiz escolhida para iniciar
def Prim(G, E, raiz):
    (V,E,w) = G
    chave = {}
    predecessor = {}
    
    # inicializando as chaves e os seus predecessores com valores de infinito e nulo, respectivamente
    for v in V:
        chave[v] = inf
        predecessor[v] = ''
    
    # inicializamos a raiz com valor 0
    chave[raiz] = 0
    
    # ordenamos uma fila com vertices ordenados pelos pesos de cada vertice dentro do conjunto de vertices do grafo
    Q = {v:chave[v] for v in V}
    
    # enquanto nossa fila nao estiver vazia, atualize os valores das chaves e dos predecessores
    while len(Q) > 0:
        v = retire_vertice_menor_chave(Q)
        for u in adjacentes(v, G):
            if u in Q and w(v,u) < chave[u]:
                predecessor[u] = v
                chave[u] = w(v,u)
                Q[u] = chave[u]

    return predecessor, chave

# criamos uma funcao para retornar o peso de uma aresta
def w(u, v):
    return W[E.index((u, v))]

G = (V, E, w)  # grafo no formato (V, E, w) => conjunto de vertices, conjunto de arestas, conjunto de pesos de cada aresta

# chamamos o algoritmo de Prim com raiz 'A'
predecessor, chave = Prim(G, E , 'A')

# organizamos a saida das chaves e predecessores
predecessor_sorted = dict(sorted(predecessor.items()))
chave_sorted = dict(sorted(chave.items()))

print("Predecessor:", predecessor_sorted)
print("Chave:", chave_sorted)