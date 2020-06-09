import pygame as pg
from pygame.locals import *
import sys

BACKGROUND = (50,50,50)
YELLOW = (255, 255, 0)
class Ball: 
    def __init__(self):
        self.vx = 5
        self.vy = 5
        self.Cx = 400
        self.Cy = 300
        self.h = 20
        self.w = 20

        self.image = pg.Surface((self.w, self.h))
        self.image.fill(YELLOW)

    @property
    def posx(self):
        return self.Cx - self.w // 2
        
    @property
    def posy(self):
        return self.Cy - self.h // 2

    def move(self, limSupX, limSupY):
        if self.Cx >= limSupX or self.Cx <=0:
            self.vx *= -1

        if self.Cy >= limSupY or self.Cy <=0:
            self.vy *= -1
                
        self.Cx += self.vx
        self.Cy += self.vy


class Raquet:
    def __init__(self, Cx):
        self.vx = 0
        self.vy = 0
        self.w = 25
        self.h = 100
        self.Cx = Cx
        self.Cy = 300

        self.image = pg.Surface((self.w, self.h))
        self.image.fill((255, 255, 255))

    @property
    def posx(self):
        return self.Cx - self.w // 2
        
    @property
    def posy(self):
        return self.Cy - self.h // 2

    def move(self, limSupX, limSupY):
        self.Cx += self.vx
        self.Cy += self.vy

        if self.Cy < self.h //2:
            self.Cy = self.h // 2

        if self.Cy > limSupY - self.h // 2:
            self.Cy = limSupY - self.h // 2

        print('velocidad ({}, {})'.format(self.vx, self.vy))
        

class Game:
    def __init__(self):
        self.pantalla = pg.display.set_mode((800, 600))
        self.pantalla.fill(BACKGROUND)
        self.fondo = pg.image.load("./resources/images/fondo.jpg")
        self.ball = Ball()
        self.playerOne = Raquet(30)
        self.playerTwo = Raquet(770)
        pg.display.set_caption("Pong")

    def main_loop(self):
        game_over = False

        while not game_over:
            for event in pg.event.get():
                if event.type == QUIT:
                    game_over = True
                '''
                if event.type == KEYDOWN:
                    if event.key == K_UP:
                        self.playerOne.vy = -5


                    if event.key == K_DOWN:
                        self.playerOne.vy = 5
                '''
            key_pressed = pg.key.get_pressed()
            if key_pressed[K_UP]:
                self.playerTwo.vy = - 5
            elif key_pressed[K_DOWN]:
                self.playerTwo.vy = 5
            else:
                self.playerTwo.vy = 0

            if key_pressed[K_w]:
                self.playerOne.vy = - 5
            elif key_pressed[K_z]:
                self.playerOne.vy = 5
            else:
                self.playerOne.vy = 0


            self.pantalla.blit(self.fondo, (0, 0))
            self.pantalla.blit(self.ball.image, (self.ball.posx, self.ball.posy))
            self.pantalla.blit(self.playerOne.image, (self.playerOne.posx, self.playerOne.posy))
            self.pantalla.blit(self.playerTwo.image, (self.playerTwo.posx, self.playerTwo.posy))

            self.ball.move(800, 600)
            self.playerOne.move(800, 600)
            self.playerTwo.move(800, 600)

            pg.display.flip()

    def quit(self):
        pg.quit()
        sys.exit()


if __name__ == "__main__":
    pg.init()
    game = Game()
    game.main_loop()
    game.quit()
