"""Todos los posibles caminos para las distintas ciudades"""

GRAFO = {\
            'Arad': {'Sibiu': 140, 'Zerind': 75, 'Timisoara': 118},\
            'Zerind': {'Arad': 75, 'Oradea': 71},\
            'Oradea': {'Zerind': 71, 'Sibiu': 151},\
            'Sibiu': {'Arad': 140, 'Oradea': 151, 'Fagaras': 99, 'Rimnicu': 80},\
            'Timisoara': {'Arad': 118, 'Lugoj': 111},\
            'Lugoj': {'Timisoara': 111, 'Mehadia': 70},\
            'Mehadia': {'Lugoj': 70, 'Drobeta': 75},\
            'Drobeta': {'Mehadia': 75, 'Craiova': 120},\
            'Craiova': {'Drobeta': 120, 'Rimnicu': 146, 'Pitesti': 138},\
            'Rimnicu': {'Sibiu': 80, 'Craiova': 146, 'Pitesti': 97},\
            'Fagaras': {'Sibiu': 99, 'Bucharest': 211},\
            'Pitesti': {'Rimnicu': 97, 'Craiova': 138, 'Bucharest': 101},\
            'Bucharest': {'Fagaras': 211, 'Pitesti': 101, 'Giurgiu': 90, 'Urziceni': 85},\
            'Giurgiu': {'Bucharest': 90},\
            'Urziceni': {'Bucharest': 85, 'Vaslui': 142, 'Hirsova': 98},\
            'Hirsova': {'Urziceni': 98, 'Eforie': 86},\
            'Eforie': {'Hirsova': 86},\
            'Vaslui': {'Iasi': 92, 'Urziceni': 142},\
            'Iasi': {'Vaslui': 92, 'Neamt': 87},\
            'Neamt': {'Iasi': 87}\
        }

def dfs_caminos(origen, destino, camino=None):
    """Todos los posibles caminos desde el origen hasta el destino usando busqueda primero en profundidad (depth-first search)
    :parámetro origen: nombre de la ciudad de origen
    :parámetro destino: nombre de la ciudad de destino
    :parámetro camino: Camino actual recorrido camino (valor por defecto = None)
    :campos: Todos los posibles caminos desde el  origen hasta el destino
    """
    if camino is None:
        camino = [origen]
    if origen == destino:
        yield camino
    for sig_nodo in set(GRAFO[origen].keys()) - set(camino):
        yield from dfs_caminos(sig_nodo, destino, camino + [sig_nodo])

def ucs(origen, destino):
    """Camino menos costoso del origen hasta destino usando busqueda de costo uniforme (uniform costo search)
    :parámetro origen: nombre de la ciudad de origen
    :parámetro destino: nombre de la ciudad de destino
    :retorna: costo y camino para el recorrido más barato
    """
    from queue import PriorityQueue
    cola_prioridad, visitado = PriorityQueue(), {}
    cola_prioridad.put((0, origen, [origen]))
    visitado[origen] = 0
    while not cola_prioridad.empty():
        (costo, vertice, camino) = cola_prioridad.get()
        if vertice == destino:
            return costo, camino
        for sig_nodo in GRAFO[vertice].keys():
            costo_actual = costo + GRAFO[vertice][sig_nodo]
            if not sig_nodo in visitado or visitado[sig_nodo] >= costo_actual:
                visitado[sig_nodo] = costo_actual
                cola_prioridad.put((costo_actual, sig_nodo, camino + [sig_nodo]))

def a_estrella(origen, destino):
    """Camino óptimo desde el origen al destino usando como heurística la distancia en line recta
    :parámetro origen: nombre de la ciudad de origen
    :parámetro destino: nombre de la ciudad de destino
    :retorna: valor heurístico, costo y camino para el recorrido más óptimo
    """
    # AQUÍ LOS VALORES DE DISTANCIA DE LÍNEA RECTA DESDE LAS DISTINTAS CIUDADES HASTA BUCAREST QUE ES EL DESTINO
    dis_lineal = {\
                        'Arad': 366,\
                        'Zerind': 374,\
                        'Oradea': 380,\
                        'Sibiu': 253,\
                        'Timisoara': 329,\
                        'Lugoj': 244,\
                        'Mehadia': 241,\
                        'Drobeta': 242,\
                        'Craiova': 160,\
                        'Rimnicu': 193,\
                        'Fagaras': 176,\
                        'Pitesti': 100,\
                        'Bucharest': 0,\
                        'Giurgiu': 77,\
                        'Urziceni': 80,\
                        'Hirsova': 151,\
                        'Eforie': 161,\
                        'Vaslui': 199,\
                        'Iasi': 226,\
                        'Neamt': 234\
                    }
    from queue import PriorityQueue
    cola_prioridad, visitado = PriorityQueue(), {}
    cola_prioridad.put((dis_lineal[origen], 0, origen, [origen]))
    visitado[origen] = dis_lineal[origen]
    while not cola_prioridad.empty():
        (heuristica, costo, vertice, camino) = cola_prioridad.get()
        if vertice == destino:
            return heuristica, costo, camino
        for sig_nodo in GRAFO[vertice].keys():
            costo_actual = costo + GRAFO[vertice][sig_nodo]
            heuristica = costo_actual + dis_lineal[sig_nodo]
            if not sig_nodo in visitado or visitado[sig_nodo] >= heuristica:
                visitado[sig_nodo] = heuristica
                cola_prioridad.put((heuristica, costo_actual, sig_nodo, camino + [sig_nodo]))

def main():
    """Función principal"""
    print('INGRESE LA CUIDAD DE ORIGEN :', end=' ')
    origen = input().strip()
    print('INGRESE LA CIUDAD OBJETIVO :', end=' ')
    objetivo = input().strip()
    if origen not in GRAFO or objetivo not in GRAFO:
        print('ERROR: LA CIUDAD NO EXISTE.')
    else:
        print('\nTODOS LOS PISIBLES CAMINOS:')
        caminos = dfs_caminos(origen, objetivo)
        for camino in caminos:
            print(' -> '.join(ciudad for ciudad in camino))
        print('\nCAMINO MENOS COSTOSO:')
        costo, camino_barato = ucs(origen, objetivo)
        print('COSTO DEL CAMINO =', costo)
        print(' -> '.join(ciudad for ciudad in camino_barato))
        print('\nCAMINO ÓPTIMO:')
        heuristica, costo, camino_optimo = a_estrella(origen, objetivo)
        print('HEURÍSTICA =', heuristica)
        print('COSTO DEL CAMINO =', costo)
        print(' -> '.join(ciudad for ciudad in camino_optimo))

if __name__ == '__main__':
    main()
