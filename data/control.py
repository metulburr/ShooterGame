import pygame as pg
import sys
from . import prepare
from .states import menu, game, options, game_over
  
class Control:
    def __init__(self):
        self.done = False
        self.screen = pg.display.set_mode(prepare.WINSIZE)
        self.clock = pg.time.Clock()
    def setup_states(self, state_dict, start_state):
        self.state_dict = state_dict
        self.state_name = start_state
        self.state = self.state_dict[self.state_name]
    def flip_state(self):
        self.state.done = False
        previous,self.state_name = self.state_name, self.state.next
        self.state.cleanup()
        self.state = self.state_dict[self.state_name]
        self.state.startup()
        self.state.previous = previous
    def update(self, dt):
        keys = pg.key.get_pressed()
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
        self.state.update(self.screen, dt, keys)
    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            self.state.get_event(event)
    def main_game_loop(self):
        while not self.done:
            delta_time = self.clock.tick(prepare.FPS)/1000.0
            self.event_loop()
            self.update(delta_time)
            pg.display.update()
  
  
app = Control()
state_dict = {
    'menu'      : menu.Menu(),
    'game'      : game.Game(),
    'options'   : options.Options(),
    'game_over' : game_over.GameOver(),
}
app.setup_states(state_dict, 'menu')
app.main_game_loop()
pg.quit()
sys.exit()
