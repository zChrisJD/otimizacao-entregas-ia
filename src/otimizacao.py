"""
Projeto: Rota Inteligente - Otimização de Entregas "Sabor Express"
Disciplina: Artificial Intelligence Fundamentals
Autor: [Seu Nome Aqui]

Este script contém a implementação de duas soluções de IA:
1. Algoritmo de Dijkstra: Para encontrar a rota mais curta (menor distância) 
   entre o restaurante e um ponto de entrega, usando um grafo.
2. Algoritmo K-Means: Para agrupar múltiplos pedidos em "zonas"
   para otimizar a alocação de entregadores.
"""

import csv
from collections import defaultdict
import heapq
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import os
import sys

# --- PARTE 1: ALGORITMO DE DIJKSTRA (OTIMIZAÇÃO DE ROTA) ---

def carregar_grafo(caminho_arquivo):
    """
    Lê um arquivo CSV de mapa e o transforma em um grafo (lista de adjacência).
    Assume que as rotas são de mão dupla.
    """
    grafo = defaultdict(list)
    
    # Verifica se o caminho do arquivo existe
    if not os.path.exists(caminho_arquivo):
        print(f"Erro: Arquivo de mapa não encontrado em '{caminho_arquivo}'")
        return None
        
    try:
        with open(caminho_arquivo, mode='r', encoding='utf-8') as arquivo:
            leitor_csv = csv.reader(arquivo)
            next(leitor_csv) # Pula cabeçalho
            
            for linha in leitor_csv:
                if len(linha) == 3:
                    origem, destino, distancia = linha
                    distancia = int(distancia)
                    grafo[origem].append((destino, distancia))
                    grafo[destino].append((origem, distancia))
                
    except Exception as e:
        print(f"Erro ao ler o arquivo de mapa: {e}")
        return None
    
    print(f"✔️ Grafo carregado com sucesso de '{caminho_arquivo}'")
    return dict(grafo)

def algoritmo_dijkstra(grafo, ponto_partida):
    """
    Executa o Algoritmo de Dijkstra para encontrar o menor caminho
    a partir de um 'ponto_partida' para TODOS os outros pontos.
    """
    distancias = {ponto: float('inf') for ponto in grafo}
    caminho_anterior = {ponto: None for ponto in grafo}
    distancias[ponto_partida] = 0
    
    fila_prioridade = [(0, ponto_partida)] # (distancia_acumulada, ponto)
    
    while fila_prioridade:
        distancia_atual, ponto_atual = heapq.heappop(fila_prioridade)
        
        if distancia_atual > distancias[ponto_atual]:
            continue
            
        for vizinho, peso in grafo[ponto_atual]:
            nova_distancia = distancia_atual + peso
            
            if nova_distancia < distancias[vizinho]:
                distancias[vizinho] = nova_distancia
                caminho_anterior[vizinho] = ponto_atual
                heapq.heappush(fila_prioridade, (nova_distancia, vizinho))
                
    return distancias, caminho_anterior

def reconstruir_caminho(caminho_anterior, ponto_partida, ponto_chegada):
    """
    Usa o resultado do Dijkstra para montar a lista do caminho.
    """
    caminho = []
    ponto_atual = ponto_chegada
    
    while ponto_atual is not None:
        caminho.append(ponto_atual)
        ponto_atual = caminho_anterior[ponto_atual]
    
    caminho.reverse()
    
    if caminho and caminho[0] == ponto_partida:
        return caminho
    else:
        return None # Nenhum caminho encontrado

def executar_simulacao_rota(arquivo_mapa, partida, chegada):
    """
    Função principal para executar a otimização de rota.
    """
    print("\n--- 🚀 INICIANDO SIMULAÇÃO DE ROTA (DIJKSTRA) ---")
    mapa_sabor_express = carregar_grafo(arquivo_mapa)
    
    if mapa_sabor_express:
        # Valida se os pontos existem no grafo
        if partida not in mapa_sabor_express or chegada not in mapa_sabor_express:
            print(f"Erro: Ponto de partida '{partida}' ou chegada '{chegada}' não existe no mapa.")
            return

        distancias, caminho_anterior = algoritmo_dijkstra(mapa_sabor_express, partida)
        caminho_encontrado = reconstruir_caminho(caminho_anterior, partida, chegada)
        
        if caminho_encontrado:
            distancia_total = distancias[chegada]
            print(f"📍 Rota Mais Rápida (Dijkstra) de '{partida}' para '{chegada}':")
            print(f"   Distância Total: {distancia_total} km")
            print(f"   Caminho: {' -> '.join(caminho_encontrado)}")
        else:
            print(f"Não foi possível encontrar um caminho de '{partida}' para '{chegada}'.")

# --- PARTE 2: ALGORITMO K-MEANS (AGRUPAMENTO DE PEDIDOS) ---

def executar_agrupamento_pedidos(arquivo_pedidos, num_entregadores, gerar_grafico=True):
    """
    Função principal para agrupar pedidos em zonas usando K-Means.
    """
    print("\n---  clustering INICIANDO AGRUPAMENTO DE PEDIDOS (K-MEANS) ---")
    
    # Verifica se o arquivo existe
    if not os.path.exists(arquivo_pedidos):
        print(f"Erro: Arquivo de pedidos não encontrado em '{arquivo_pedidos}'")
        return
        
    try:
        df_pedidos = pd.read_csv(arquivo_pedidos)
        
        if 'Local_X' not in df_pedidos.columns or 'Local_Y' not in df_pedidos.columns:
            print("Erro: CSV de pedidos deve conter colunas 'Local_X' e 'Local_Y'")
            return
            
        coordenadas = df_pedidos[['Local_X', 'Local_Y']].values
        
        print(f"Agrupando {len(coordenadas)} pedidos para {num_entregadores} entregadores...")

        kmeans = KMeans(n_clusters=num_entregadores, n_init=10, random_state=42)
        kmeans.fit(coordenadas)
        
        grupos_atribuidos = kmeans.labels_
        centros_dos_grupos = kmeans.cluster_centers_
        
        df_pedidos['Grupo_Entrega'] = grupos_atribuidos
        
        print("\n--- Resultados do Agrupamento ---")
        print(df_pedidos)
        
        if gerar_grafico:
            print("\nGerando gráfico de agrupamento...")
            plt.figure(figsize=(10, 7))
            
            # Plota os pedidos
            scatter = plt.scatter(coordenadas[:, 0], coordenadas[:, 1], c=grupos_atribuidos, cmap='viridis', s=100, alpha=0.7, label='Pedidos')
            
            # Plota os centros
            plt.scatter(centros_dos_grupos[:, 0], centros_dos_grupos[:, 1], c='red', s=250, marker='X', label='Centro do Grupo (Zona)')
            
            # Plota o restaurante (localização fictícia)
            plt.scatter(50, 50, c='black', s=200, marker='s', label='Restaurante (Sabor Express)')
            
            plt.title('Agrupamento de Pedidos "Sabor Express" (K-Means)')
            plt.xlabel('Coordenada X (Leste-Oeste)')
            plt.ylabel('Coordenada Y (Norte-Sul)')
            plt.legend()
            plt.grid(True, linestyle='--', alpha=0.5)
            
            # Salva o gráfico em um arquivo
            caminho_output = 'outputs'
            if not os.path.exists(caminho_output):
                os.makedirs(caminho_output)
            
            nome_grafico = os.path.join(caminho_output, 'agrupamento_kmeans.png')
            plt.savefig(nome_grafico)
            print(f"Gráfico salvo em '{nome_grafico}'")
            # plt.show() # Desabilitado para rodar em servidor
            
    except Exception as e:
        print(f"Ocorreu um erro no K-Means: {e}")


# --- EXECUÇÃO PRINCIPAL (MAIN) ---

if __name__ == "__main__":
    """
    Este bloco será executado quando o script for chamado diretamente.
    Ele espera argumentos da linha de comando para decidir o que fazer.
    Ex: python src/otimizacao.py rota
        python src/otimizacao.py cluster
        python src/otimizacao.py tudo
    """
    
    # Caminhos padrão para os arquivos de dados
    ARQUIVO_MAPA = 'data/mapa.csv'
    ARQUIVO_PEDIDOS = 'data/pedidos.csv'
    
    # Argumentos da linha de comando
    # sys.argv[0] é o nome do script
    # sys.argv[1] é o primeiro argumento
    modo = "tudo" # Padrão
    if len(sys.argv) > 1:
        modo = sys.argv[1]

    print("==============================================")
    print("🤖 SISTEMA DE OTIMIZAÇÃO 'SABOR EXPRESS' 🤖")
    print("==============================================")

    if modo == "rota" or modo == "tudo":
        # Simulação de Rota: Do Restaurante (A) para o Cliente (E)
        executar_simulacao_rota(ARQUIVO_MAPA, partida='A', chegada='E')

    if modo == "cluster" or modo == "tudo":
        # Simulação de Agrupamento: 3 entregadores
        executar_agrupamento_pedidos(ARQUIVO_PEDIDOS, num_entregadores=3, gerar_grafico=True)

    if modo != "rota" and modo != "cluster" and modo != "tudo":
        print(f"Modo '{modo}' desconhecido. Use 'rota', 'cluster' ou 'tudo'.")
