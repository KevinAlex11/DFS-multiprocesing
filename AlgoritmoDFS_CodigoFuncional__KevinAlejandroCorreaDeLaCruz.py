import matplotlib.pyplot as plt
import random
import multiprocessing

def crear_grafo():
    grafo = {}
    for nivel in range(1, 8):
        for nodo in range(1, nivel + 1):
            nodo_actual = nivel * 10 + nodo  # Números únicos para cada nodo
            vecinos = []
            if nivel < 7:
                vecinos.append((nivel + 1) * 10 + nodo)  # Conectar con el nodo del siguiente nivel
                vecinos.append((nivel + 1) * 10 + nodo + 1)  # Conectar con el nodo del siguiente nivel y a la derecha
            if nodo > 1:
                vecinos.append((nivel - 1) * 10 + nodo - 1)  # Conectar con el nodo del nivel anterior y a la izquierda
            if nodo < nivel:
                vecinos.append((nivel - 1) * 10 + nodo)  # Conectar con el nodo del nivel anterior
            grafo[nodo_actual] = vecinos
    return grafo

def dfs(grafo, inicio, objetivo, visitados, camino_actual, camino_mas_corto):
    if inicio == objetivo:
        camino_mas_corto.extend(camino_actual)
        return True
    
    visitados.add(inicio)
    camino_actual.append(inicio)
    
    for vecino in grafo[inicio]:
        if vecino not in visitados:
            if dfs(grafo, vecino, objetivo, visitados, camino_actual, camino_mas_corto):
                return True
                
    camino_actual.pop()
    return False

def encontrar_camino_mas_corto(grafo, inicio, objetivo):
    camino_mas_corto = []
    visitados = set()
    dfs(grafo, inicio, objetivo, visitados, [], camino_mas_corto)
    return camino_mas_corto

def dfs_paralelo(grafo, inicio, objetivo, resultado):
    camino_mas_corto = encontrar_camino_mas_corto(grafo, inicio, objetivo)
    resultado.put(camino_mas_corto)

def crear_grafo_visual(grafo, posicion_nodos):
    plt.figure(figsize=(10, 8))
    for nodo, posicion in posicion_nodos.items():
        plt.plot(posicion[0], posicion[1], 'o', markersize=15, markerfacecolor='lightblue')
        plt.text(posicion[0], posicion[1] + 0.3, str(nodo), ha='center', va='center', fontsize=12)
    for nodo, vecinos in grafo.items():
        for vecino in vecinos:
            x = [posicion_nodos[nodo][0], posicion_nodos[vecino][0]]
            y = [posicion_nodos[nodo][1], posicion_nodos[vecino][1]]
            plt.plot(x, y, 'b-', linewidth=1)
    plt.title('Grafo')
    plt.axis('off')
    plt.show()

if __name__ == "__main__":
    grafo = crear_grafo()
    inicio = 11
    objetivo = 71
    
    # Crear posiciones aleatorias para los nodos
    posicion_nodos = {}
    for nodo in grafo.keys():
        posicion_nodos[nodo] = (random.uniform(0, 10), random.uniform(0, 10))
    
    # Visualizar el grafo
    crear_grafo_visual(grafo, posicion_nodos)
    
    # Ejecución secuencial
    camino_mas_corto_secuencial = encontrar_camino_mas_corto(grafo, inicio, objetivo)
    print("Camino más corto (secuencial):", camino_mas_corto_secuencial)
    
    # Ejecución paralela
    resultado = multiprocessing.Queue()
    procesos = []
    for _ in range(multiprocessing.cpu_count()):
        proceso = multiprocessing.Process(target=dfs_paralelo, args=(grafo, inicio, objetivo, resultado))
        proceso.start()
        procesos.append(proceso)
    
    for proceso in procesos:
        proceso.join()
    
    caminos_paralelos = [resultado.get() for _ in range(len(procesos))]
    camino_mas_corto_paralelo = min(caminos_paralelos, key=len)
    print("Camino más corto (paralelo):", camino_mas_corto_paralelo)
    
    # Visualizar el camino más corto
    plt.figure(figsize=(10, 8))
    for nodo, posicion in posicion_nodos.items():
        plt.plot(posicion[0], posicion[1], 'o', markersize=15, markerfacecolor='lightblue')
        plt.text(posicion[0], posicion[1] + 0.3, str(nodo), ha='center', va='center', fontsize=12)
    for i in range(len(camino_mas_corto_paralelo) - 1):
        nodo_origen = camino_mas_corto_paralelo[i]
        nodo_destino = camino_mas_corto_paralelo[i + 1]
        x = [posicion_nodos[nodo_origen][0], posicion_nodos[nodo_destino][0]]
        y = [posicion_nodos[nodo_origen][1], posicion_nodos[nodo_destino][1]]
        plt.plot(x, y, 'r-', linewidth=2)
    plt.title('Camino más corto')
    plt.axis('off')
    plt.show()

