import csv
from geopy.distance import geodesic

# Função para calcular a distância entre duas coordenadas geográficas
def calcular_distancia(coord1, coord2):
    return geodesic(coord1, coord2).kilometers

# Carregar os dados do CSV de entrada
def carregar_dados(arquivo):
    dados = []
    with open(arquivo, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            dados.append({
                'nome': row['Nome_Colegio'],
                'coordenadas': (float(row['Latitude']), float(row['Longitude']))
            })
    return dados

# Função para encontrar o colégio mais próximo
def encontrar_mais_proximo(colegio, colegios):
    distancias = [(outro['nome'], calcular_distancia(colegio['coordenadas'], outro['coordenadas'])) for outro in colegios if outro['nome'] != colegio['nome']]
    distancias.sort(key=lambda x: x[1])
    return distancias[0]

# Carregar os dados dos colégios
colegios = carregar_dados('escolas.csv')

# Conjunto para armazenar conexões já registradas
conexoes_registradas = set()

# Criar conexões entre os colégios
conexoes = []
for colegio in colegios:
    # Encontrar o colégio mais próximo, se estiver isolado
    DISTANCIA_MINIMA = 100
    if all(calcular_distancia(colegio['coordenadas'], outro['coordenadas']) > DISTANCIA_MINIMA for outro in colegios if outro['nome'] != colegio['nome']):
        destino, distancia = encontrar_mais_proximo(colegio, colegios)
        # Adicionar conexão apenas se não estiver registrada
        conexao = tuple(sorted([colegio['nome'], destino]))
        if conexao not in conexoes_registradas:
            conexoes.append({'origem': colegio['nome'], 'destino': destino, 'peso': distancia})
            conexoes_registradas.add(conexao)
    else:
        # Conectar com colégios dentro do raio de 300km
        for outro in colegios:
            if outro['nome'] != colegio['nome'] and calcular_distancia(colegio['coordenadas'], outro['coordenadas']) <= DISTANCIA_MINIMA:
                # Adicionar conexão apenas se não estiver registrada
                conexao = tuple(sorted([colegio['nome'], outro['nome']]))
                if conexao not in conexoes_registradas:
                    conexoes.append({'origem': colegio['nome'], 'destino': outro['nome'], 'peso': calcular_distancia(colegio['coordenadas'], outro['coordenadas'])})
                    conexoes_registradas.add(conexao)

# Escrever os dados no CSV de saída
with open('conexoes.csv', 'w', newline='') as csvfile:
    fieldnames = ['origem', 'destino', 'peso']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for conexao in conexoes:
        writer.writerow(conexao)

