import pygame as pg
from math import floor

class Timer():
    # set everything to 0 when instantiated
    def __init__(self, game):
        self.game = game
        self.current_time = 0
        self.event_time = 0
        self.cd = 0
    # ticking counts up and down
    def ticking(self):
        self.current_time = floor((pg.time.get_ticks())/1000)
        self.game.score += 1
    def get_current_time(self):
        self.current_time = floor((pg.time.get_ticks())/1000) 