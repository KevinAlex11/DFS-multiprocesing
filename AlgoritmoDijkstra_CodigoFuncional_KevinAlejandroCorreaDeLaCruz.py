import networkx as nx
import matplotlib.pyplot as plt

def create_graph(levels):
    graph = {}
    total_nodes = 1
    for i in range(levels):
        level_nodes = i + 1
        for j in range(level_nodes):
            node = f"Nodo_{total_nodes}"
            total_nodes += 1
            neighbors = []
            if i > 1:  # Conectar con nodos del nivel anterior
                prev_level_start = total_nodes - level_nodes - 1
                for k in range(level_nodes):
                    prev_node = f"Nodo_{prev_level_start + k}"
                    neighbors.append(prev_node)
            graph[node] = neighbors
    return graph

def shortest_path(graph, start, end):
    try:
        return nx.shortest_path(graph, start, end)
    except nx.NetworkXNoPath:
        return None

def print_shortest_path(shortest_path):
    if shortest_path:
        print("El camino más corto es:", shortest_path)
    else:
        print("No se encontró un camino entre los nodos especificados.")

if __name__ == '__main__':
    # Crear el grafo
    graph = create_graph(7)
    print("Grafo:", graph)

    # Visualizar el grafo
    G = nx.Graph()
    for node, neighbors in graph.items():
        G.add_node(node)
        for neighbor in neighbors:
            G.add_edge(node, neighbor)

    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=700, node_color="skyblue", font_size=10, font_weight="bold")
    plt.title("Grafo")
    plt.show()

    # Prueba del algoritmo de búsqueda de camino más corto
    start_node = "Nodo_1"
    end_node = "Nodo_27"
    shortest_path = shortest_path(G, start_node, end_node)
    print_shortest_path(shortest_path)