import pygame as pg
 
from data import (
    prepare,
    tools,
    label,
    enemy,
    player,
)
    
game_over_label = label.GameOverText(prepare.SCREEN_RECT)
score_label = label.TopLeftText((10,10), 'Score: {}', None, prepare.SCREEN_RECT)
damage_label = label.TopLeftText((10,30), 'Damage: {}', None, prepare.SCREEN_RECT)
player = player.Player(prepare.SCREEN_RECT)
enemy_control = enemy.EnemyController()
clock = pg.time.Clock()
done = False
while not done:
    keys = pg.key.get_pressed()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
        player.get_event(event)
    prepare.SCREEN.fill((0,0,0))
    delta_time = clock.tick(60)/1000.0
    if not player.dead:
        player.update(keys, delta_time, enemy_control.enemies)
        enemy_control.update(delta_time, player, score_label, damage_label)
    else:
        game_over_label.draw(prepare.SCREEN)
    score_label.draw(prepare.SCREEN)
    damage_label.draw(prepare.SCREEN)
    player.draw(prepare.SCREEN)
    pg.display.update()
