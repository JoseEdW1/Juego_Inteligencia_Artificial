# José Eduardo Williams 23-EISN-2-048
import pygame
import random
import math
import time

# Inicializar Pygame
pygame.init()

# Dimensiones de la ventana
ancho_pantalla = 800
alto_pantalla = 600
screen = pygame.display.set_mode((ancho_pantalla, alto_pantalla))
pygame.display.set_caption("Survive Cube")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)

# José Eduardo Williams 23-EISN-2-048
# Configuración del personaje
ancho_jugador = 50
alto_jugador = 50
jugador_x = ancho_pantalla // 2
jugador_y = alto_pantalla // 2
jugador_velocidad = 5

# Configuración de los enemigos
enemigo_ancho = 50
enemigo_alto = 50
enemigo_velocidad = 2
enemigo_conteo = 10

# Configuración de los obstáculos
obstaculo_ancho = 100
obstaculo_alto = 20

# Fuente para el texto
font = pygame.font.SysFont("Arial", 30)

# José Eduardo Williams 23-EISN-2-048
# Función para mostrar texto en pantalla
def dibujar_contador(text, x, y):
    label = font.render(text, True, BLANCO)
    screen.blit(label, (x, y))

# Función para mover al jugador
def mover_jugador(keys, x, y):
    if keys[pygame.K_w]:
        y -= jugador_velocidad
    if keys[pygame.K_s]:
        y += jugador_velocidad
    if keys[pygame.K_a]:
        x -= jugador_velocidad
    if keys[pygame.K_d]:
        x += jugador_velocidad
    return x, y


# Función para generar enemigos desde los bordes
def generar_enemigos(count):
    enemigos = []
    for _ in range(count):
        side = random.choice(['top', 'bottom', 'left', 'right'])
        if side == 'top':
            x = random.randint(0, ancho_pantalla - enemigo_ancho)
            y = 0
        elif side == 'bottom':
            x = random.randint(0, ancho_pantalla - enemigo_ancho)
            y = alto_pantalla - enemigo_alto
        elif side == 'left':
            x = 0
            y = random.randint(0, alto_pantalla - enemigo_alto)
        elif side == 'right':
            x = ancho_pantalla - enemigo_ancho
            y = random.randint(0, alto_pantalla - enemigo_alto)
        enemigos.append(pygame.Rect(x, y, enemigo_ancho, enemigo_alto))
    return enemigos

# José Eduardo Williams 23-EISN-2-048
# Función para mover los enemigos hacia el jugador
def mover_enemigos(enemigos, jugador_rect):
    for enemigo in enemigos:
        angulo = math.atan2(jugador_rect.centery - enemigo.centery, jugador_rect.centerx - enemigo.centerx)
        velocidad = [math.cos(angulo) * enemigo_velocidad, math.sin(angulo) * enemigo_velocidad]
        enemigo.x += velocidad[0]
        enemigo.y += velocidad[1]

# Función para disparar (con temporizador)
def disparar(jugador_rect, disparos, ultimo_disparo):
    tiempo_actual = time.time()
    if tiempo_actual - ultimo_disparo > 2:  # Disparar solo si han pasado 2 segundos
        if pygame.mouse.get_pressed()[0]:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            angulo = math.atan2(mouse_y - jugador_rect.centery, mouse_x - jugador_rect.centerx)
            velocidad = [math.cos(angulo) * 5, math.sin(angulo) * 5]
            disparo = pygame.Rect(jugador_rect.centerx - 5, jugador_rect.centery - 5, 10, 10)
            disparos.append([disparo, velocidad])
            ultimo_disparo = tiempo_actual  # Actualizar el tiempo del último disparo
    return ultimo_disparo

# José Eduardo Williams 23-EISN-2-048
# Función para mover las balas
def mover_balas(disparos):
    for disparo in disparos:
        disparo[0].x += disparo[1][0]
        disparo[0].y += disparo[1][1]

# Función para detectar colisiones
def revisar_colisiones(disparos, enemigos, obstaculos, jugador_rect):
    global running
    for disparo in disparos[:]:
        for enemigo in enemigos[:]:
            if disparo[0].colliderect(enemigo):
                enemigos.remove(enemigo)
                disparos.remove(disparo)
                break
        for obstaculo in obstaculos:
            if disparo[0].colliderect(obstaculo):
                disparos.remove(disparo)
                break
    for enemigo in enemigos:
        if enemigo.colliderect(jugador_rect):
            running = False  # El jugador pierde el juego si un enemigo lo toca

# Función para mover los obstáculos
def mover_obstaculos(obstaculos):
    for obstaculo in obstaculos:
        obstaculo.x = random.randint(0, ancho_pantalla - obstaculo_ancho)
        obstaculo.y = random.randint(0, alto_pantalla - obstaculo_alto)

# José Eduardo Williams 23-EISN-2-048
# Función para crear obstáculos
def crear_obstaculos():
    obstaculos = []
    for _ in range(5):  # Número de obstáculos
        x = random.randint(0, ancho_pantalla - obstaculo_ancho)
        y = random.randint(0, alto_pantalla - obstaculo_alto)
        obstaculos.append(pygame.Rect(x, y, obstaculo_ancho, obstaculo_alto))
    return obstaculos

# José Eduardo Williams 23-EISN-2-048
# Función principal
def game_loop():
    global running, enemigo_conteo
    running = True
    jugador_rect = pygame.Rect(jugador_x, jugador_y, ancho_jugador, alto_jugador)
    disparos = []
    enemigos = generar_enemigos(enemigo_conteo)
    obstaculos = crear_obstaculos()
    ultimo_disparo = time.time()  # Iniciar temporizador para disparos
    clock = pygame.time.Clock()

    while running:
        screen.fill(NEGRO)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        jugador_rect.x, jugador_rect.y = mover_jugador(keys, jugador_rect.x, jugador_rect.y)

        ultimo_disparo = disparar(jugador_rect, disparos, ultimo_disparo)
        mover_balas(disparos)
        mover_enemigos(enemigos, jugador_rect)
        revisar_colisiones(disparos, enemigos, obstaculos, jugador_rect)

        if not enemigos:
            enemigo_conteo += 4
            enemigos = generar_enemigos(enemigo_conteo)
            mover_obstaculos(obstaculos)

        dibujar_contador(f"Enemigos restantes: {len(enemigos)}", 10, 10)

        for enemigo in enemigos:
            pygame.draw.rect(screen, ROJO, enemigo)

        for obstaculo in obstaculos:
            pygame.draw.rect(screen, VERDE, obstaculo)

        for disparo in disparos:
            pygame.draw.rect(screen, BLANCO, disparo[0])

        pygame.draw.rect(screen, AZUL, jugador_rect)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()

# Ejecutar el juego
game_loop()
# José Eduardo Williams 23-EISN-2-048