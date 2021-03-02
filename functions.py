import pygame
import math
from options import * 

def imprimir_mensaje(WIN, mensaje, COLOR, posicion, size, all_fonts):
    font = pygame.font.SysFont(all_fonts[0], size) 
    textSurf = font.render(mensaje, True, COLOR)
    textRect = textSurf.get_rect()

    textRect.center = posicion
    WIN.blit(textSurf, textRect)

def imprimir_mensaje2(WIN, mensaje, COLOR, posicion, size, all_fonts):
    font = pygame.font.SysFont(all_fonts[0], size)
    texto = font.render(mensaje, True, COLOR)
    WIN.blit(texto, posicion)

def draw_lines(WIN):
    for i in range(WIDTH_TRABAJO // LADO_CUADRICULA + 1):
        line = pygame.Rect(i * LADO_CUADRICULA - 1, 0, 2, HEIGHT)
        pygame.draw.rect(WIN, COLOR_LINEAS, line)

    for i in range(HEIGHT // LADO_CUADRICULA + 1):
        line = pygame.Rect(0, i * LADO_CUADRICULA - 1, WIDTH_TRABAJO, 2)
        pygame.draw.rect(WIN, COLOR_LINEAS, line)

def draw_nodos(WIN, nodos, nodo1, nodo2):
    for i in range(len(nodos)):
        COLOR = COLOR_CENTRO
        if i != 0: COLOR = COLOR_NODO
        if i == nodo1 or i == nodo2: COLOR = COLOR_NODO_SELECCIONADO

        pygame.draw.circle(WIN, COLOR, nodos[i], RADIO_NODO)
        pygame.draw.circle(WIN, BLACK, nodos[i], RADIO_NODO, 1)

def draw_aristas(WIN, nodos, aristas, COLOR, TREE, all_fonts):
    for arista in aristas:
        i = arista[0]
        j = arista[1]

        if not TREE:
            pygame.draw.line(WIN, COLOR, nodos[i], nodos[j])

        if TREE and arista[2] != INF:
            mitad = ((nodos[i][0] + nodos[j][0])/2, (nodos[i][1] + nodos[j][1]) / 2)
            pygame.draw.line(WIN, COLOR, nodos[i], nodos[j])
            imprimir_mensaje(WIN, str(arista[2]), COLOR_VALOR_ARISTA, mitad, SIZE_FONT, all_fonts)

def draw_nodo_informacion(WIN, nodos, informacion, all_fonts):
    for i in range(len(nodos)):
        mensaje = str(informacion[i])
        if informacion[i] == INF:
            mensaje = "INF"

        imprimir_mensaje(WIN, mensaje, COLOR_VALOR_DISTANCIA, nodos[i], SIZE_FONT, all_fonts)

def comprobar_posicion_nodo(posicion, nodos):
    comp = True
    for nodo in nodos:
        if calcular_distancia(nodo[0], nodo[1], posicion[0], posicion[1]) < RADIO_NODO * 3:
            comp = False
    if posicion[0] >= 0 and posicion[0]+RADIO_NODO <= WIDTH_TRABAJO and posicion[1] >= 0 and posicion[1]+RADIO_NODO <= HEIGHT:
        return True and comp
    return False

def calcular_distancia(x1, y1, x2, y2):
    return math.hypot(x1-x2, y1-y2)

def obtener_cercano(posicion, nodos):
    d = INF 
    pos = -1
    for i in range(len(nodos)):
        dTemp = calcular_distancia(nodos[i][0], nodos[i][1], posicion[0], posicion[1])
        if dTemp < d:
            d = dTemp
            pos = i

    if d < RADIO_NODO: return pos
    return -1

# Dado el numero de vertices y el numero de aristas, me retornara n-1 aristas, el cual representa las aristas elegidas por el algoritmo Dijkstra
# y tambien retornará las distancias del nodo 0 a los demas nodos
def dijkstra(n, aristas):
    tree = []
    d = [INF] * n
    used = [False] * n
    p = [-1] * n
    g = [[INF] * n for i in range(n)]

    for arista in aristas:
        u = arista[0]
        v = arista[1]
        w = arista[2]

        g[u][v] = min(g[u][v], w)
        g[v][u] = g[u][v]

    d[0] = 0
    for i in range(n):
        pos = -1
        Tpos = INF

        for j in range(n):
            if used[j] == False and d[j] < Tpos:
                pos = j
                Tpos = d[j]

        if Tpos == INF: break
        used[pos] = 1

        for j in range(n):
            if used[j] == False and d[pos] + g[pos][j] < d[j]:
               d[j] = d[pos] + g[pos][j]
               p[j] = pos

        d[j] = d[j] * 10
        d[j] = int(d[j])
        d[j] = d[j] / 10

    for i in range(1, n):
        if p[i] != -1:
            tree.append((i, p[i], g[i][p[i]]))
    
    return tree, d

def obtener_ady(n, tree):
    adyTree = [[] for i in range(n)]
    
    for arista in tree:
        u = arista[0]
        v = arista[1] 

        adyTree[u].append(v)
        adyTree[v].append(u)

    return adyTree

# En la lista C, se guardaran el numero de vehiculos necesarios para cada nodo. Partirán todos los vehiculos desde la central
def cantidad_vehiculos(v, adyTree, used, c):
    used[v] = True

    c[v] = 0
    for to in adyTree[v]:
        if not used[to]:
            cantidad_vehiculos(to, adyTree, used, c)
            c[v] = c[v] + c[to]

    if c[v] == 0: c[v] = 1

#imprimir_mensaje(WIN, mensaje, COLOR, posicion, size)

def imprimir_instrucciones(WIN, MODE, all_fonts):
    LEFT = WIDTH_TRABAJO + 20
    imprimir_mensaje2(WIN, "Presionar 0: Borrar el grafo actual", COLOR_INSTRUCCIONES, (LEFT, 20), SIZE_INSTRUCCIONES, all_fonts)
    imprimir_mensaje2(WIN, "Presionar 1: Añadir nodo con click izq.", COLOR_INSTRUCCIONES, (LEFT, 60), SIZE_INSTRUCCIONES, all_fonts)
    imprimir_mensaje2(WIN, "(Eliminar nodo con click der.)", COLOR_INSTRUCCIONES, (LEFT, 80), SIZE_INSTRUCCIONES, all_fonts)
    imprimir_mensaje2(WIN, "Presionar 2: Añadir una arista", COLOR_INSTRUCCIONES, (LEFT, 120), SIZE_INSTRUCCIONES, all_fonts)
    imprimir_mensaje2(WIN, "(Clickear en 2 nodos diferentes)", COLOR_INSTRUCCIONES, (LEFT, 140), SIZE_INSTRUCCIONES, all_fonts)
    imprimir_mensaje2(WIN, "(Borrar arista: w <= 0)", COLOR_INSTRUCCIONES, (LEFT, 160), SIZE_INSTRUCCIONES, all_fonts)
    imprimir_mensaje2(WIN, "Presionar 3: Mostrar/esconder pesos", COLOR_INSTRUCCIONES, (LEFT, 200), SIZE_INSTRUCCIONES, all_fonts)
    imprimir_mensaje2(WIN, "Presionar 4: Mostrar/esconder mapa", COLOR_INSTRUCCIONES, (LEFT, 240), SIZE_INSTRUCCIONES, all_fonts)
    imprimir_mensaje2(WIN, "Presionar 5: Dijkstra", COLOR_INSTRUCCIONES, (LEFT, 280), SIZE_INSTRUCCIONES, all_fonts)
    imprimir_mensaje2(WIN, "Presionar 6: Vehiculos", COLOR_INSTRUCCIONES, (LEFT, 320), SIZE_INSTRUCCIONES, all_fonts)
    imprimir_mensaje2(WIN, "MODO ACTUAL: " + str(MODE), COLOR_INSTRUCCIONES, (LEFT, 380), SIZE_INSTRUCCIONES, all_fonts)


