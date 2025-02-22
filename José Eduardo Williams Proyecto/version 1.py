# José Eduardo Williams 23-EISN-2-048
import pygame
import random
import math

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

# José Eduardo Williams 23-EISN-2-048
# Configuración del personaje
jugador_ancho = 50
jugador_alto = 50
jugador_x = ancho_pantalla // 2
jugador_y = alto_pantalla // 2
jugador_velocidad = 5

# Configuración de los enemigos
enemigo_ancho = 50
enemigo_alto = 50
enemigo_conteo = 10  # Número inicial de enemigos

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

# Función para generar enemigos
def generar_enemigos(count):
    enemigos = []
    for _ in range(count):
        x = random.randint(0, ancho_pantalla - enemigo_ancho)
        y = random.randint(0, alto_pantalla - enemigo_alto)
        enemigos.append(pygame.Rect(x, y, enemigo_ancho, enemigo_alto))
    return enemigos

# José Eduardo Williams 23-EISN-2-048
# Función para disparar
def disparar(jugador_rect, disparos):
    if pygame.mouse.get_pressed()[0]:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        angulo = math.atan2(mouse_y - jugador_rect.centery, mouse_x - jugador_rect.centerx)
        velocidad = [math.cos(angulo) * 10, math.sin(angulo) * 10]
        disparo = pygame.Rect(jugador_rect.centerx - 5, jugador_rect.centery - 5, 10, 10)
        disparos.append([disparo, velocidad])
    
# Función para mover las balas
def mover_disparos(disparos):
    for disparo in disparos:
        disparo[0].x += disparo[1][0]
        disparo[0].y += disparo[1][1]

# Función para detectar colisiones
def revisar_colision(disparos, enemigos, obstaculos):
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
    jugador_rect = pygame.Rect(jugador_x, jugador_y, jugador_ancho, jugador_alto)
    disparos = []
    enemigos = generar_enemigos(enemigo_conteo)
    obstaculos = crear_obstaculos()
    clock = pygame.time.Clock()

    running = True
    while running:
        screen.fill(NEGRO)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        jugador_rect.x, jugador_rect.y = mover_jugador(keys, jugador_rect.x, jugador_rect.y)

        disparar(jugador_rect, disparos)
        mover_disparos(disparos)
        revisar_colision(disparos, enemigos, obstaculos)

        dibujar_contador(f"Enemigos restantes: {len(enemigos)}", 10, 10)

        for enemigo in enemigos:
            pygame.draw.rect(screen, (255, 0, 0), enemigo)

        for obstaculo in obstaculos:
            pygame.draw.rect(screen, (0, 255, 0), obstaculo)

        for disparo in disparos:
            pygame.draw.rect(screen, (255, 255, 255), disparo[0])

        pygame.draw.rect(screen, (0, 0, 255), jugador_rect)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()

# Ejecutar el juego
game_loop()
# José Eduardo Williams 23-EISN-2-048