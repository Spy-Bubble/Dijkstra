"""
SIMULADOR DEL ALGORITMO DE DIJKSTRA
Encuentra el camino más corto desde un nodo origen a todos los demás nodos en un grafo ponderado.
"""

import heapq
import math


class Grafo:
    """Clase para representar un grafo ponderado."""
    
    def __init__(self):
        """Inicializa un grafo vacío."""
        self.vertices = set()
        self.aristas = {}
    
    def agregar_vertice(self, vertice):
        """Agrega un vértice al grafo."""
        self.vertices.add(vertice)
        if vertice not in self.aristas:
            self.aristas[vertice] = []
    
    def agregar_arista(self, origen, destino, peso):
        """
        Agrega una arista con peso al grafo.
        
        Args:
            origen: Nodo de origen
            destino: Nodo de destino
            peso: Peso de la arista (distancia, costo, etc.)
        """
        self.agregar_vertice(origen)
        self.agregar_vertice(destino)
        
        # Arista no dirigida (bidireccional)
        self.aristas[origen].append((destino, peso))
        self.aristas[destino].append((origen, peso))
    
    def obtener_vecinos(self, vertice):
        """Retorna los vecinos de un vértice con sus pesos."""
        return self.aristas.get(vertice, [])
    
    def mostrar_grafo(self):
        """Muestra la estructura del grafo."""
        print("\nEstructura del Grafo:")
        print("-" * 50)
        for vertice in sorted(self.vertices):
            vecinos = self.aristas[vertice]
            print(f"{vertice}: {vecinos}")


def dijkstra(grafo, origen):
    """
    Implementación del Algoritmo de Dijkstra.
    
    Args:
        grafo: Instancia de la clase Grafo
        origen: Nodo desde el cual calcular las distancias mínimas
    
    Returns:
        distancias: Diccionario con las distancias mínimas desde origen
        predecesores: Diccionario con el nodo predecesor en el camino más corto
    """
    # Inicializar distancias con infinito
    distancias = {vertice: math.inf for vertice in grafo.vertices}
    distancias[origen] = 0
    
    # Diccionario para rastrear predecesores (reconstruir camino)
    predecesores = {vertice: None for vertice in grafo.vertices}
    
    # Conjunto de nodos visitados
    visitados = set()
    
    # Cola de prioridad: (distancia, nodo)
    cola_prioridad = [(0, origen)]
    
    print(f"\nIniciando Dijkstra desde nodo: {origen}")
    print("=" * 70)
    
    paso = 0
    
    while cola_prioridad:
        # Extraer nodo con menor distancia
        distancia_actual, nodo_actual = heapq.heappop(cola_prioridad)
        
        # Si ya fue visitado, continuar
        if nodo_actual in visitados:
            continue
        
        # Marcar como visitado
        visitados.add(nodo_actual)
        
        paso += 1
        print(f"\nPaso {paso}: Visitando nodo '{nodo_actual}' con distancia {distancia_actual}")
        
        # Explorar vecinos
        for vecino, peso in grafo.obtener_vecinos(nodo_actual):
            if vecino in visitados:
                continue
            
            # Calcular nueva distancia
            nueva_distancia = distancia_actual + peso
            
            # Si encontramos un camino más corto, actualizar
            if nueva_distancia < distancias[vecino]:
                distancia_anterior = distancias[vecino]
                distancias[vecino] = nueva_distancia
                predecesores[vecino] = nodo_actual
                heapq.heappush(cola_prioridad, (nueva_distancia, vecino))
                
                print(f"  -> Actualizando '{vecino}': {distancia_anterior} -> {nueva_distancia} (via '{nodo_actual}')")
            else:
                print(f"  -> '{vecino}': distancia {nueva_distancia} no mejora la actual ({distancias[vecino]})")
    
    return distancias, predecesores


def reconstruir_camino(predecesores, origen, destino):
    """
    Reconstruye el camino más corto desde origen hasta destino.
    
    Args:
        predecesores: Diccionario de predecesores
        origen: Nodo de inicio
        destino: Nodo final
    
    Returns:
        Lista con el camino desde origen hasta destino
    """
    camino = []
    nodo_actual = destino
    
    # Reconstruir camino desde destino hacia origen
    while nodo_actual is not None:
        camino.append(nodo_actual)
        nodo_actual = predecesores[nodo_actual]
    
    # Invertir para tener camino de origen a destino
    camino.reverse()
    
    # Verificar que el camino comienza en origen
    if camino[0] != origen:
        return []
    
    return camino


def mostrar_resultados(grafo, origen, distancias, predecesores):
    """Muestra los resultados del algoritmo de Dijkstra."""
    print("\n" + "=" * 70)
    print("RESULTADOS FINALES")
    print("=" * 70)
    
    print(f"\nDistancias mínimas desde '{origen}':")
    print("-" * 50)
    for vertice in sorted(grafo.vertices):
        distancia = distancias[vertice]
        if distancia == math.inf:
            print(f"  {origen} -> {vertice}: INALCANZABLE")
        else:
            print(f"  {origen} -> {vertice}: {distancia}")
    
    print(f"\nCaminos más cortos desde '{origen}':")
    print("-" * 50)
    for vertice in sorted(grafo.vertices):
        if vertice == origen:
            continue
        
        camino = reconstruir_camino(predecesores, origen, vertice)
        
        if not camino:
            print(f"  {origen} -> {vertice}: NO HAY CAMINO")
        else:
            camino_str = " -> ".join(camino)
            print(f"  {camino_str} (distancia: {distancias[vertice]})")


# ============================================================================
# EJEMPLOS DE USO
# ============================================================================

def ejemplo_basico():
    """Ejemplo básico con grafo pequeño."""
    print("\n" + "=" * 70)
    print("EJEMPLO 1: Grafo Básico")
    print("=" * 70)
    
    # Crear grafo
    g = Grafo()
    
    # Agregar aristas (origen, destino, peso)
    g.agregar_arista('A', 'B', 4)
    g.agregar_arista('A', 'C', 2)
    g.agregar_arista('B', 'C', 1)
    g.agregar_arista('B', 'D', 5)
    g.agregar_arista('C', 'D', 8)
    g.agregar_arista('C', 'E', 10)
    g.agregar_arista('D', 'E', 2)
    
    # Mostrar estructura
    g.mostrar_grafo()
    
    # Ejecutar Dijkstra
    origen = 'A'
    distancias, predecesores = dijkstra(g, origen)
    
    # Mostrar resultados
    mostrar_resultados(g, origen, distancias, predecesores)


def ejemplo_red_ciudades():
    """Ejemplo de red de ciudades con distancias."""
    print("\n" + "=" * 70)
    print("EJEMPLO 2: Red de Ciudades")
    print("=" * 70)
    
    # Crear grafo de ciudades
    g = Grafo()
    
    # Agregar conexiones entre ciudades (distancias en km)
    g.agregar_arista('Guadalajara', 'Zapopan', 10)
    g.agregar_arista('Guadalajara', 'Tlaquepaque', 12)
    g.agregar_arista('Guadalajara', 'Tonala', 18)
    g.agregar_arista('Zapopan', 'Tlaquepaque', 20)
    g.agregar_arista('Zapopan', 'Tequila', 60)
    g.agregar_arista('Tlaquepaque', 'Tonala', 8)
    g.agregar_arista('Tonala', 'El Salto', 15)
    g.agregar_arista('Tequila', 'Amatitan', 25)
    
    # Mostrar estructura
    g.mostrar_grafo()
    
    # Ejecutar Dijkstra desde Guadalajara
    origen = 'Guadalajara'
    distancias, predecesores = dijkstra(g, origen)
    
    # Mostrar resultados
    mostrar_resultados(g, origen, distancias, predecesores)


def ejemplo_interactivo():
    """Permite al usuario crear su propio grafo."""
    print("\n" + "=" * 70)
    print("EJEMPLO 3: Grafo Interactivo")
    print("=" * 70)
    
    g = Grafo()
    
    print("\nCrear grafo personalizado")
    print("Ingrese las aristas (origen destino peso)")
    print("Ejemplo: A B 5")
    print("Escriba 'fin' para terminar")
    print("-" * 50)
    
    while True:
        entrada = input("Arista: ").strip()
        
        if entrada.lower() == 'fin':
            break
        
        try:
            partes = entrada.split()
            if len(partes) != 3:
                print("  ERROR: Formato incorrecto. Use: origen destino peso")
                continue
            
            origen, destino, peso = partes[0], partes[1], float(partes[2])
            g.agregar_arista(origen, destino, peso)
            print(f"  Agregada: {origen} <-> {destino} (peso: {peso})")
        
        except ValueError:
            print("  ERROR: El peso debe ser un número")
        except Exception as e:
            print(f"  ERROR: {e}")
    
    if not g.vertices:
        print("\nNo se agregaron aristas. Terminando.")
        return
    
    # Mostrar grafo creado
    g.mostrar_grafo()
    
    # Solicitar nodo origen
    print("\nNodos disponibles:", sorted(g.vertices))
    nodo_origen = input("Ingrese nodo origen: ").strip()
    
    if nodo_origen not in g.vertices:
        print(f"ERROR: El nodo '{nodo_origen}' no existe en el grafo")
        return
    
    # Ejecutar Dijkstra
    distancias, predecesores = dijkstra(g, nodo_origen)
    
    # Mostrar resultados
    mostrar_resultados(g, nodo_origen, distancias, predecesores)


def ejemplo_complejo():
    """Ejemplo con grafo más complejo."""
    print("\n" + "=" * 70)
    print("EJEMPLO 4: Grafo Complejo")
    print("=" * 70)
    
    g = Grafo()
    
    # Red más compleja
    aristas = [
        ('S', 'A', 7),
        ('S', 'B', 2),
        ('S', 'C', 3),
        ('A', 'B', 3),
        ('A', 'D', 4),
        ('B', 'D', 4),
        ('B', 'H', 1),
        ('C', 'L', 2),
        ('D', 'F', 5),
        ('E', 'G', 2),
        ('E', 'K', 5),
        ('F', 'H', 3),
        ('G', 'H', 2),
        ('I', 'J', 6),
        ('I', 'K', 4),
        ('J', 'L', 4),
        ('K', 'J', 4)
    ]
    
    for origen, destino, peso in aristas:
        g.agregar_arista(origen, destino, peso)
    
    g.mostrar_grafo()
    
    # Ejecutar desde 'S'
    origen = 'S'
    distancias, predecesores = dijkstra(g, origen)
    
    mostrar_resultados(g, origen, distancias, predecesores)


# ============================================================================
# PROGRAMA PRINCIPAL
# ============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print(" SIMULADOR DEL ALGORITMO DE DIJKSTRA")
    print("=" * 70)
    
    while True:
        print("\n" + "=" * 70)
        print("MENU PRINCIPAL")
        print("=" * 70)
        print("1. Ejemplo Básico")
        print("2. Ejemplo Red de Ciudades")
        print("3. Crear Grafo Interactivo")
        print("4. Ejemplo Complejo")
        print("5. Salir")
        print("-" * 70)
        
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == '1':
            ejemplo_basico()
        elif opcion == '2':
            ejemplo_red_ciudades()
        elif opcion == '3':
            ejemplo_interactivo()
        elif opcion == '4':
            ejemplo_complejo()
        elif opcion == '5':
            print("\nSaliendo del simulador...")
            break
        else:
            print("\nOpción inválida. Intente nuevamente.")
        
        input("\nPresione ENTER para continuar...")
    
    print("\n" + "=" * 70)
    print(" FIN DEL SIMULADOR")
    print("=" * 70)