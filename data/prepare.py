
import pygame as pg
import os
from . import tools

CAPTION = "ShooterGame"
WINSIZE = (800,600)

#stop delay on sound
pg.mixer.pre_init(44100, -16, 1, 512)

#intialization
pg.init()

SCREEN = pg.display.set_mode(WINSIZE)
SCREEN_RECT = SCREEN.get_rect()

#loading resources
SFX = tools.load_all_sfx(os.path.join('resources', 'sounds'))
GFX = tools.load_all_gfx(os.path.join('resources', 'images'))

#set sound volumes
SFX['beep'].set_volume(0.1)
SFX['game_over'].set_volume(0.2)
