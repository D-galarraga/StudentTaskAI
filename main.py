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