import pygame as pg
from pygame.locals import *
import random 

BACKGROUND = (50,50,50)
YELLOW = (255, 255, 0)  
WHITE = (255, 255, 255)

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
        super().__init__(Cx, 300, 25, 100)


    def move(self, limSupX, limSupY):
        super().move()

        if self.Cy < self.h //2:
            self.Cy = self.h // 2

        if self.Cy > limSupY - self.h // 2:
            self.Cy = limSupY - self.h // 2
        
