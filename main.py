import pygame as pg
from pygame.locals import *
import sys

BACKGROUND = (0,240,0)
YELLOW = (255, 255, 0)
class Ball: 
    def __init__(self):
        self.vx = 5
        self.vy = 5
        self.Cx = 400
        self.Cy = 300
        self.h = 20
        self.w = 20

        self.image = pg.Surface((20, 20))
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



class Game:
    def __init__(self):
        self.pantalla = pg.display.set_mode((800, 600))
        self.pantalla.fill(BACKGROUND)
        self.fondo = pg.image.load("./resources/images/fondo.jpg")
        self.ball = Ball()

        pg.display.set_caption("Pong")

    def main_loop(self):
        game_over = False

        while not game_over:
            for event in pg.event.get():
                if event.type == QUIT:
                    game_over = True

            self.pantalla.blit(self.fondo, (0, 0))
            self.pantalla.blit(self.ball.image, (self.ball.posx, self.ball.posy))

            self.ball.move(800, 600)

            pg.display.flip()

    def quit(self):
        pg.quit()
        sys.exit()


if __name__ == "__main__":
    pg.init()
    game = Game()
    game.main_loop()
    game.quit()
