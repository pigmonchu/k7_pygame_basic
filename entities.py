import pygame as pg
from pygame.locals import *
import sys, random


DARK_GREY = (50,50,50)
YELLOW = (255, 255, 0)  
WHITE = (255, 255, 255)

WIN_GAME_SCORE = 3

class Movil:
    vx = 0
    vy = 0
    __color = WHITE
    def __init__(self, w, h, centerx=0, centery=0):
        self.w = w
        self.h = h
        self.Cx = centerx
        self.Cy = centery

        self.image = pg.Surface((self.w, self.h))
        self.image.fill(self.color)

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
    def color(self, tupla_color):
        self.__color = tupla_color
        self.image.fill(self.__color)
    '''
    def move(self, limSupX, limSupY):
        pass
    '''
    def move(self, *args, **kwargs):
        pass


class Ball(Movil):
    def __init__(self):
        super().__init__(20, 20)
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
                
        self.Cx += self.vx
        self.Cy += self.vy

    def reset(self):
        self.vx = random.choice([-7, -5, 5, 7])
        self.vy = random.choice([-7, -5, 5, 7]) 
        self.Cx = 400
        self.Cy = 300

    def comprobarChoque(self, something):
        dx = abs(self.Cx - something.Cx)
        dy = abs(self.Cy - something.Cy)

        if dx < (self.w + something.w)//2 and dy < (self.h +something.h) // 2:
            self.vx *= -random.uniform(0.8, 1.3)
            self.vy *= random.uniform(0.8, 1.3)

            self.Cx += self.vx
            self.Cy += self.vy
            self.ping.play()

class Raquet(Movil):
    def __init__(self, centerX):
        super().__init__(25, 100, centerX, 300)

    def move(self, limSupY):
        self.Cx += self.vx
        self.Cy += self.vy

        if self.Cy < self.h //2:
            self.Cy = self.h // 2

        if self.Cy > limSupY - self.h // 2:
            self.Cy = limSupY - self.h // 2
