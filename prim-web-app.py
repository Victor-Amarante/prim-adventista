import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from math import inf

from typing import List, Tuple


def procurar_adjacentes(vertice_atual:str, grafo:Tuple) -> List:
    """Procura os vértices adjacentes ao vértice atual
    Args:
        vertice_atual (str): Vértice atual
        grafo (Tuple): Grafo

    Returns:
        List: Lista de vértices adjacentes
    """
    (_, arestas, _) = grafo
    adj = []
    for aresta in arestas: 
        (pred, suc) = aresta 
        if vertice_atual == pred: 
            adj.append(suc) 
    return adj 

def retire_vertice_menor_chave(vertices_ordenados:dict) -> str:
    """Retira o vértice de menor chave da lista de vértices ordenados

    Args:
        vertices_ordenados (dict): Dicionário com os pesos e seus vértices

    Returns:
        str: Vértice de menor chave
    """
    menor_vertice = list(vertices_ordenados.keys())[0]
    menor_peso = vertices_ordenados[menor_vertice]

    for vertice in vertices_ordenados:
        chave = vertices_ordenados[vertice]
        if chave < menor_peso:
            menor_peso = chave
            menor_vertice = vertice
    
    vertices_ordenados.pop(menor_vertice)
    return menor_vertice

def Prim(grafo:Tuple, raiz:str, pesos:List) -> Tuple:
    """Aplica o algoritmo de Prim em um grafo

    Args:
        grafo (Tuple): Grafo a ser analisado
        raiz (str): Vértice raiz
        pesos (List): Pesos das arestas

    Returns:
        Tuple: Predecessores e chaves
    """
    
    (vertices, arestas, pesos) = grafo
    custos = {}
    predecessor = {}
    for vertice in vertices:
        custos[vertice] = inf
        predecessor[vertice] = ''

    custos[raiz] = 0
    vertices_ordenados = {vertice:custos[vertice] for vertice in vertices}
    while vertices_ordenados:
        vertice = retire_vertice_menor_chave(vertices_ordenados)
        for vertice_adjacente in procurar_adjacentes(vertice, grafo):
            if vertice_adjacente in vertices_ordenados and retornar_peso_aresta(vertice,vertice_adjacente, pesos) < custos[vertice_adjacente]:
                predecessor[vertice_adjacente] = vertice
                custos[vertice_adjacente] = retornar_peso_aresta(vertice,vertice_adjacente, pesos)
                vertices_ordenados[vertice_adjacente] = custos[vertice_adjacente]

    return predecessor, custos

def retornar_peso_aresta(vertice, vertice_adjacente, pesos):
    """Retorna o peso da aresta entre dois vértices

    Args:
        vertice (_type_): Vertice Alvo
        vertice_adjacente (_type_): Vertice Adjacente
        pesos (_type_): Pesos das arestas

    Returns:
        _type_: Peso da aresta do vertice ao vertice adjacente
    """
    return pesos[(vertice, vertice_adjacente)]


st.set_page_config(page_title='Algoritmo do Prim')

def main():
    st.title("Aplicação de Algoritmo de Prim em Grafos")

    # Adicionar upload de arquivo CSV
    st.markdown("É necessário que a base de dados tenha as seguintes variáveis em ordem:\norigem, destino, peso")
    file = st.file_uploader("Carregar arquivo CSV", type=["csv"])
    if file is not None:
        df = pd.read_csv(file)
        
        V = list(set(df['origem'].tolist() + df['destino'].tolist()))
        E = [(row['origem'], row['destino']) for index, row in df.iterrows()]
        W = {(row['origem'], row['destino']): row['peso'] for index, row in df.iterrows()}
        G = (V, E, W)

        # Aplicar algoritmo de Prim
        raiz = st.selectbox("Selecione a raiz:", sorted(V))
        if raiz:
            predecessor, chave = Prim(G, E, raiz, W)
            
            predecessor_sorted = dict(sorted(predecessor.items()))
            chave_sorted = dict(sorted(chave.items()))
            
            st.markdown('## Lista de Predecessores:')
            st.markdown(f"Predecessor: {predecessor_sorted}")
            st.markdown('## Lista de Custos para chegar ao vértice:')
            st.markdown(f"Chave: {chave_sorted}")
            # Criar grafo original
            G_original = nx.Graph()
            G_original.add_edges_from(E)
            plt.figure(figsize=(8, 6))
            pos = nx.spring_layout(G_original)
            nx.draw(G_original, pos, with_labels=True, node_size=700, node_color='skyblue', font_size=10, font_weight='bold', width=2, edge_color='gray')
            st.pyplot(plt)
            # Criar grafo mínimo
            G_minimo = nx.Graph()
            for u, v in predecessor.items():
                if v != '':
                    G_minimo.add_edge(v, u, weight=W[(v, u)])
            plt.figure(figsize=(8, 6))
            pos = nx.spring_layout(G_minimo)
            nx.draw(G_minimo, pos, with_labels=True, node_size=700, node_color='lightgreen', font_size=10, font_weight='bold', width=2, edge_color='green')
            st.pyplot(plt)
            


if __name__ == "__main__":
    main()
