# This file was created by Evan Choy

# this is where we import libraries and modules
import pygame as pg
from settings import *
from sprites import *
from tilemap import *
from os import path

'''
GOALS:
RULES:
FEEDBACK:
FREEDOM:

'''

# create a game class that carries all the properties of the game and methods
class Game:
    def __init__(self):
        pg.init()
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Evan's really cool game")
        self.playing = True
    def load_data(self):
        self.game_folder = path.dirname(__file__)
        self.map = Map(path.join(self.game_folder, 'level1.txt'))
        # this is where the game creates the stuff you see and hear
    def new(self):
        self.load_data()
        # create a group for sprites and walls using the pg library
        self.all_sprites = pg.sprite.Group()
        self.all_walls = pg.sprite.Group()
        self.all_powerups = pg.sprite.Group()
        self.all_coins = pg.sprite.Group()
        # instantiating the classes to create objects
        # self.player = Player(self, 5, 5)
        # self.mob = Mob(self, 50, 50)
        # self.wall = Wall(self, WIDTH//2, HEIGHT//2)

        # # loop creating wall
        # for i in range(6):
        #     w = Wall(self, TILESIZE*i, TILESIZE*i)
        #     m = Mob(self, TILESIZE*i, TILESIZE*i)
        for row, tiles in enumerate(self.map.data):
            print(row)
            for col,tile in enumerate(tiles):
                print(col)
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'M':
                    Mob(self,col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'U':
                    Powerup(self, col, row)
                if tile == 'C':
                    Coin(self, col, row)


    # running the game
    def run(self):
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            # input
            self.events()
            # process
            self.update()
            # output
            self.draw()
            

        pg.quit
    # input
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.playing = False
    # this is where the game updates the game state
    def update(self):
    # this is where the sprites get updated
        self.all_sprites.update()
    def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        surface.blit(text_surface, text_rect)

    # output
    def draw(self):
        self.screen.fill((0, 0, 0))
        self.all_sprites.draw(self.screen)
        self.draw_text(self.screen, "asdfdasfasdf", 24, WHITE, WIDTH/2, HEIGHT/2)
        self.draw_text(self.screen, str(self.dt*1000), 24, WHITE, WIDTH/30, HEIGHT/30)
        self.draw_text(self.screen, str(self.player.coin_count), 24, WHITE, WIDTH-100, 50)
        pg.display.flip()

#? What does this block of code do?
if __name__ == "__main__":
  # instantiate
  g = Game()
  g.new()
  g.run()    