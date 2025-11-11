# 🤖 ROTA INTELIGENTE: Otimização de Entregas com Algoritmos de IA
## Projeto de Fundamentos de Inteligência Artificial | UniFECAF

---

## 1. 🎯 Descrição e Objetivo do Desafio

### 1.1. O Problema da Sabor Express
[cite_start]A "Sabor Express" é uma pequena empresa de delivery que opera no centro da cidade[cite: 6]. [cite_start]Atualmente, ela enfrenta grandes desafios durante os horários de pico[cite: 7]. [cite_start]As rotas são ineficientes, definidas manualmente com base apenas na experiência do entregador, o que causa atrasos, aumenta o custo de combustível e leva à insatisfação do cliente[cite: 8, 10].

### 1.2. O Objetivo da Solução
[cite_start]A missão deste projeto é desenvolver uma solução inteligente, baseada em algoritmos de Inteligência Artificial, para otimizar as entregas[cite: 11].

O projeto ataca duas frentes principais:
1.  [cite_start]**Encontrar o Menor Caminho:** Implementar um algoritmo eficiente para determinar a rota mais rápida e curta entre o restaurante e os múltiplos pontos de entrega[cite: 13].
2.  [cite_start]**Agrupamento de Pedidos:** Criar uma estratégia para agrupar pedidos próximos durante a alta demanda, otimizando o tempo de trabalho dos entregadores[cite: 14, 18].

---

## 2. 🧠 Abordagem e Algoritmos Utilizados

[cite_start]O problema foi modelado utilizando a **Teoria dos Grafos**[cite: 12], onde:
* **Nós (Nodes):** Representam o restaurante (A) e os pontos de entrega (B, C, D, E).
* **Arestas (Edges):** Representam as ruas, com pesos baseados na distância (em km) ou tempo estimado.

### 2.1. Otimização de Rota: Algoritmo de Dijkstra
Para encontrar o menor caminho entre dois pontos (Restaurante → Cliente), utilizamos o **Algoritmo de Dijkstra**.

* **Por que Dijkstra?** O Dijkstra é um algoritmo de busca eficiente, ideal para grafos com pesos positivos (como distâncias ou tempo), que garante encontrar o caminho com o custo acumulado mínimo. [cite_start]Ele é uma base fundamental para algoritmos de roteamento complexos como o $A^{*}$ (mencionado no desafio)[cite: 19].
* **Resultado:** A simulação demonstrou que a rota otimizada entre o Restaurante (A) e o ponto mais distante (E) tem uma distância total de **23 km** (A -> B -> D -> E), sendo a opção mais econômica e rápida.

### 2.2. Agrupamento de Pedidos: Algoritmo K-Means
[cite_start]Para lidar com a alta demanda e agrupar pedidos em zonas de entrega eficientes, foi utilizado o algoritmo de aprendizado não supervisionado **K-Means**[cite: 19].

* [cite_start]**Por que K-Means?** O K-Means é perfeito para o problema de *Clustering* Logístico, pois ele automaticamente encontra os centros ideais (centróides) para dividir um conjunto de dados (coordenadas de pedidos) em um número $K$ de grupos predefinidos (o número de entregadores)[cite: 32, 35].
* **Implementação:** Foram simulados 12 pedidos com coordenadas geográficas e um valor $K=3$ (para 3 entregadores).

---

## 3. 📊 Análise de Resultados e Visualização

### 3.1. Diagrama do Grafo e Dados

O grafo utilizado para o Dijkstra foi carregado a partir do arquivo `data/mapa.csv`.
| Ponto | Vizinhos e Distâncias (em km) |
| :--- | :--- |
| A | [('B', 10), ('C', 15)] |
| B | [('A', 10), ('D', 5), ('C', 2)] |
| C | [('A', 15), ('B', 2), ('E', 12)] |
| D | [('B', 5), ('E', 8)] |
| E | [('C', 12), ('D', 8)] |

### 3.2. Visualização do Agrupamento (K-Means)

O gráfico de dispersão abaixo demonstra a eficácia do K-Means ao dividir os 12 pedidos em 3 zonas (Grupos 0, 1 e 2), garantindo que cada entregador receba um conjunto de pedidos geograficamente próximos. O `X` vermelho indica o **Centróide**, ou o ponto central da zona de entrega atribuída.

![Gráfico de Agrupamento K-Means com 3 zonas de entrega](grafico_kmeans.png)
*(O arquivo `grafico_kmeans.png` está anexado na raiz do repositório)*

### 3.3. Limitações e Sugestões de Melhoria
| Categoria | Limitação da Solução Atual | Sugestão de Melhoria |
| :--- | :--- | :--- |
| **Rotas** | Utiliza o Dijkstra, que é estático (não considera tráfego em tempo real). | [cite_start]Implementar o algoritmo $A^{*}$ com uma heurística baseada em dados de tráfego em tempo real (ex: APIs de mapas), conforme a solução ORION da UPS[cite: 19, 25, 26]. |
| **Clustering** | O K-Means exige que o número de grupos ($K$) seja definido manualmente. | [cite_start]Utilizar algoritmos como **DBSCAN** ou **Programação Linear Inteira Mista (MILP)** para otimizar o agrupamento, ou o **"método do cotovelo"** para escolher o K ideal[cite: 33]. |
| **Geral** | As rotas encontradas para múltiplos pontos ainda precisam de otimização (Problema do Caixeiro Viajante - TSP). | [cite_start]Integrar os clusters do K-Means com algoritmos heurísticos avançados, como Algoritmos Genéticos ou Aprendizado por Reforço (RL), para resolver o TSP dentro de cada grupo[cite: 37, 38]. |

---

## 4. 🛠️ Instruções para Execução do Projeto

O projeto foi desenvolvido em Python.

### 4.1. Estrutura de Pastas
