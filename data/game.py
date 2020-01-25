import pygame as pg
from . import (
    prepare,
    tools,
    label,
    enemy,
    player,
)

class Game(tools.States):
    def __init__(self):
        tools.States.__init__(self)
        self.next = 'menu'
        self.game_over_label = label.GameOverText(prepare.SCREEN_RECT)
        self.score_label = label.TopLeftText((10,10), 'Score: {}', None, prepare.SCREEN_RECT)
        self.damage_label = label.TopLeftText((10,30), 'Damage: {}', None, prepare.SCREEN_RECT)
        self.player = player.Player(prepare.SCREEN_RECT)
        self.enemy_control = enemy.EnemyController()
    def cleanup(self):
        print('cleaning up Game state stuff')
    def startup(self):
        print('starting Game state stuff')
    def get_event(self, event):
        self.player.get_event(event)
    def update(self, screen, dt, keys):
        self.draw(screen)
        if not self.player.dead:
            self.player.update(keys, dt, self.enemy_control.enemies)
            self.enemy_control.update(dt, self.player, self.score_label, self.damage_label)
        else:
            self.game_over_label.draw(prepare.SCREEN)
    def draw(self, screen):
        prepare.SCREEN.fill((0,0,0))
        self.score_label.draw(prepare.SCREEN)
        self.damage_label.draw(prepare.SCREEN)
        self.player.draw(prepare.SCREEN)
