import pygame as pg
from .. import tools, label, prepare, menu_manager

class Options(tools.States, menu_manager.MenuManager):
    def __init__(self):
        tools.States.__init__(self)
        menu_manager.MenuManager.__init__(self)
        self.next = 'game'
        self.options = ['Audio', 'Graphics', 'Test', 'Back']
        self.next_list = ['options', 'options', 'options', 'menu']
        self.pre_render_options()
        self.from_bottom = 200
        self.spacer = 75
    def cleanup(self):
        print('cleaning up Menu state stuff')
    def startup(self):
        print('starting Menu state stuff')
    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        self.get_event_menu(event)
    def update(self, screen, dt, keys):
        self.update_menu()
        self.draw(screen)
    def draw(self, screen):
        screen.fill((0,255,0))
        self.draw_menu()
