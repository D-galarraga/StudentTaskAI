import pygame
import math
import time
from Utils import escalar_imagen, blit_rotar_centro, blit_text_center

def dibujar(win, images, JugadorCarro, ComputadoraCarro):
    for img, pos in images:
        win.blit(img, pos)
    level_text =  MAIN_FONT.render(f"Nivel: {game_info.level}",1,(255,255,255))
    win.blit(level_text, (10, HEIGHT - level_text.get_height() - 70))
    time_text = MAIN_FONT.render(f"Tiempo: {round(game_info.getLevelTime(),1)} s", 1, (255, 255, 255))
    win.blit(time_text, (10, HEIGHT - time_text.get_height() - 40))
    vel_text = MAIN_FONT.render(f"Velocidad: {round(JugadorCarro.vel,1)} px/s", 1, (255, 255, 255))
    win.blit(vel_text, (10, HEIGHT - vel_text.get_height() - 10))
    JugadorCarro.dibujar(win)
    ComputadoraCarro.dibujar(win)
    pygame.display.update()

class AbstractCar:
    def _init_(self, max_vel, rotacion_vel):
        self.img = self.IMG
        self.max_vel = max_vel

        self.rotacion_vel = rotacion_vel
        self.vel = 0
        self.angulo = 0
        self.x, self.y = self.POSICION_INICIAL
        self.aceleracion = 0.1

    def rotacion (self, left = False, right = False):
        if left:
            self.angulo += self.rotacion_vel
        elif right:
            self.angulo -= self.rotacion_vel

    def dibujar(self, win):
        blit_rotar_centro(win, self.img,(self.x, self.y), self.angulo)

    def moverAdelante(self):
        self.vel = min(self.vel  + self.aceleracion, self.max_vel)
        self.move()

    def move(self):
        radianes = math.radians(self.angulo)
        vertical = math.cos(radianes) * self.vel
        horizontal = math.sin(radianes) * self.vel
        self.y -= vertical
        self.x -= horizontal



    def moverAtras(self):
        self.vel = max(self.vel - self.aceleracion, -self.max_vel/2)
        self.move()

    def colision(self, mask, x=0, y=0):
        carro_mascara = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(carro_mascara, offset)
        return poi

    def reseteo(self):
        self.x, self.y = self.POSICION_INICIAL
        self.angulo = 0
        self.vel = 0

#Codigo para el juego de carreras
run = True
clock = pygame.time.Clock()
images = [(GRASS, (0, 0)), (TRACK, (0, 0)), (FINISH, FINISH_POSITION), (TRACK_BORDER, (0,0))]
JugadorCarro = Jugador_Carro(4,4)
ComputadoraCarro= Computadora_Caroo(2,4, PATH)
game_info = informacionJuego()
while run:
    clock.tick(fps)
    dibujar(WIN, images, JugadorCarro, ComputadoraCarro)
    while not game_info.iniciado:
        blit_text_center(WIN, MAIN_FONT, f"Presiona cualquier tecla para iniciar el nivel {game_info.level}")
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break
            if event.type == pygame.KEYDOWN:
                game_info.iniciarNivel()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

        #if event.type == pygame.MOUSEBUTTONDOWN:
         #   pos = pygame.mouse.get_pos()
          #  ComputadoraCarro.path.append(pos)


    movimiento_jugador(JugadorCarro)
    ComputadoraCarro.move()
    lineaDeMeta(JugadorCarro, ComputadoraCarro, game_info)

    if game_info.juego_terminado():
        blit_text_center(WIN, MAIN_FONT, "Ganaste! ")
        pygame.time.wait(5000)
        JugadorCarro.reseteo()
        ComputadoraCarro.reseteo()
        game_info.reinicio()
pygame.quit()
