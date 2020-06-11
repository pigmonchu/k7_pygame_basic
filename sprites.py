import pygame as pg
from pygame.locals import *
import random

BACKGROUND = (50,50,50)
YELLOW = (255, 255, 0)  
WHITE = (255, 255, 255)

class Ball(pg.sprite.Sprite):
    vx = 0
    vy = 0

    def __init__(self):
        self.image = pg.Surface((20, 20))
        self.image.fill(YELLOW)
        self.ping = pg.mixer.Sound('./resources/sounds/ping.wav')
        self.lost_point = pg.mixer.Sound('./resources/sounds/lost-point.wav')
        
        self.rect = self.image.get_rect()
        self.reset()

    def reset(self):
        self.vx = random.choice([-5, -3, 3, 5])
        self.vy = random.choice([-5, -3, 3, 5]) 
        self.rect.centerx = 400
        self.rect.centery = 300

    def update(self, limSupX, limSupY):
        if self.rect.centerx >= limSupX or self.rect.centerx <= 0:
            self.vx = 0
            self.vy = 0
            self.lost_point.play

        if self.rect.centery >= limSupY or self.rect.centery <= 0:
            self.vy *= -1
            self.ping.play()

        self.rect.centerx += self.vx
        self.rect.centery += self.vy

    def comprobarChoque(self, something):
        if self.rect.colliderect(something):
            self.vx *= -random.uniform(0.9, 1.2)
            self.vy *= random.uniform(0.9, 1.2)
            self.ping.play()
            self.__expulsaMe(something)

    def __expulsaMe(self, something):
        signo = abs(self.vx)/self.vx
        dx = signo * (something.rect.centerx - self.rect.centerx) + something.rect.w//2 + self.rect.w//2
        dt = abs(dx/self.vx)
        dy = int(round(self.vy * dt, 0))
        self.rect.centerx += (dx * signo)
        self.rect.centery += dy


class Raquet(pg.sprite.Sprite):
    vx = 0
    vy = 0
    def __init__(self, x):
        self.image = pg.Surface((25, 100))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = 300              

    def update(self, limSupX, limSupY):
        self.rect.centerx += self.vx
        self.rect.centery += self.vy

        if self.rect.centery < self.rect.h //2:
            self.rect.centery = self.rect.h // 2

        if self.rect.centery > limSupY - self.rect.h // 2:
            self.rect.centery = limSupY - self.rect.h // 2



