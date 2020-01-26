import pygame as pg
from .. import tools, label, prepare

class Options(tools.States):
    def __init__(self):
        tools.States.__init__(self)
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
        elif event.type == pg.KEYDOWN:
            if event.key in [pg.K_UP, pg.K_w]:
                self.change_selected_option(-1)
            elif event.key in [pg.K_DOWN, pg.K_s]:
                self.change_selected_option(1)
                
            elif event.key == pg.K_RETURN:
                self.select_option(self.selected_index)
        self.mouse_menu_click(event)
    def update(self, screen, dt, keys):

        self.mouse_hover_sound()
        self.change_selected_option()
        self.draw(screen)
    def draw(self, screen):
        screen.fill((0,255,0))
        for i,opt in enumerate(self.rendered["des"]):
            opt[1].center = (prepare.SCREEN_RECT.centerx, self.from_bottom+i*self.spacer)
            if i == self.selected_index:
                rend_img,rend_rect = self.rendered["sel"][i]
                rend_rect.center = opt[1].center
                screen.blit(rend_img,rend_rect)
            else:
                screen.blit(opt[0],opt[1])
