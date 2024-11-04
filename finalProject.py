import random
import pygame
from pygame.locals import *

#Initializes Pygame. Variables are set here.
pygame.init()

screen_width = 800
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Final Platformer')


rect_1 = pygame.Rect(200, 100, 150, 100)

clock = pygame.time.Clock()


#random color list
color_list = ["Red", "Blue", "Green"]
index = random.randrange(len(color_list))
rand_color = str(color_list[index])

#load images



#Game Loop
running = True

while running:
    
    black = pygame.Color(0, 0, 0)
    screen.fill(black)

    pygame.draw.rect(screen, (255, 0, 0), rect_1)
    #pygame.draw.rect(screen, (255,0,0), (0, 0), 10, 10)

    
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type ==  pygame.KEYDOWN and event.key == pygame.K_f:
                pygame.display.toggle_fullscreen()
    
    pygame.display.update()
    pygame.display.flip()

pygame.quit()