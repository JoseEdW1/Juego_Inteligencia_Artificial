# José Eduardo Williams 23-EISN-2-048
import pygame
import random
import math
import heapq

# Inicializar Pygame
pygame.init()

# Dimensiones de la ventana
ANCHO_PANTALLA = 1200
ALTO_PANTALLA = 900
screen = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption("Survive Cube")

# José Eduardo Williams 23-EISN-2-048
# Cargar imágenes
imagen_jugador = pygame.image.load("Imgs/jugador.png")
imagen_enemigo = pygame.image.load("Imgs/enemigo.png")
imagen_disparo = pygame.image.load("Imgs/disparo.png")
imagen_obstaculo = pygame.image.load("Imgs/obstaculo.png")
imagen_fondo = pygame.image.load("Imgs/fondo.png")
menu_inicio = pygame.image.load("Imgs/Menu inicio.png")
menu_derrota = pygame.image.load("Imgs/Menu perder.png")
menu_victoria = pygame.image.load("Imgs/Menu ganar.png")

# Cargar sonidos
sonido_disparo = pygame.mixer.Sound("Audio/disparo.mp3")
sonido_muerte_enemigo = pygame.mixer.Sound("Audio/enemigo muerte.mp3")
pygame.mixer.music.load("Audio/musica.mp3")

# José Eduardo Williams 23-EISN-2-048
# Reproducir música en bucle
pygame.mixer.music.play(-1)

# Colores
BLANCO = (255, 255, 255)

# Configuración del personaje
JUGADOR_VELOCIDAD = 3

# José Eduardo Williams 23-EISN-2-048
# Configuración de los enemigos
ENEMIGO_VELOCIDAD = 1
ENEMIGO_RECUENTO_INICIAL = 10

# Configuración de los obstáculos
OBSTACULO_ANCHO = 120
OBSTACULO_ALTO = 100
CANTIDAD_OBSTACULOS = 5

# Fuente para el texto
font = pygame.font.SysFont("Arial", 30)

# José Eduardo Williams 23-EISN-2-048
# Función para mostrar texto en pantalla
def dibujar_contador(texto, x, y):
    label = font.render(texto, True, BLANCO)
    screen.blit(label, (x, y))

# Función para mostrar la pantalla de inicio
def pantalla_inicio():
    screen.blit(menu_inicio, (0, 0))
    pygame.display.update()
    esperando = True
    while esperando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:  # Detectar clic del ratón
                esperando = False

# José Eduardo Williams 23-EISN-2-048
# Función para mostrar la pantalla de derrota
def pantalla_derrota():
    screen.blit(menu_derrota, (0, 0))
    pygame.display.update()
    esperando = True
    while esperando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:  # Detectar clic del ratón
                esperando = False
                game_loop()  # Reiniciar el juego

# Función para mostrar la pantalla de victoria
def pantalla_victoria():
    screen.blit(menu_victoria, (0, 0))
    pygame.display.update()
    esperando = True
    while esperando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:  # Detectar clic del ratón
                esperando = False

# José Eduardo Williams 23-EISN-2-048
# Función para mover al jugador
def mover_jugador(keys, x, y, obstaculos):
    nueva_x, nueva_y = x, y
    if keys[pygame.K_w] and y > 0:
        nueva_y -= JUGADOR_VELOCIDAD
    if keys[pygame.K_s] and y < ALTO_PANTALLA - 50:
        nueva_y += JUGADOR_VELOCIDAD
    if keys[pygame.K_a] and x > 0:
        nueva_x -= JUGADOR_VELOCIDAD
    if keys[pygame.K_d] and x < ANCHO_PANTALLA - 50:
        nueva_x += JUGADOR_VELOCIDAD

    # Verificar colisión con obstáculos
    if not colision_con_obstaculos(nueva_x, nueva_y, obstaculos):
        return nueva_x, nueva_y
    return x, y

# José Eduardo Williams 23-EISN-2-048
# Función para verificar colisión con obstáculos
def colision_con_obstaculos(x, y, obstaculos):
    jugador_rect = pygame.Rect(x, y, 50, 50)
    for obstaculo in obstaculos:
        if jugador_rect.colliderect(obstaculo):
            return True
    return False

# Función para generar enemigos
def generar_enemigos(count):
    enemigos = []
    for _ in range(count):
        lado = random.choice(['top', 'bottom', 'left', 'right'])
        if lado == 'top':
            x = random.randint(0, ANCHO_PANTALLA - 50)
            y = 0
        elif lado == 'bottom':
            x = random.randint(0, ANCHO_PANTALLA - 50)
            y = ALTO_PANTALLA - 50
        elif lado == 'left':
            x = 0
            y = random.randint(0, ALTO_PANTALLA - 50)
        else:
            x = ANCHO_PANTALLA - 50
            y = random.randint(0, ALTO_PANTALLA - 50)
        enemigos.append(pygame.Rect(x, y, 50, 50))
    return enemigos

# José Eduardo Williams 23-EISN-2-048
# Función para generar obstáculos
def generar_obstaculos():
    obstaculos = []
    for _ in range(CANTIDAD_OBSTACULOS):
        x = random.randint(0, ANCHO_PANTALLA - OBSTACULO_ANCHO)
        y = random.randint(0, ALTO_PANTALLA - OBSTACULO_ALTO)
        obstaculo = pygame.Rect(x, y, OBSTACULO_ANCHO, OBSTACULO_ALTO)
        obstaculos.append(obstaculo)
    return obstaculos

# Función para disparar
def disparar(jugador_rect, disparos, tiempo_ultimo_disparo):
    if pygame.mouse.get_pressed()[0] and pygame.time.get_ticks() - tiempo_ultimo_disparo >= 1000:  # En milisegundos
        sonido_disparo.play()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        angulo = math.atan2(mouse_y - jugador_rect.centery, mouse_x - jugador_rect.centerx)
        velocidad = [math.cos(angulo) * 5, math.sin(angulo) * 5]
        disparo = pygame.Rect(jugador_rect.centerx, jugador_rect.centery, 60, 100)
        disparos.append([disparo, velocidad, angulo])
        tiempo_ultimo_disparo = pygame.time.get_ticks()  # Actualizar el tiempo del último disparo
    return tiempo_ultimo_disparo

# José Eduardo Williams 23-EISN-2-048
# Función para mover balas
def mover_balas(disparos):
    for disparo in disparos:
        disparo[0].x += disparo[1][0]
        disparo[0].y += disparo[1][1]

# Función para detectar colisiones
def revisar_colisiones(disparos, enemigos, jugador_rect):
    for disparo in disparos[:]:
        for enemigo in enemigos[:]:
            if disparo[0].colliderect(enemigo):
                sonido_muerte_enemigo.play()
                enemigos.remove(enemigo)
                disparos.remove(disparo)
                break
    for enemigo in enemigos:
        if enemigo.colliderect(jugador_rect):
            return True
    return False

# José Eduardo Williams 23-EISN-2-048
# Algoritmo A* 
def a_estrella(inicio, objetivo, obstaculos):
    def distancia(p1, p2):
        return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

    def obtener_vecinos(nodo):
        vecinos = []
        for dx in [-10, 0, 10]:
            for dy in [-10, 0, 10]:
                if dx == 0 and dy == 0:
                    continue
                x = nodo[0] + dx
                y = nodo[1] + dy
                if 0 <= x < ANCHO_PANTALLA and 0 <= y < ALTO_PANTALLA:
                    colision = False
                    punto_rect = pygame.Rect(x, y, 1, 1)
                    for obstaculo in obstaculos:
                        if obstaculo.colliderect(punto_rect):
                            colision = True
                            break
                    if not colision:
                        vecinos.append((x, y))
        return vecinos

    frontera = []
    heapq.heappush(frontera, (0, inicio))
    came_from = {}
    cost_so_far = {inicio: 0}
    came_from[inicio] = None

    while frontera:
        current = heapq.heappop(frontera)[1]

        if distancia(current, objetivo) < 20:
            break

        for next in obtener_vecinos(current):
            new_cost = cost_so_far[current] + distancia(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + distancia(objetivo, next)
                heapq.heappush(frontera, (priority, next))
                came_from[next] = current

    # Reconstruir camino
    path = []
    current = current
    while current != inicio:
        path.append(current)
        current = came_from.get(current, inicio)
    path.reverse()
    return path

# Clase para el nodo del algoritmo A*
class NodoAEstrella:
    def __init__(self, posicion, padre=None):
        self.posicion = posicion
        self.padre = padre
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, otro):
        return self.posicion == otro.posicion

# José Eduardo Williams 23-EISN-2-048
# Árbol de comportamiento
class Nodo:
    def ejecutar(self, enemigo, jugador_rect, obstaculos):
        raise NotImplementedError

class NodoPerseguir(Nodo):
    def __init__(self):
        self.ultimo_calculo = 0  # Controla el tiempo del último cálculo de camino

    def ejecutar(self, enemigo, jugador_rect, obstaculos):
        # Movimiento directo hacia el jugador
        dx = jugador_rect.centerx - enemigo.centerx
        dy = jugador_rect.centery - enemigo.centery
        distancia = math.hypot(dx, dy)

        if distancia > 0:
            dx /= distancia
            dy /= distancia

        # Mover al enemigo en la dirección del jugador
        enemigo.x += dx * ENEMIGO_VELOCIDAD
        enemigo.y += dy * ENEMIGO_VELOCIDAD

# José Eduardo Williams 23-EISN-2-048
class NodoMovimientoAleatorio(Nodo):
    def ejecutar(self, enemigo, jugador_rect, obstaculos):
        enemigo.x += random.choice([-1, 1]) * ENEMIGO_VELOCIDAD
        enemigo.y += random.choice([-1, 1]) * ENEMIGO_VELOCIDAD

class NodoCondicion(Nodo):
    def __init__(self, condicion, nodo_verdadero, nodo_falso):
        self.condicion = condicion
        self.nodo_verdadero = nodo_verdadero
        self.nodo_falso = nodo_falso

    def ejecutar(self, enemigo, jugador_rect, obstaculos):
        if self.condicion(enemigo, jugador_rect):
            self.nodo_verdadero.ejecutar(enemigo, jugador_rect, obstaculos)
        else:
            self.nodo_falso.ejecutar(enemigo, jugador_rect, obstaculos)

# José Eduardo Williams 23-EISN-2-048
def esta_cerca(enemigo, jugador_rect):
    return math.hypot(enemigo.centerx - jugador_rect.centerx, 
                    enemigo.centery - jugador_rect.centery) < 800

# Crear el árbol de comportamiento
arbol_comportamiento = NodoCondicion(
    esta_cerca,
    NodoPerseguir(),
    NodoMovimientoAleatorio()
)

def mover_enemigos(enemigos, jugador_rect, obstaculos):
    for enemigo in enemigos:
        # Calcular la dirección del enemigo hacia el jugador
        dx = jugador_rect.centerx - enemigo.centerx
        dy = jugador_rect.centery - enemigo.centery
        distancia = math.hypot(dx, dy)

        if distancia > 0:
            dx /= distancia
            dy /= distancia

        # Calcular el próximo movimiento
        nuevo_rect = enemigo.copy()
        nuevo_rect.x += dx * ENEMIGO_VELOCIDAD
        nuevo_rect.y += dy * ENEMIGO_VELOCIDAD

        # Comprobar colisiones con obstáculos
        colision_con_obstaculos = False
        for obstaculo in obstaculos:
            if nuevo_rect.colliderect(obstaculo):
                colision_con_obstaculos = True
                break

        # Si no hay colisión, mover al enemigo
        if not colision_con_obstaculos:
            enemigo.x += dx * ENEMIGO_VELOCIDAD
            enemigo.y += dy * ENEMIGO_VELOCIDAD
        else:
            pass

# José Eduardo Williams 23-EISN-2-048
# Función para rotar la imagen del enemigo
def rotar_imagen_enemigo(imagen, angulo):
    angulo += math.pi / 2  # Ajustar el ángulo para que la imagen apunte correctamente
    imagen_rotada = pygame.transform.rotate(imagen, -math.degrees(angulo))
    return imagen_rotada

# Función para rotar la imagen del jugador
def rotar_imagen_jugador(imagen, angulo):
    angulo += math.pi / 2
    imagen_rotada = pygame.transform.rotate(imagen, -math.degrees(angulo))
    return imagen_rotada

def evitar_solapamiento(enemigos):
    for i, enemigo1 in enumerate(enemigos):
        for j, enemigo2 in enumerate(enemigos):
            if i != j and enemigo1.colliderect(enemigo2):
                # Mover enemigo1 lejos de enemigo2
                dx = enemigo1.centerx - enemigo2.centerx
                dy = enemigo1.centery - enemigo2.centery
                distancia = math.hypot(dx, dy)
                if distancia == 0:
                    distancia = 1
                dx /= distancia
                dy /= distancia
                enemigo1.x += dx * ENEMIGO_VELOCIDAD
                enemigo1.y += dy * ENEMIGO_VELOCIDAD

# José Eduardo Williams 23-EISN-2-048
# Función principal del juego
def game_loop():
    global running
    running = True
    ronda = 1
    jugador_rect = pygame.Rect(ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2, 50, 50)
    disparos = []
    enemigos = generar_enemigos(ENEMIGO_RECUENTO_INICIAL)
    obstaculos = generar_obstaculos()
    tiempo_ultimo_disparo = 0
    clock = pygame.time.Clock()

    while running:
        screen.blit(imagen_fondo, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        jugador_rect.x, jugador_rect.y = mover_jugador(keys, jugador_rect.x, jugador_rect.y, obstaculos)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        angulo_jugador = math.atan2(mouse_y - jugador_rect.centery, mouse_x - jugador_rect.centerx)
        imagen_rotada_jugador = rotar_imagen_jugador(imagen_jugador, angulo_jugador)
        imagen_rect_jugador = imagen_rotada_jugador.get_rect(center=jugador_rect.center)

        tiempo_ultimo_disparo = disparar(jugador_rect, disparos, tiempo_ultimo_disparo)
        mover_balas(disparos)
        mover_enemigos(enemigos, jugador_rect, obstaculos)  # Mover enemigos usando el árbol de comportamiento
        evitar_solapamiento(enemigos)
        if revisar_colisiones(disparos, enemigos, jugador_rect):
            pantalla_derrota()
            running = False

        if not enemigos:
            if ronda < 4:
                ronda += 1
                enemigos = generar_enemigos(ENEMIGO_RECUENTO_INICIAL + (ronda - 1) + 3)
                jugador_rect.center = (ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2)
            else:
                pantalla_victoria()
                running = False

        for obstaculo in obstaculos:
            screen.blit(imagen_obstaculo, (obstaculo.x, obstaculo.y))
        for enemigo in enemigos:
            # Calcular el ángulo entre el enemigo y el jugador
            angulo_enemigo = math.atan2(jugador_rect.centery - enemigo.centery, jugador_rect.centerx - enemigo.centerx)
            imagen_rotada_enemigo = rotar_imagen_enemigo(imagen_enemigo, angulo_enemigo)
            imagen_rect_enemigo = imagen_rotada_enemigo.get_rect(center=enemigo.center)
            screen.blit(imagen_rotada_enemigo, imagen_rect_enemigo)
        for disparo in disparos:
            disparo_rect = disparo[0]
            imagen_rotada_disparo = rotar_imagen_jugador(imagen_disparo, disparo[2])
            screen.blit(imagen_rotada_disparo, (disparo_rect.x, disparo_rect.y))

        screen.blit(imagen_rotada_jugador, imagen_rect_jugador)
        dibujar_contador(f"Ronda: {ronda}/4", 10, 10)
        dibujar_contador(f"Enemigos restantes: {len(enemigos)}", 10, 40)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()

# Mostrar pantalla de inicio y ejecutar el juego
pantalla_inicio()
game_loop()
# José Eduardo Williams 23-EISN-2-048