import pygame as pg
from pygame.locals import *
import sys, random

BACKGROUND = (50,50,50)
YELLOW = (255, 255, 0)  
WHITE = (255, 255, 255)

WIN_GAME_SCORE = 3

class Movil:
    __vx = 0
    __vy = 0
    def __init__(self, x=0, y=0, w=10, h=10):
        self.Cx = x
        self.Cy = y
        self.w = w
        self.h = h
        

        self.image = pg.Surface((self.w, self.h))
        self.color = WHITE

    @property
    def posx(self):
        return self.Cx - self.w // 2
        
    @property
    def posy(self):
        return self.Cy - self.h // 2

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, value):
        self.__color = value
        self.image.fill(self.__color)

    @property
    def vx(self):
        return self.__vx

    @vx.setter
    def vx(self, value):
        self.__vx = value

    @property
    def vy(self):
        return self.__vy

    @vy.setter
    def vy(self, value):
        self.__vy = value

    def move(self):
        self.Cx += self.__vx
        self.Cy += self.__vy

    def comprobarChoque(self, something):
        dx = abs(self.Cx - something.Cx)
        dy = abs(self.Cy - something.Cy)

        return dx < (self.w + something.w)//2 and dy < (self.h +something.h) // 2

class Ball(Movil): 
    def __init__(self):
        super().__init__(400, 300, 20, 20)
        self.reset()
        self.color = YELLOW
        self.ping = pg.mixer.Sound('./resources/sounds/ping.wav')
        self.lost_point = pg.mixer.Sound('./resources/sounds/lost-point.wav')

 
    def move(self, limSupX, limSupY):
        if self.Cx >= limSupX or self.Cx <=0:
            self.vx = 0
            self.vy = 0
            self.lost_point.play()

        if self.Cy >= limSupY or self.Cy <=0:
            self.vy *= -1
            self.ping.play()

        super().move()


    def __expulsaMe(self, something):
        signo = abs(self.vx)/self.vx
        dx = signo * (something.Cx - self.Cx) + something.w//2 + self.w//2
        dt = abs(dx/self.vx)
        dy = int(round(self.vy * dt, 0))
        self.Cx += (dx * signo)
        self.Cy += dy

    def comprobarChoque(self, something):
        if super().comprobarChoque(something):
            self.vx *= -random.uniform(0.9, 1.2)
            self.vy *= random.uniform(0.9, 1.2)
            self.ping.play()
            self.__expulsaMe(something)

    def reset(self):
        self.vx = random.choice([-5, -3, 3, 5])
        self.vy = random.choice([-5, -3, 3, 5]) 
        self.Cx = 400
        self.Cy = 300

class Raquet(Movil):
    def __init__(self, Cx):
        super().__init__(Cx, 200, 25, 100)


    def move(self, limSupX, limSupY):
        super().move()

        if self.Cy < self.h //2:
            self.Cy = self.h // 2

        if self.Cy > limSupY - self.h // 2:
            self.Cy = limSupY - self.h // 2
        

class Game:
    def __init__(self):
        self.pantalla = pg.display.set_mode((800, 600))
        self.pantalla.fill(BACKGROUND)
        self.fondo = pg.image.load("./resources/images/fondo.jpg")
        self.ball = Ball()
        self.playerOne = Raquet(30)
        self.playerTwo = Raquet(770)

        self.status = 'Partida'

        self.font = pg.font.Font('./resources/fonts/font.ttf', 40)
        self.fontGrande = pg.font.Font('./resources/fonts/font.ttf', 60)

        self.marcadorOne = self.font.render("0", True, WHITE)
        self.marcadorTwo = self.font.render("0", True, WHITE)

        self.text_game_over = self.fontGrande.render("GAME OVER", True, YELLOW)
        self.text_insert_coin = self.font.render('<SPACE> - Inicio partida', True, WHITE)

        self.scoreOne = 0
        self.scoreTwo = 0
        pg.display.set_caption("Pong")


    def handlenEvent(self):
        for event in pg.event.get():
            if event.type == QUIT:
                self.quit()
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    self.playerOne.vy = -5
                if event.key == K_DOWN:
                    self.playerOne.vy = 5

                if event.key == K_w:
                    self.playerOne.vy = -5
                if event.key == K_z:
                    self.playerOne.vy = 5

        key_pressed = pg.key.get_pressed()
        if key_pressed[K_UP]:
            self.playerTwo.vy -= 1 
        elif key_pressed[K_DOWN]:
            self.playerTwo.vy += 1
        else:
            self.playerTwo.vy = 0

        if key_pressed[K_w]:
            self.playerOne.vy -= 1
        elif key_pressed[K_z]:
            self.playerOne.vy += 1
        else:
            self.playerOne.vy = 0
        
        return False

    def bucle_partida(self):
        game_over = False
        self.scoreOne = 0
        self.scoreTwo = 0
        self.marcadorOne = self.font.render(str(self.scoreOne), True, WHITE)
        self.marcadorTwo = self.font.render(str(self.scoreOne), True, WHITE)

        while not game_over:
            game_over = self.handlenEvent()

            self.ball.move(800, 600)
            self.playerOne.move(800, 600)
            self.playerTwo.move(800, 600)
            self.ball.comprobarChoque(self.playerOne)
            self.ball.comprobarChoque(self.playerTwo)

            if self.ball.vx == 0 and self.ball.vy == 0:
                if self.ball.Cx >=800:
                    self.scoreOne += 1
                    self.marcadorOne = self.font.render(str(self.scoreOne), True, WHITE)
                if self.ball.Cx <= 0:
                    self.scoreTwo += 1
                    self.marcadorTwo = self.font.render(str(self.scoreTwo), True, WHITE)

                if self.scoreOne == WIN_GAME_SCORE or self.scoreTwo == WIN_GAME_SCORE:
                    game_over = True

                self.ball.reset()

            self.pantalla.blit(self.fondo, (0, 0))
            self.pantalla.blit(self.ball.image, (self.ball.posx, self.ball.posy))
            self.pantalla.blit(self.playerOne.image, (self.playerOne.posx, self.playerOne.posy))
            self.pantalla.blit(self.playerTwo.image, (self.playerTwo.posx, self.playerTwo.posy))
            self.pantalla.blit(self.marcadorOne, (30, 10))
            self.pantalla.blit(self.marcadorTwo, (740, 10))

            pg.display.flip()

        self.status = 'Inicio'

    def bucle_inicio(self):
        inicio_partida = False
        while not inicio_partida:
            for event in pg.event.get():
                if event.type == QUIT:
                    self.quit()

                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        inicio_partida = True

            self.pantalla.fill((0,0, 255))
            self.pantalla.blit(self.text_game_over, (100, 100))
            self.pantalla.blit(self.text_insert_coin, (100, 200))     

            pg.display.flip()       

        self.status = 'Partida'


    def main_loop(self):

        while True:
            if self.status == 'Partida':
                self.bucle_partida()
            else:
                self.bucle_inicio()


    def quit(self):
        pg.quit()
        sys.exit()


if __name__ == "__main__":
    pg.init()
    game = Game()
    game.main_loop()
    game.quit()
