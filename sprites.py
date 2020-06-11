import pygame as pg
from pygame.locals import *
import sys, random


DARK_GREY = (50,50,50)
YELLOW = (255, 255, 0)  
WHITE = (255, 255, 255)

WIN_GAME_SCORE = 3

class Ball(pg.sprite.Sprite):
    vx = 0
    vy = 0
    __color = WHITE

    def __init__(self):
        self.image = pg.Surface((20, 20))
        self.color = YELLOW
        self.image.fill(self.__color)
        self.rect = self.image.get_rect()
        self.reset()

        self.ping = pg.mixer.Sound('./resources/sounds/ping.wav')
        self.lost_point = pg.mixer.Sound('./resources/sounds/lost-point.wav')


    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, tupla_color):
        self.__color = tupla_color
        self.image.fill(self.__color)

    def reset(self):
        self.vx = random.choice([-7, -5, 5, 7])
        self.vy = random.choice([-7, -5, 5, 7]) 
        self.rect.centerx = 400
        self.rect.centery = 300

    def comprobarChoque(self, something):
        dx = abs(self.rect.centerx - something.rect.centerx)
        dy = abs(self.rect.centery - something.rect.centery)

        if dx < (self.rect.w + something.rect.w)//2 and dy < (self.rect.h +something.rect.h) // 2:
            self.vx *= -random.uniform(0.8, 1.3)
            self.vy *= random.uniform(0.8, 1.3)

            self.rect.centerx += self.vx
            self.rect.centery += self.vy
            self.ping.play()

    def update(self, limSupX, limSupY):
        if self.rect.centerx >= limSupX or self.rect.centerx <=0:
            self.vx = 0
            self.vy = 0
            self.lost_point.play()

        if self.rect.centery >= limSupY or self.rect.centery <=0:
            self.vy *= -1
            self.ping.play()
                
        self.rect.centerx += self.vx
        self.rect.centery += self.vy

class Raquet(pg.sprite.Sprite):
    vx = 0
    vy = 0
    __color = WHITE

    def __init__(self, centerx):
        self.image = pg.Surface((25, 100))
        self.image.fill(self.__color)
        self.rect = self.image.get_rect()
        self.rect.centerx = centerx
        self.rect.centery = 400

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, tupla_color):
        self.__color = tupla_color
        self.image.fill(self.__color)


    def update(self, limSupY):
        self.rect.centerx += self.vx
        self.rect.centery += self.vy

        if self.rect.centery < self.rect.h //2:
            self.rect.centery = self.rect.h // 2

        if self.rect.centery > limSupY - self.rect.h // 2:
            self.rect.centery = limSupY - self.rect.h // 2
