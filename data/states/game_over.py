import pygame as pg
from .. import (
    prepare,
    tools,
    label,
    enemy,
    player,
    menu_manager,
)

class GameOver(tools.States, menu_manager.MenuManager):
    def __init__(self):
        tools.States.__init__(self)
        menu_manager.MenuManager.__init__(self)
        self.next = 'menu'
        self.game_over_label = label.GameOverText(prepare.SCREEN_RECT)
    def cleanup(self):
        print('cleaning up Game state stuff')
    def startup(self):
        print('starting Game state stuff')
    def get_event(self, event):
        if event.type == pg.KEYDOWN or event.type == pg.MOUSEBUTTONDOWN:
            self.done = True
    def update(self, screen, dt, keys):
        self.draw(screen)
    def draw(self, screen):
        prepare.SCREEN.fill((0,0,0))
        self.game_over_label.draw(prepare.SCREEN)
