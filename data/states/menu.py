import pygame as pg
from .. import tools, label, prepare

class Menu(tools.States):
    def __init__(self):
        tools.States.__init__(self)
        self.next = 'game'
        self.info = label.TopLeftText((100,100), 'Press mouse button to start', None, prepare.SCREEN_RECT)
    def cleanup(self):
        print('cleaning up Menu state stuff')
    def startup(self):
        print('starting Menu state stuff')
    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            print('Menu State keydown')
        elif event.type == pg.MOUSEBUTTONDOWN:
            self.done = True
    def update(self, screen, dt, keys):
        self.draw(screen)
    def draw(self, screen):
        screen.fill((255,0,0))
        self.info.draw(prepare.SCREEN)
        
