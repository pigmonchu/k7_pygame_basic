import pygame as pg
from pygame.locals import *
import random

BACKGROUND = (50,50,50)
YELLOW = (255, 255, 0) 
RED = (255, 0, 0) 
WHITE = (255, 255, 255)
SPRITES_PATH = './resources/sprites/'

class Ball(pg.sprite.Sprite):
    vx = 0
    vy = 0
    sprite = 'f_{}.png'
    num_sprites = 12

    def __init__(self):
        self.image = pg.Surface((20, 20), pg.SRCALPHA, 32)
        self.images = self.loadImages()
        self.image_act = 0
        self.ping = pg.mixer.Sound('./resources/sounds/ping.wav')
        self.lost_point = pg.mixer.Sound('./resources/sounds/lost-point.wav')
        
        self.rect = self.image.get_rect()
        self.reset()

    def loadImages(self):
        return [pg.image.load(SPRITES_PATH + self.sprite.format(i)) for i in range(self.num_sprites)]

    def reset(self):
        self.vx = random.choice([-5, -3, 3, 5])
        self.vy = random.choice([-5, -3, 3, 5]) 
        self.rect.centerx = 400
        self.rect.centery = 300

    def update(self, limSupX, limSupY):
        self.image_act += 1
        self.image_act = self.image_act % self.num_sprites
        self.image.blit(self.images[self.image_act], (0,0))
        if self.rect.centerx >= limSupX or self.rect.centerx <= 0:
            self.vx = 0
            self.vy = 0
            self.lost_point.play()
            pg.time.delay(1000)

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
            return True
        return False

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
    sprite = 'p{}_{}.png'
    num_sprites = 8
    def __init__(self, x, player):
        self.image = pg.Surface((25, 100), pg.SRCALPHA, 32)
        self.images = self.loadImages(player)
        self.image_act = 0
        self.image.blit(self.images[self.image_act], (0,0))

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = 300
        self.impacto = False

    def loadImages(self, player):
        return [pg.image.load(SPRITES_PATH + self.sprite.format(player, i)) for i in range(self.num_sprites)]      

    def update(self, limSupX, limSupY):
        self.rect.centerx += self.vx
        self.rect.centery += self.vy

        if self.rect.centery < self.rect.h //2:
            self.rect.centery = self.rect.h // 2

        if self.rect.centery > limSupY - self.rect.h // 2:
            self.rect.centery = limSupY - self.rect.h // 2

        if self.impacto:
            self.image_act += 1
            if self.image_act >= self.num_sprites:
                self.image_act = 0
                self.impacto = False

            self.image = pg.Surface((25, 100), pg.SRCALPHA, 32)
            self.image.blit(self.images[self.image_act], (0,0))


            



