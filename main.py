import pygame
import random
from options import *
from functions import *

pygame.init()
pygame.font.init()

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

def main():
    trabajo = pygame.Rect((0, 0), (WIDTH_TRABAJO, 800))
    opciones = pygame.Rect((WIDTH_TRABAJO, 0), (WIDTH_OPCIONES, 800))
    all_fonts = pygame.font.get_fonts()

    imagen = pygame.image.load("mapa.png")

    MODE = 0

    n = 0
    nodos = []
    aristas = []

    nodo1 = -1
    nodo2 = -1

    tree = []
    vehiculos = []
    d = []

    used = []

    changes = False

    VER_ARBOL = False
    VER_VEHICULOS = False
    MOSTRAR_PESOS = False
    MOSTRAR_MAPA = False
    font = pygame.font.SysFont(all_fonts[0], SIZE_FONT)

    run = True
    while run: 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                if event.key != pygame.K_2:
                    nodo1 = -1
                    nodo2 = -1

                if event.key == pygame.K_0:
                    MOSTRAR_PESOS = False
                    changes = True
                    n = 0
                    nodos = []
                    aristas = []
                    VER_ARBOL = False
                    MODE = 0

                if event.key == pygame.K_1:
                    MODE = 1
                    VER_ARBOL = False

                if event.key == pygame.K_2:
                    MODE = 2
                    VER_ARBOL = False

                if event.key == pygame.K_3:
                    MOSTRAR_PESOS = not MOSTRAR_PESOS 

                if event.key == pygame.K_4:
                    MOSTRAR_MAPA = not MOSTRAR_MAPA

                if event.key == pygame.K_5 or event.key == pygame.K_6:
                    if changes:
                        tree, d = dijkstra(n, aristas)

                        for i in range(len(d)):
                            d[i] = round(d[i], 1)

                        adyTree = obtener_ady(n, tree)

                        used = [False] * n
                        vehiculos = [0] * n

                        cantidad_vehiculos(0, adyTree, used, vehiculos)

                        changes = False
                        
                    VER_ARBOL = True
                    if event.key == pygame.K_6:
                        VER_VEHICULOS = True
                        MODE = 6
                    else:
                        VER_VEHICULOS = False
                        MODE = 5

            if event.type == pygame.MOUSEBUTTONDOWN:
                if MODE == 1:
                    if event.button == MOUSE_LEFT:
                        posicion = pygame.mouse.get_pos()
                        if comprobar_posicion_nodo(posicion, nodos):
                            changes = True
                            n = n + 1
                            nodos.append(posicion)

                    if event.button == MOUSE_RIGHT:
                        posicion = pygame.mouse.get_pos()
                        ind = obtener_cercano(posicion, nodos)
                        borrar = []

                        if ind > 0:
                            changes = True
                            for arista in aristas:
                                if arista[0] == ind or arista[1] == ind:
                                    borrar.append(arista)

                            for arista in borrar:
                                aristas.remove(arista)

                            nodos.remove(nodos[ind])

                            for i in range(len(aristas)):
                                u = aristas[i][0]
                                v = aristas[i][1]
                                w = aristas[i][2]

                                if u > ind:
                                    u = u - 1

                                if v  > ind:
                                    v = v - 1

                                aristas[i] = (u, v, w)

                            n = n - 1
                
                if MODE == 2:
                    if event.button == MOUSE_LEFT:
                        if len(nodos) == 0: continue

                        posicion = pygame.mouse.get_pos()
                        ind = obtener_cercano(posicion, nodos)

                        if ind != -1:
                            if nodo1 == -1:
                                nodo1 = ind

                            elif ind != nodo1:
                                nodo2 = ind
                                w = calcular_distancia(nodos[nodo1][0], nodos[nodo1][1], nodos[nodo2][0], nodos[nodo2][1]) - 2 * RADIO_NODO
                                w /= 3
                                w = int(w)
                                w = w / 10

                                found = False 
                                for i in range(len(aristas)):
                                    if (nodo1 == aristas[i][0] and nodo2 == aristas[i][1]) or (nodo1 == aristas[i][1] and nodo2 == aristas[i][0]):
                                        found = True
                                        if w > 0:
                                            aristas[i] = (nodo1, nodo2, w)
                                        else:
                                            aristas.remove(aristas[i])
                                        break

                                if not found: aristas.append((nodo1, nodo2, w))

                                changes = True
                                
                                nodo1 = -1
                                nodo2 = -1
        
        pygame.draw.rect(WIN, COLOR_TRABAJO, trabajo)
        pygame.draw.rect(WIN, COLOR_OPCIONES, opciones)
        draw_lines(WIN)

        if MOSTRAR_MAPA:
            WIN.blit(imagen, (0, 0))

        imprimir_instrucciones(WIN, MODE, all_fonts)

        if VER_ARBOL == False:
            draw_aristas(WIN, nodos, aristas, COLOR_ARISTAS_GRAFO, MOSTRAR_PESOS, all_fonts)
        else:
            if not VER_VEHICULOS:
                draw_aristas(WIN, nodos, tree, COLOR_ARISTAS_ARBOL, MOSTRAR_PESOS, all_fonts)
            else:
                draw_aristas(WIN, nodos, tree, COLOR_ARISTAS_VEHICULOS, False, all_fonts)

        draw_nodos(WIN, nodos, nodo1, nodo2)

        if VER_ARBOL:
            if not VER_VEHICULOS:
                draw_nodo_informacion(WIN, nodos, d, all_fonts)
            else:   
                draw_nodo_informacion(WIN, nodos, vehiculos, all_fonts)

        pygame.display.flip()

    

    pygame.quit()

if __name__ == "__main__":
    main()
