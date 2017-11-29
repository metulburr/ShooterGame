import pygame as pg
from . import laser, prepare

class Player:
    def __init__(self, screen_rect):
        self.screen_rect = screen_rect
        #self.image = pg.image.load('spaceship.png').convert()
        self.image = prepare.GFX['spaceship']
        self.image.set_colorkey((255,0,255))
        self.mask = pg.mask.from_surface(self.image)
        self.transformed_image = pg.transform.rotate(self.image, 180)
        start_buffer = 300
        self.rect = self.image.get_rect(
            center=(screen_rect.centerx, screen_rect.centery + start_buffer)
        )
        self.dx = 300
        self.dy = 300
        self.lasers = []
        self.timer = 0.0
        self.laser_delay = 500
        self.add_laser = False
        self.damage = 10
        self.score = 0
        self.dead = False
         
    def take_damage(self, value):
        self.damage -= value
     
    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                if self.add_laser:
                    self.lasers.append(laser.Laser(self.rect.center, self.screen_rect))
                    self.add_laser = False
                    prepare.SFX['beep'].play()
     
    def update(self, keys, dt, enemies):
        self.rect.clamp_ip(self.screen_rect)
        if keys[pg.K_LEFT]:
            self.rect.x -= self.dx * dt
        if keys[pg.K_RIGHT]:
            self.rect.x += self.dx * dt
        if keys[pg.K_UP]:
            self.rect.y -= self.dy * dt
        if keys[pg.K_DOWN]:
            self.rect.y += self.dy * dt
        if pg.time.get_ticks()-self.timer > self.laser_delay:
            self.timer = pg.time.get_ticks()
            self.add_laser = True
             
        self.check_laser_collision(enemies)
         
        if self.damage <= 0:
            self.damage = 0
            self.dead = True
            prepare.SFX['game_over'].play()
         
    def check_laser_collision(self, enemies):
        for laser in self.lasers[:]:
            laser.update()
            for e in enemies:
                if laser.rect.colliderect(e.rect):
                    offset_x =  laser.rect.x - e.rect.x 
                    offset_y =  laser.rect.y - e.rect.y
                    if e.mask.overlap(laser.mask, (offset_x, offset_y)):
                        e.dead = True
                        self.lasers.remove(laser)
                        break #otherwise would create a ValueError: list.remove(x): x not in list
             
    def draw(self, surf):
        for laser in self.lasers:
            laser.render(surf)
        surf.blit(self.transformed_image, self.rect)
         
    def add_score(self, amt):
        self.score += amt
