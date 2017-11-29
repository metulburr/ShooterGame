import pygame as pg

class Laser:
    def __init__(self, loc, screen_rect):
        self.screen_rect = screen_rect
        self.image = pg.Surface((5,40)).convert_alpha()
        #self.image.set_colorkey((255,0,255))
        self.mask = pg.mask.from_surface(self.image)
        self.image.fill((255,255,0))
        self.rect = self.image.get_rect(center=loc)
        self.speed = 5
     
    def update(self,direction='up'):
        if direction == 'down':
            self.rect.y += self.speed
        else:
            self.rect.y -= self.speed
     
    def render(self, surf):
        surf.blit(self.image, self.rect)
