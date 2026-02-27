"""
═══════════════════════════════════════════════
Red de Hospitales y Urgencias — Algoritmo de Dijkstra
Encuentra la ruta más rápida desde cualquier punto
hasta el hospital más cercano.
═══════════════════════════════════════════════
"""

import heapq
import math
import os
import sys


# ═══════════════════════════════════════════════
#  COLORES ANSI
# ═══════════════════════════════════════════════

class Color:
    VERDE        = "\033[92m"
    VERDE_OSCURO = "\033[32m"
    AZUL         = "\033[96m"
    AZUL_OSCURO  = "\033[34m"
    AMARILLO     = "\033[93m"
    ROJO         = "\033[91m"
    ROJO_OSCURO  = "\033[31m"
    GRIS         = "\033[90m"
    BLANCO       = "\033[97m"
    MAGENTA      = "\033[95m"
    NEGRITA      = "\033[1m"
    RESET        = "\033[0m"

def c(texto, *estilos):
    return "".join(estilos) + str(texto) + Color.RESET


# ═══════════════════════════════════════════════
#  ESTRUCTURAS DE DATOS
# ═══════════════════════════════════════════════

class RedHospitalaria:
    """
    Grafo que representa una red de ubicaciones (colonias,
    intersecciones, hospitales) con tiempos de traslado en minutos.
    """

    def __init__(self):
        self.nodos      = {}   # nombre → { 'tipo': 'hospital'|'colonia'|'cruce', 'info': str }
        self.adyacencia = {}   # nombre → [(vecino, minutos), ...]

    # ── Agregar nodos ──────────────────────────

    def agregar_lugar(self, nombre, tipo="colonia", info=""):
        """
        Agrega una ubicación a la red.
        tipo: 'hospital' | 'colonia' | 'cruce'
        """
        if nombre not in self.nodos:
            self.nodos[nombre]      = {"tipo": tipo, "info": info}
            self.adyacencia[nombre] = []

    def agregar_ruta(self, origen, destino, minutos):
        """Conecta dos ubicaciones con un tiempo de traslado (bidireccional)."""
        self.agregar_lugar(origen)
        self.agregar_lugar(destino)
        # Evitar duplicados
        if not any(v == destino for v, _ in self.adyacencia[origen]):
            self.adyacencia[origen].append((destino, minutos))
        if not any(v == origen for v, _ in self.adyacencia[destino]):
            self.adyacencia[destino].append((origen, minutos))

    def hospitales(self):
        return [n for n, d in self.nodos.items() if d["tipo"] == "hospital"]

    def colonias(self):
        return [n for n, d in self.nodos.items() if d["tipo"] != "hospital"]

    def vecinos(self, nodo):
        return self.adyacencia.get(nodo, [])


# ═══════════════════════════════════════════════
#  ALGORITMO DE DIJKSTRA
# ═══════════════════════════════════════════════

def dijkstra(red, origen):
    """
    Dijkstra desde un nodo origen hacia todos los demás.

    Retorna:
        dist  : { nodo: minutos_minimos }
        prev  : { nodo: nodo_anterior }   ← para reconstruir el camino
        pasos : [ str ]                   ← log del proceso
    """
    INF  = math.inf
    dist = {n: INF  for n in red.nodos}
    prev = {n: None for n in red.nodos}
    dist[origen] = 0

    # Cola de prioridad: (distancia_acumulada, nodo)
    heap     = [(0, origen)]
    visitado = set()
    pasos    = []

    pasos.append(f"▶  Origen: '{origen}'  —  iniciando búsqueda")

    while heap:
        d_actual, u = heapq.heappop(heap)

        if u in visitado:
            continue
        visitado.add(u)

        tipo_u = red.nodos[u]["tipo"]
        emoji  = "🏥" if tipo_u == "hospital" else "📍"
        pasos.append(f"   Visitando {emoji} '{u}'  ({d_actual} min desde origen)")

        for v, peso in red.vecinos(u):
            if v in visitado:
                continue
            nueva_d = d_actual + peso
            if nueva_d < dist[v]:
                dist[v] = nueva_d
                prev[v] = u
                heapq.heappush(heap, (nueva_d, v))
                pasos.append(
                    f"      ~ Actualizado '{v}': {nueva_d} min  (vía '{u}')"
                )

    return dist, prev, pasos


def reconstruir_ruta(prev, origen, destino):
    """Reconstruye el camino desde origen hasta destino usando el dict prev."""
    ruta = []
    nodo = destino
    while nodo is not None:
        ruta.append(nodo)
        nodo = prev[nodo]
    ruta.reverse()
    if not ruta or ruta[0] != origen:
        return []
    return ruta


# ═══════════════════════════════════════════════
#  UTILIDADES DE TERMINAL
# ═══════════════════════════════════════════════

def limpiar():
    os.system("cls" if os.name == "nt" else "clear")

def sep(ancho=50, color=Color.GRIS):
    print(c("  " + "─" * ancho, color))

def encabezado():
    print(c("╔══════════════════════════════════════════════════╗", Color.ROJO))
    print(c("║  🏥  Red de Hospitales — Ruta de Urgencias       ║", Color.ROJO, Color.NEGRITA))
    print(c("║       Algoritmo de Dijkstra · Python             ║", Color.ROJO))
    print(c("╚══════════════════════════════════════════════════╝", Color.ROJO))
    print()

def pedir_entero(msg, minimo=1):
    while True:
        try:
            v = int(input(msg))
            if v >= minimo:
                return v
            print(c(f"  ⚠  Debe ser ≥ {minimo}", Color.AMARILLO))
        except ValueError:
            print(c("  ⚠  Ingresa un número entero.", Color.AMARILLO))

def pedir_opcion(opciones):
    while True:
        op = input("  Opción: ").strip()
        if op in opciones:
            return op
        print(c("  ⚠  Opción no válida.", Color.AMARILLO))

def listar_nodos(red, solo_hospitales=False, solo_colonias=False):
    for nombre, datos in sorted(red.nodos.items()):
        tipo = datos["tipo"]
        if solo_hospitales and tipo != "hospital":
            continue
        if solo_colonias and tipo == "hospital":
            continue
        emoji = "🏥" if tipo == "hospital" else ("🔀" if tipo == "cruce" else "🏘️")
        info  = f"  {c('—', Color.GRIS)} {datos['info']}" if datos["info"] else ""
        print(f"    {emoji}  {c(nombre, Color.BLANCO)}{info}")


# ═══════════════════════════════════════════════
#  MENÚS
# ═══════════════════════════════════════════════

def menu_agregar_lugar(red):
    sep()
    print(c("  ➕  AGREGAR LUGAR", Color.AZUL, Color.NEGRITA))
    sep()
    print(f"  Tipos:  {c('1', Color.AMARILLO)} Hospital   "
          f"{c('2', Color.AMARILLO)} Colonia/Barrio   "
          f"{c('3', Color.AMARILLO)} Cruce/Avenida")
    print()
    t = pedir_opcion({"1", "2", "3"})
    tipo_map = {"1": "hospital", "2": "colonia", "3": "cruce"}
    tipo = tipo_map[t]

    nombre = input(c("  Nombre del lugar: ", Color.BLANCO)).strip()
    if not nombre:
        print(c("  ⚠  Nombre vacío, operación cancelada.", Color.AMARILLO))
        return
    if nombre in red.nodos:
        print(c(f"  ⚠  '{nombre}' ya existe.", Color.AMARILLO))
        return

    info = input(c("  Descripción breve (opcional): ", Color.GRIS)).strip()
    red.agregar_lugar(nombre, tipo, info)
    emoji = "🏥" if tipo == "hospital" else ("🔀" if tipo == "cruce" else "🏘️")
    print(c(f"\n  ✔  {emoji} '{nombre}' agregado como {tipo}.", Color.VERDE))


def menu_agregar_ruta(red):
    sep()
    print(c("  🛣️  AGREGAR RUTA / CONEXIÓN", Color.AZUL, Color.NEGRITA))
    sep()
    if len(red.nodos) < 2:
        print(c("  ⚠  Necesitas al menos 2 lugares.", Color.AMARILLO))
        return

    print(c("  Lugares disponibles:", Color.BLANCO))
    listar_nodos(red)
    print()

    origen  = input(c("  Desde: ", Color.BLANCO)).strip()
    destino = input(c("  Hasta: ", Color.BLANCO)).strip()

    if origen not in red.nodos:
        print(c(f"  ⚠  '{origen}' no existe.", Color.ROJO)); return
    if destino not in red.nodos:
        print(c(f"  ⚠  '{destino}' no existe.", Color.ROJO)); return
    if origen == destino:
        print(c("  ⚠  Origen y destino son iguales.", Color.AMARILLO)); return

    minutos = pedir_entero(c("  Tiempo de traslado (minutos): ", Color.BLANCO), minimo=1)
    red.agregar_ruta(origen, destino, minutos)
    print(c(f"\n  ✔  Ruta añadida: '{origen}' ↔ '{destino}'  ({minutos} min)", Color.VERDE))


def menu_calcular(red):
    sep()
    print(c("  🚨  CALCULAR RUTA DE URGENCIA", Color.ROJO, Color.NEGRITA))
    sep()

    if not red.hospitales():
        print(c("  ⚠  No hay hospitales en la red. Añade al menos uno.", Color.AMARILLO))
        return
    if len(red.nodos) < 2:
        print(c("  ⚠  La red tiene muy pocos nodos.", Color.AMARILLO))
        return

    print(c("  Lugar de origen (paciente / emergencia):", Color.BLANCO))
    listar_nodos(red, solo_colonias=True)
    print()
    origen = input(c("  ¿Desde dónde parte la ambulancia? ", Color.BLANCO)).strip()

    if origen not in red.nodos:
        print(c(f"  ⚠  '{origen}' no existe en la red.", Color.ROJO))
        return

    # ── Ejecutar Dijkstra ──
    dist, prev, pasos = dijkstra(red, origen)

    # ── Mostrar log ──
    print()
    sep(50, Color.AZUL)
    print(c("  📋  REGISTRO DEL PROCESO", Color.AZUL, Color.NEGRITA))
    sep(50, Color.AZUL)
    for paso in pasos:
        if "▶" in paso:
            print(c(paso, Color.VERDE))
        elif "🏥" in paso:
            print(c(paso, Color.ROJO))
        elif "~" in paso:
            print(c(paso, Color.GRIS))
        else:
            print(c(paso, Color.AZUL_OSCURO))

    # ── Encontrar hospital más cercano ──
    hospitales_alcanzables = [
        (dist[h], h) for h in red.hospitales() if dist[h] < math.inf
    ]

    print()
    sep(50, Color.ROJO)
    print(c("  🏆  RESULTADO", Color.ROJO, Color.NEGRITA))
    sep(50, Color.ROJO)

    if not hospitales_alcanzables:
        print(c("  ⚠  Ningún hospital es alcanzable desde este punto.", Color.ROJO))
        return

    hospitales_alcanzables.sort()

    # Mostrar todos los hospitales con sus tiempos
    print(c(f"\n  Tiempos desde '{origen}' a cada hospital:", Color.BLANCO))
    print()
    for i, (tiempo, hosp) in enumerate(hospitales_alcanzables):
        ruta  = reconstruir_ruta(prev, origen, hosp)
        camino = " → ".join(ruta)
        marca = c("  ★ MÁS CERCANO", Color.AMARILLO, Color.NEGRITA) if i == 0 else ""
        print(f"  {c('🏥', '')} {c(hosp, Color.BLANCO, Color.NEGRITA)}{marca}")
        print(f"     Tiempo : {c(str(tiempo) + ' minutos', Color.AMARILLO)}")
        print(f"     Ruta   : {c(camino, Color.AZUL)}")
        print()

    # ── Recomendación principal ──
    mejor_tiempo, mejor_hosp = hospitales_alcanzables[0]
    mejor_ruta = reconstruir_ruta(prev, origen, mejor_hosp)

    sep(50, Color.VERDE)
    print(c("  🚑  RECOMENDACIÓN DE URGENCIA", Color.VERDE, Color.NEGRITA))
    sep(50, Color.VERDE)
    print()
    print(f"  Dirigirse a  : {c(mejor_hosp, Color.BLANCO, Color.NEGRITA)}")
    print(f"  Tiempo total : {c(str(mejor_tiempo) + ' minutos', Color.AMARILLO, Color.NEGRITA)}")
    print(f"  Paradas      : {c(str(len(mejor_ruta)), Color.AZUL)}")
    print()
    print(f"  {c('Ruta completa:', Color.BLANCO)}")

    for i, nodo in enumerate(mejor_ruta):
        tipo  = red.nodos[nodo]["tipo"]
        emoji = "🏥" if tipo == "hospital" else ("📍" if i == 0 else "🔀")
        flecha = "" if i == len(mejor_ruta) - 1 else "  ↓"
        if i == 0:
            print(f"    {emoji}  {c(nodo, Color.VERDE, Color.NEGRITA)}  {c('← ORIGEN', Color.GRIS)}{flecha}")
        elif i == len(mejor_ruta) - 1:
            print(f"    {emoji}  {c(nodo, Color.ROJO, Color.NEGRITA)}  {c('← DESTINO', Color.GRIS)}")
        else:
            # Mostrar tiempo parcial hasta este punto
            t_parcial = dist[nodo]
            print(f"    🔀  {c(nodo, Color.AZUL)}  {c(f'({t_parcial} min)', Color.GRIS)}{flecha}")
    print()


def menu_ver_red(red):
    sep()
    print(c("  📡  ESTADO DE LA RED", Color.AZUL, Color.NEGRITA))
    sep()
    if not red.nodos:
        print(c("  (Red vacía)", Color.GRIS))
        return

    # Hospitales
    hospitales = red.hospitales()
    print(c(f"\n  Hospitales ({len(hospitales)}):", Color.ROJO, Color.NEGRITA))
    if hospitales:
        for h in sorted(hospitales):
            info = red.nodos[h]["info"]
            desc = f"  — {info}" if info else ""
            rutas = red.adyacencia[h]
            print(f"    🏥  {c(h, Color.BLANCO)}{c(desc, Color.GRIS)}")
            for v, m in rutas:
                print(f"         {c('↔', Color.GRIS)} {v}  {c(str(m)+'min', Color.AMARILLO)}")
    else:
        print(c("    (ninguno)", Color.GRIS))

    # Colonias y cruces
    otros = [n for n in red.nodos if red.nodos[n]["tipo"] != "hospital"]
    print(c(f"\n  Colonias y cruces ({len(otros)}):", Color.AZUL, Color.NEGRITA))
    for n in sorted(otros):
        tipo  = red.nodos[n]["tipo"]
        emoji = "🔀" if tipo == "cruce" else "🏘️"
        rutas = red.adyacencia[n]
        print(f"    {emoji}  {c(n, Color.BLANCO)}")
        for v, m in rutas:
            print(f"         {c('↔', Color.GRIS)} {v}  {c(str(m)+'min', Color.AMARILLO)}")
    print()


# ═══════════════════════════════════════════════
#  EJEMPLO PRECONFIGURADO — Guadalajara
# ═══════════════════════════════════════════════

def cargar_ejemplo():
    """Red hospitalaria basada en zonas de Guadalajara."""
    red = RedHospitalaria()

    # Hospitales
    red.agregar_lugar("Hospital Civil",      "hospital", "Centro Histórico")
    red.agregar_lugar("Hospital Country",    "hospital", "Colonia Country Club")
    red.agregar_lugar("Cruz Roja GDL",       "hospital", "Av. Federalismo")

    # Colonias
    for col in ["Centro", "Zapopan", "Tlaquepaque", "Tonalá",
                "Providencia", "Chapalita", "Las Águilas"]:
        red.agregar_lugar(col, "colonia")

    # Cruces clave
    for cruce in ["Av. Vallarta", "Av. López Mateos", "Periférico Norte"]:
        red.agregar_lugar(cruce, "cruce")

    # Rutas (minutos en tráfico normal)
    rutas = [
        ("Centro",          "Hospital Civil",    5),
        ("Centro",          "Av. Vallarta",      8),
        ("Centro",          "Cruz Roja GDL",    10),
        ("Av. Vallarta",    "Providencia",       7),
        ("Av. Vallarta",    "Chapalita",        12),
        ("Av. Vallarta",    "Hospital Country", 15),
        ("Providencia",     "Hospital Country",  8),
        ("Chapalita",       "Las Águilas",      10),
        ("Las Águilas",     "Av. López Mateos",  6),
        ("Av. López Mateos","Hospital Civil",   18),
        ("Av. López Mateos","Tlaquepaque",       9),
        ("Tlaquepaque",     "Tonalá",           12),
        ("Tonalá",          "Periférico Norte", 20),
        ("Periférico Norte","Zapopan",          14),
        ("Periférico Norte","Hospital Country", 22),
        ("Zapopan",         "Cruz Roja GDL",    17),
        ("Cruz Roja GDL",   "Periférico Norte", 19),
    ]
    for o, d, m in rutas:
        red.agregar_ruta(o, d, m)

    return red


# ═══════════════════════════════════════════════
#  PROGRAMA PRINCIPAL
# ═══════════════════════════════════════════════

def main():
    red = RedHospitalaria()

    limpiar()
    encabezado()

    print(c("  ¿Cargar la red de ejemplo (Guadalajara)?", Color.BLANCO))
    print(f"  {c('s', Color.AMARILLO)} Sí    {c('n', Color.AMARILLO)} No, empezar vacío")
    print()
    if input("  → ").strip().lower() == "s":
        red = cargar_ejemplo()
        print(c("  ✔  Red de Guadalajara cargada.", Color.VERDE))

    while True:
        print()
        sep(50, Color.ROJO)
        print(c("  MENÚ PRINCIPAL", Color.ROJO, Color.NEGRITA))
        sep(50, Color.ROJO)
        print(f"  {c('1', Color.AMARILLO)} Agregar lugar (hospital / colonia / cruce)  "
              f"{c(f'({len(red.nodos)} en red)', Color.GRIS)}")
        print(f"  {c('2', Color.AMARILLO)} Agregar ruta entre dos lugares")
        print(f"  {c('3', Color.AMARILLO)} {c('🚨 Calcular ruta de urgencia', Color.ROJO, Color.NEGRITA)}")
        print(f"  {c('4', Color.AMARILLO)} Ver estado de la red")
        print(f"  {c('0', Color.AMARILLO)} Salir")
        print()

        op = pedir_opcion({"1", "2", "3", "4", "0"})

        if op == "1":
            menu_agregar_lugar(red)

        elif op == "2":
            menu_agregar_ruta(red)

        elif op == "3":
            print()
            menu_calcular(red)
            input(c("  Presiona Enter para continuar...", Color.GRIS))

        elif op == "4":
            menu_ver_red(red)
            input(c("  Presiona Enter para continuar...", Color.GRIS))

        elif op == "0":
            print(c("\n  🚑  ¡Que nunca necesites usarlo de verdad! Hasta luego.\n", Color.VERDE))
            sys.exit(0)


if __name__ == "__main__":
    main()
