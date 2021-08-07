import pygame
from colors import *
import os
from pygame import mixer

class Alimento:
    def __init__(self,x=0,y=0,dx=4,dy=0, width=30, height=30,color=RED):
        self.image = ""
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.width = width
        self.height = height
        self.color = color

    def load_image(self, img):
        self.image = pygame.image.load(img).convert()
        self.image = pygame.transform.scale(self.image,(50,50))
        self.image.set_colorkey(BLACK)

    def draw_image(self,screen):
        screen.blit(self.image,[self.x,self.y])

    def move_x(self):
        self.x +=self.dx

    def move_y(self):
        self.y +=self.dy

    def draw_rect(self,screen):
        pygame.draw.rect(screen,self.color,[self.x,self.y,self.width, self.height],0)

    def check_out_of_screen(self):
        if self.x + self.width > 400 or self.x < 0:
            self.x -=self.dx
