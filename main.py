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
        
        
        
        
    
    
    
    
    
    def movimiento_jugador(self, JugadorCarro):
        teclas = pygame.key.get_pressed()
        moviendo = False

        if teclas[pygame.K_a]:
            JugadorCarro.rotacion(left=True)
        if teclas[pygame.K_d]:
            JugadorCarro.rotacion(right=True)
        if teclas[pygame.K_w]:
            moviendo = True
            JugadorCarro.moverAdelante()
        if teclas[pygame.K_s]:
            moviendo = True
            JugadorCarro.moverAtras()
        if not moviendo:
            JugadorCarro.reducir_velocidad()


class Jugador_Carro(AbstractCar):
    IMG = RED_CAR
    POSICION_INICIAL = (180, 200)

    def reducir_velocidad(self):
        self.vel = max(self.vel - self.aceleracion/2, 0)
        self.move()

    def rebotar(self):
        self.vel = -self.vel
        self.move()

class Computadora_Caroo(AbstractCar):
    IMG = GREEN_CAR
    POSICION_INICIAL = (150, 200)
    def _init_(self, max_vel, rotation_vel, path=[]):
        super()._init_(max_vel, rotation_vel)
        self.path = path
        self.currentPoint = 0
        self.vel = max_vel

    #def dibujarPuntos(self,win):
     #   for point in self.path:
      #      pygame.draw.circle(win, (250, 0 , 0 ), point, 5 )

    def dibujar(self,win):
        super().dibujar(win)
        #self.dibujarPuntos(win)

    def calcularAngulo(self):
        target_x, target_y = self.path[self.currentPoint]
        x_diff = target_x - self.x
        y_diff = target_y - self.y
        if y_diff == 0:
            desired_radian_angle = math.pi/2
        else: desired_radian_angle = math.atan(x_diff/y_diff)

        if target_y > self.y:
            desired_radian_angle += math.pi

        difference_in_angle = self.angulo - math.degrees(desired_radian_angle)

        if difference_in_angle >= 180:
            difference_in_angle -= 360

        if difference_in_angle > 0:
            self.angulo -= min(self.rotacion_vel, abs(difference_in_angle))
        else:
            self.angulo += min(self.rotacion_vel, abs(difference_in_angle))
    def update_path_point(self):
        target = self.path[self.currentPoint]
        rect = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())
        if rect.collidepoint(*target):
            self.currentPoint += 1

    def move(self):
        if self.currentPoint >= len(self.path):
            return
        self.calcularAngulo()
        self.update_path_point()
        super().move()


    def next_level(self, level):
        self.reseteo()
        self.vel = self.max_vel + (level-1) * 0.2
        self.currentPoint = 0




def movimiento_jugador(JugadorCarro):
    teclas = pygame.key.get_pressed()
    moviendo = False

    if teclas[pygame.K_a]:
        JugadorCarro.rotacion(left=True)
    if teclas[pygame.K_d]:
        JugadorCarro.rotacion(right=True)
    if teclas[pygame.K_w]:
        moviendo = True
        JugadorCarro.moverAdelante()
    if teclas[pygame.K_s]:
        moviendo = True
        JugadorCarro.moverAtras()
    if not moviendo:
        JugadorCarro.reducir_velocidad()

def lineaDeMeta(JugadorCarro, ComputadoraCarro, game_info):
    if JugadorCarro.colision(TRACK_BORDER_MASK) != None:
        JugadorCarro.rebotar()
    ColisionComputadora = ComputadoraCarro.colision(FINISH_MASK, *FINISH_POSITION)
    if  ColisionComputadora != None:
        print("Computadora gana")

        blit_text_center(WIN , MAIN_FONT, "Perdiste! ")
        pygame.display.update()
        pygame.time.wait(5000)
        JugadorCarro.reseteo()
        ComputadoraCarro.reseteo()
        game_info.reinicio()


    ColisionJugador = JugadorCarro.colision(FINISH_MASK, *FINISH_POSITION)
    if  ColisionJugador != None:
        if ColisionJugador[1] == 0:
            JugadorCarro.rebotar()
        else:
            game_info.siguiente_nivel()
            JugadorCarro.reseteo()
            ComputadoraCarro.next_level(game_info.level)
            print("Ganaste")