#from https://www.digitalocean.com/community/tutorials/how-to-install-pygame-and-create-a-template-for-developing-games-in-python-3
import pygame
from pygame.locals import *


pygame.init()

display_width = 800
display_height = 600

game_display = pygame.display.set_mode((display_width, display_height))

pygame.display.update()

while True:
    for event in pygame.event.get():
        print(event)