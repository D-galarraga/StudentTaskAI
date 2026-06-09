import pygame
import math
import time
from Utils import escalar_imagen, blit_rotar_centro, blit_text_center


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


#print(ComputadoraCarro.path)
pygame.quit()