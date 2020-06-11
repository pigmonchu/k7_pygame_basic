import pygame as pg
from pygame.locals import *
from sprites import *
import sys, random

WIN_GAME_SCORE = 3


class Game:
    def __init__(self):
        self.pantalla = pg.display.set_mode((800, 600))
        self.pantalla.fill(BACKGROUND)
        self.fondo = pg.image.load("./resources/images/futbol.png")
        self.ball = Ball()
        self.playerOne = Raquet(30,1)
        self.playerTwo = Raquet(770,2)

        self.status = 'Partida'

        self.font = pg.font.Font('./resources/fonts/font.ttf', 40)
        self.fontGrande = pg.font.Font('./resources/fonts/font.ttf', 60)

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
        self.marcadorOne = self.font.render(str(self.scoreOne), True, RED)
        self.marcadorTwo = self.font.render(str(self.scoreOne), True, RED)

        while not game_over:
            game_over = self.handlenEvent()

            self.ball.update(800, 600)
            self.playerOne.update(800, 600)
            self.playerTwo.update(800, 600)
            if self.ball.comprobarChoque(self.playerOne):
                self.playerOne.impacto = True
            if self.ball.comprobarChoque(self.playerTwo):
                self.playerTwo.impacto = True
            if self.ball.vx == 0 and self.ball.vy == 0:
                if self.ball.rect.centerx >=800:
                    self.scoreOne += 1
                    self.marcadorOne = self.font.render(str(self.scoreOne), True, RED)
                if self.ball.rect.centerx <= 0:
                    self.scoreTwo += 1
                    self.marcadorTwo = self.font.render(str(self.scoreTwo), True, RED)

                if self.scoreOne == WIN_GAME_SCORE or self.scoreTwo == WIN_GAME_SCORE:
                    game_over = True

                self.ball.reset()

            self.pantalla.blit(self.fondo, (0, 0))
            self.pantalla.blit(self.ball.image, (self.ball.rect.x, self.ball.rect.y))
            self.pantalla.blit(self.playerOne.image, (self.playerOne.rect.x, self.playerOne.rect.y))
            self.pantalla.blit(self.playerTwo.image, (self.playerTwo.rect.x, self.playerTwo.rect.y))
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
