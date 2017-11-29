
import pygame as pg
from . import laser, prepare
import random
import math

class EnemyController:
    def __init__(self):
        self.enemies = [ ]
        self.enemy_image = self.enemy_image_load()
        self.max_enemies = 3
        for i in range(self.max_enemies):
            self.enemies.append(self.randomized_enemy())
         
    def enemy_image_load(self):
        #image = pg.image.load('enemy.png').convert()
        image = prepare.GFX['enemy']
        image.set_colorkey((255,0,255))
        transformed_image = pg.transform.rotate(image, 180)
        orig_image = pg.transform.scale(transformed_image, (40,80))
        orig_image = orig_image.convert_alpha()
        mask = pg.mask.from_surface(orig_image)
        return (orig_image, mask)
             
    def randomized_enemy(self):
        y = random.randint(-500, -100) #above screen
        x = random.randint(0, prepare.SCREEN_RECT.width)
        return Enemy(self.enemy_image, prepare.SCREEN_RECT, (x,y))
         
    def update(self, dt, player, score_label, damage_label):
        for e in self.enemies[:]:
            hit_player = e.update(dt, player)
            if hit_player:
                damage_label.update(player.damage)
            if e.dead:
                self.enemies.remove(e)
                player.add_score(25)
                score_label.update(player.score)
                self.enemies.append(self.randomized_enemy())
            e.draw(prepare.SCREEN)


class Enemy:
    total = 3
    def __init__(self, images, screen_rect, start_pos):
        self.screen_rect = screen_rect
        self.image = images[0]
        #self.image.set_colorkey((255,0,255))
        self.mask = images[1]
        start_buffer = 0
        self.rect = self.image.get_rect(
            center=(start_pos[0], start_pos[1])
        )
        self.distance_above_player = 100 
        self.speed = 2
        self.bullet_color = (255,0,0)
        self.is_hit = False
        self.range_to_fire = False
        self.timer = 0.0
        self.bullets = [ ]
        self.dead = False
           
    def pos_towards_player(self, player_rect):
        c = math.sqrt((player_rect.x - self.rect.x) ** 2 + (player_rect.y - self.distance_above_player  - self.rect.y) ** 2)
        try:
            x = (player_rect.x - self.rect.x) / c
            y = ((player_rect.y - self.distance_above_player)  - self.rect.y) / c
        except ZeroDivisionError: 
            return False
        return (x,y)
           
    def update(self, dt, player):
        new_pos = self.pos_towards_player(player.rect)
        if new_pos: #if not ZeroDivisonError
            self.rect.x, self.rect.y = (self.rect.x + new_pos[0] * self.speed, self.rect.y + new_pos[1] * self.speed)
           
        self.check_attack_ability(player)
        if self.range_to_fire:  
            if pg.time.get_ticks() - self.timer > 1500.0:
                self.timer = pg.time.get_ticks()
                self.bullets.append(laser.Laser(self.rect.center, self.bullet_color))
                   
        return self.update_bullets(player)
                   
    def draw(self, surf):
        if self.bullets:
            for bullet in self.bullets:
                surf.blit(bullet.image, bullet.rect)
        surf.blit(self.image, self.rect)
           
    def check_attack_ability(self, player):
        #if player is lower than enemy
        if player.rect.y >= self.rect.y: 
            try:
                offset_x =  self.rect.x - player.rect.x
                offset_y =  self.rect.y - player.rect.y
                d = int(math.degrees(math.atan(offset_x / offset_y)))
            except ZeroDivisionError: #player is above enemy
                return
            #if player is within 15 degrees lower of enemy
            if math.fabs(d) <= 15: 
                self.range_to_fire = True
            else:
                self.range_to_fire = False
                   
    def update_bullets(self, player):
        if self.bullets:
            for obj in self.bullets[:]:
                obj.update('down')
                #check collision
                if obj.rect.colliderect(player.rect):
                    offset_x =  obj.rect.x - player.rect.x 
                    offset_y =  obj.rect.y - player.rect.y
                    if player.mask.overlap(obj.mask, (offset_x, offset_y)):
                        player.take_damage(1)
                        self.bullets.remove(obj)
                        return True
                        
