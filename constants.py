############################
###      Game    ###########
###########################

#[game]
import pygame
import pygame.locals

pygame.init()
pygame.mixer.init()
pygame.font.init()

#[utils]
import os
import time
import random

############################
#####   REOUSRCES    #######
############################


#[COLORS]
def getColor(hexValue) -> tuple:
    "Must be in the form: #AAAAAA"
    hexValue = hexValue[1:]
    assert(len(hexValue) == 6)
    return (int(hexValue[:2], 16),
            int(hexValue[2:4], 16),
            int(hexValue[4:], 16)
            )

#using dimmer shades
BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
RED = (200, 0, 0)
BLUE = (0, 0, 200)
GREEN = (0, 255, 0)

YELLOW = (255, 255, 0)

BORDER_COLOR = getColor("#7777FF")
BACKGROUND_COLOR = getColor("#000000")



#[GAME]
FPS = 30

UP_DIRECTION = -1
DOWN_DIRECTION = 1
#time taken to make an impression to the user in seonds
IMPRESSION_TIME = 1000 / 1000


GRID_SIZE = 8
LEVELS = 3 #number of rows container players

SIDES = [('Chelsea', pygame.Color(0, 0, 200, 200)), ('Arsernal', RED)]
PLAYERS_PER_SIDE = (GRID_SIZE//2) * 3

#opponent

COMPUTER_AI = 'Computer'
COMPUTER_RANDOM = 'Random Computer'
COMPUTER_PSEUDO_AI = 'Pseudo AI Computer'
HUMAN = 'Human'

#game states
UNFINISHED = 'UNFINISHED'
STALEMATE = 'STALEMATE'
CHECKMATE = 'CHECKMATE'

#[WINDOW]
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
MIN_MARGIN = 50

BOX_SIZE  = (min(WINDOW_HEIGHT, WINDOW_HEIGHT) -MIN_MARGIN)//GRID_SIZE
GRID_BORDER = 8

WINDOW_MARGIN_X = (WINDOW_WIDTH - GRID_SIZE*BOX_SIZE) // 2
WINDOW_MARGIN_Y = (WINDOW_HEIGHT - GRID_SIZE*BOX_SIZE) // 2


WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.DOUBLEBUF, 32)
pygame.display.set_caption("Checkers")
pygame.display.set_icon(pygame.image.load("./assets/buttons-3.png"))

#main font

font = pygame.font.SysFont('Deja Vu Sans', 100, True)

#[SOUNDS]
PLAY = pygame.mixer.Sound('./assets/Cgame-alert.wav')
PLAY.set_volume(100)


GAME_END  = pygame.mixer.Sound('./assets/fanfare.wav')



# #music

pygame.mixer.music.load('./assets/GMepic_battle_music.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(.5)


print("✔🕙 All resources loaded...")
