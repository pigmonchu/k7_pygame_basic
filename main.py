import pygame as pg
from pygame.locals import *
import sys, random

BACKGROUND = (50,50,50)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

WIN_GAME_SCORE = 10

class Ball: 
    def __init__(self):
        self.reset()
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
            self.vx = 0
            self.vy = 0

        if self.Cy >= limSupY or self.Cy <=0:
            self.vy *= -1
                
        self.Cx += self.vx
        self.Cy += self.vy

    def comprobarChoque(self, something):
        dx = abs(self.Cx - something.Cx)
        dy = abs(self.Cy - something.Cy)

        if dx < (self.w + something.w)//2 and dy < (self.h +something.h) // 2:
            self.vx *= -1
            self.Cx += self.vx
            self.Cy += self.vy

    def reset(self):
        self.vx = random.choice([-7, -5, 5, 7])
        self.vy = random.choice([-7, -5, 5, 7]) 
        self.Cx = 400
        self.Cy = 300

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

        

class Game:
    def __init__(self):
        self.pantalla = pg.display.set_mode((800, 600))
        self.pantalla.fill(BACKGROUND)
        self.fondo = pg.image.load("./resources/images/fondo.jpg")
        self.ball = Ball()
        self.playerOne = Raquet(30)
        self.playerTwo = Raquet(770)

        self.font = pg.font.Font('./resources/fonts/PressStart2P-Regular.ttf', 36)

        self.marcadorOne = self.font.render("0", True, WHITE)
        self.marcadorTwo = self.font.render("0", True, WHITE)

        self.scoreOne = 0
        self.scoreTwo = 0
        pg.display.set_caption("Pong")


    def handlenEvent(self):
        for event in pg.event.get():
            if event.type == QUIT:
                return True
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
        
        return False

    def main_loop(self):
        game_over = False

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
                if self.ball.Cx <= 0:
                    self.scoreTwo += 1

                if self.scoreOne == 10 or self.scoreTwo == 10:
                    game_over = True

                self.ball.reset()



            self.pantalla.blit(self.fondo, (0, 0))
            self.pantalla.blit(self.ball.image, (self.ball.posx, self.ball.posy))
            self.pantalla.blit(self.playerOne.image, (self.playerOne.posx, self.playerOne.posy))
            self.pantalla.blit(self.playerTwo.image, (self.playerTwo.posx, self.playerTwo.posy))
            self.pantalla.blit(self.marcadorOne, (10, 10))
            self.pantalla.blit(self.marcadorTwo, (740, 10))

            pg.display.flip()

    def quit(self):
        pg.quit()
        sys.exit()


if __name__ == "__main__":
    pg.init()
    game = Game()
    game.main_loop()
    game.quit()
