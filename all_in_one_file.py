import pygame as pg
import math
import random
import os
 
pg.mixer.pre_init(44100, -16, 1, 512)
pg.init()
   
class Enemy:
    total = 3
    def __init__(self, images, screen_rect, start_pos):
        self.screen_rect = screen_rect
        self.image = images[0]
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
                self.bullets.append(Laser(self.rect.center, self.bullet_color))
                   
        self.update_bullets(player)
                   
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
     
class Player:
    def __init__(self, screen_rect):
        self.screen_rect = screen_rect
        self.image = pg.image.load('spaceship.png').convert()
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
        TOOLS.update_damage(self.damage)
     
    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                if self.add_laser:
                    self.lasers.append(Laser(self.rect.center, self.screen_rect))
                    self.add_laser = False
                    TOOLS.laser.play()
     
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
            TOOLS.game_over_sound.play()
         
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
        TOOLS.update_text(self.score)
     
class EnemyController:
    def __init__(self):
        self.enemies = [ ]
        self.enemy_image = self.enemy_image_load()
        self.max_enemies = 3
        for i in range(self.max_enemies):
            self.enemies.append(self.randomized_enemy())
         
    def enemy_image_load(self):
        image = pg.image.load('enemy.png').convert()
        image.set_colorkey((255,0,255))
        transformed_image = pg.transform.rotate(image, 180)
        orig_image = pg.transform.scale(transformed_image, (40,80))
        mask = pg.mask.from_surface(orig_image)
        return (orig_image, mask)
             
    def randomized_enemy(self):
        y = random.randint(-500, -100) #above screen
        x = random.randint(0, screen_rect.width)
        return Enemy(self.enemy_image, screen_rect, (x,y))
         
    def update(self, dt, player):
        for e in self.enemies[:]:
            e.update(dt, player)
            if e.dead:
                self.enemies.remove(e)
                player.add_score(25)
                self.enemies.append(self.randomized_enemy())
            e.draw(screen)
             
class Tools:
    def __init__(self, screen):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.sound_init()
        self.font_init(self.screen_rect)
         
    def font_init(self, screen_rect):
        self.text_size = 15
        self.text_color = (255,255,255)
        self.score_pos = (10,10)
        self.damage_pos = (10,30)
        self.font = pg.font.SysFont('Arial', self.text_size)
        self.update_text()
        self.update_damage()
        self.game_over()
         
    def update_text(self, score=0):
        self.text, self.text_rect = self.make_text('Score: {}'.format(score), self.score_pos)
         
    def update_damage(self, damage=None):
        self.damage, self.damage_rect = self.make_text('Damage: {}'.format(damage), self.damage_pos)
         
    def make_text(self,message, pos):
        text = self.font.render(message,True,self.text_color)
        rect = text.get_rect(topleft=pos)
        return text, rect
         
    def game_over(self):
        game_over_font = pg.font.SysFont('Arial', 45)
        self.game_over_text = game_over_font.render('Game Over',True,(255,0,0))
        self.game_over_rect = self.game_over_text.get_rect(center=self.screen_rect.center)
         
    def draw(self):
        self.screen.blit(self.text, self.text_rect)
        self.screen.blit(self.damage, self.damage_rect)
         
    def sound_init(self):
        directory_of_sounds = '.' #current directory == '.'
        self.laser = self.load_sound_file('beep.wav', directory_of_sounds)
        self.laser.set_volume(.1)
        self.game_over_sound = self.load_sound_file('game_over.wav', directory_of_sounds)
        self.game_over_sound.set_volume(.2)
         
    def load_sound_file(self, filename, directory):
        fullname = os.path.join(directory, filename)
        return pg.mixer.Sound(fullname)
     
screen = pg.display.set_mode((800,600))
screen_rect = screen.get_rect()
TOOLS = Tools(screen)
player = Player(screen_rect)
enemy_control = EnemyController()
clock = pg.time.Clock()
done = False
while not done:
    keys = pg.key.get_pressed()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
        player.get_event(event)
    screen.fill((0,0,0))
    delta_time = clock.tick(60)/1000.0
    if not player.dead:
        player.update(keys, delta_time, enemy_control.enemies)
        enemy_control.update(delta_time, player)
    else:
        screen.blit(TOOLS.game_over_text, TOOLS.game_over_rect)
    player.draw(screen)
    TOOLS.draw()
    pg.display.update()
