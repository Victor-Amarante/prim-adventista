import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from math import inf

def adjacentes(v, G):
    (V, E, w) = G
    adj = []
    for aresta in E: 
        (pred, suc) = aresta 
        if v == pred: 
            adj.append(suc) 
    return adj 

def retire_vertice_menor_chave(Q):
    menor_vertice = list(Q.keys())[0]
    menor_chave   = Q[menor_vertice]

    for vertice in Q:
        chave = Q[vertice]
        if chave < menor_chave:
            menor_chave   = chave
            menor_vertice = vertice

    chave_x_valor = Q.pop(menor_vertice)
    return menor_vertice

def Prim(G, E, raiz, W):
    (V,E,w) = G
    chave = {}
    predecessor = {}
    for v in V:
        chave[v] = inf
        predecessor[v] = ''

    chave[raiz] = 0
    Q = {v:chave[v] for v in V}
    while len(Q) > 0:
        v = retire_vertice_menor_chave(Q)
        for u in adjacentes(v, G):
            if u in Q and w(v,u, W) < chave[u]:
                predecessor[u] = v
                chave[u] = w(v,u, W)
                Q[u] = chave[u]

    return predecessor, chave

def w(u, v, W):
    return W[(u, v)]


st.set_page_config(page_title='Algoritmo do Prim')
def main():
    st.title("Aplicação de Algoritmo de Prim em Grafos")

    # Adicionar upload de arquivo CSV
    st.markdown("""É necessário que a base de dados tenha as seguintes variáveis em ordem:
                origem, destino, peso""")
    file = st.file_uploader("Carregar arquivo CSV", type=["csv"])
    if file is not None:
        df = pd.read_csv(file)
        
        V = list(set(df['origem'].tolist() + df['destino'].tolist()))
        E = [(row['origem'], row['destino']) for index, row in df.iterrows()]
        W = {(row['origem'], row['destino']): row['peso'] for index, row in df.iterrows()}
        G = (V, E, w)

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
