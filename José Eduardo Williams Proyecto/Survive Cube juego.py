# José Eduardo Williams 23-EISN-2-048
import pygame
import random
import math
import time

# Inicializar Pygame
pygame.init()

# Dimensiones de la ventana
ANCHO_PANTALLA = 1200
ALTO_PANTALLA = 900
screen = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption("Survive Cube")

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

# Reproducir música en bucle
pygame.mixer.music.play(-1)

# Colores
BLANCO = (255, 255, 255)

# Configuración del personaje
JUGADOR_VELOCIDAD = 3

# Configuración de los enemigos
ENEMIGO_VELOCIDAD = 1
ENEMIGO_RECUENTO_INICIAL = 10

# José Eduardo Williams 23-EISN-2-048
# Configuración de los obstáculos
OBSTACULO_ANCHO = 120
OBSTACULO_ALTO = 100
CANTIDAD_OBSTACULOS = 5

# Fuente para el texto
font = pygame.font.SysFont("Arial", 30)

# Función para mostrar texto en pantalla
def dibujar_contador(texto, x, y):
    label = font.render(texto, True, BLANCO)
    screen.blit(label, (x, y))

# José Eduardo Williams 23-EISN-2-048
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

# José Eduardo Williams 23-EISN-2-048
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
# Función para mover enemigos hacia el jugador
def mover_enemigos(enemigos, jugador_rect):
    for enemigo in enemigos:
        # Calcular la dirección hacia el jugador
        dx = jugador_rect.centerx - enemigo.centerx
        dy = jugador_rect.centery - enemigo.centery
        distancia = math.hypot(dx, dy)
        if distancia > 0:
            dx /= distancia
            dy /= distancia
        # Mover al enemigo
        enemigo.x += dx * ENEMIGO_VELOCIDAD
        enemigo.y += dy * ENEMIGO_VELOCIDAD

# Función para rotar la imagen del jugador
def rotar_imagen(imagen, angulo):
    angulo += math.pi / 2
    imagen_rotada = pygame.transform.rotate(imagen, -math.degrees(angulo))
    return imagen_rotada

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
        angulo = math.atan2(mouse_y - jugador_rect.centery, mouse_x - jugador_rect.centerx)
        imagen_rotada_jugador = rotar_imagen(imagen_jugador, angulo)
        imagen_rect = imagen_rotada_jugador.get_rect(center=jugador_rect.center)

        tiempo_ultimo_disparo = disparar(jugador_rect, disparos, tiempo_ultimo_disparo)
        mover_balas(disparos)
        mover_enemigos(enemigos, jugador_rect)  # Mover enemigos hacia el jugador
        if revisar_colisiones(disparos, enemigos, jugador_rect):
            pantalla_derrota()
            running = False

        if not enemigos:
            if ronda < 4:
                ronda += 1
                enemigos = generar_enemigos(ENEMIGO_RECUENTO_INICIAL + (ronda - 1) * 4)
                jugador_rect.center = (ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2)
            else:
                pantalla_victoria()
                running = False

        for obstaculo in obstaculos:
            screen.blit(imagen_obstaculo, (obstaculo.x, obstaculo.y))
        for enemigo in enemigos:
            screen.blit(imagen_enemigo, (enemigo.x, enemigo.y))
        for disparo in disparos:
            disparo_rect = disparo[0]
            imagen_rotada_disparo = rotar_imagen(imagen_disparo, disparo[2])
            screen.blit(imagen_rotada_disparo, (disparo_rect.x, disparo_rect.y))

        screen.blit(imagen_rotada_jugador, imagen_rect)
        dibujar_contador(f"Ronda: {ronda}/4", 10, 10)
        dibujar_contador(f"Enemigos restantes: {len(enemigos)}", 10, 40)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()

# Mostrar pantalla de inicio y ejecutar el juego
pantalla_inicio()
game_loop()
# José Eduardo Williams 23-EISN-2-048