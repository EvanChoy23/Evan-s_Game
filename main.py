# This file was created by Evan Choy


#Git Test

# this is where we import libraries and modules
import pygame as pg
from settings import *
# from sprites import *
from sprites_side_scroller import *
from tilemap import *
from os import path
import sys
from utils import *

'''
Sources:
https://www.w3schools.com/python/ref_random_choice.asp - How to use random choice
https://www.color-meanings.com/shades-of-brown-color-names-html-hex-rgb-codes/ - Various shades of brown
https://www.rapidtables.com/web/color/RGB_Color.html - Even more colors

'''

'''
create a game where the player tries to survive falling objects

GOALS: survive as long as possible
RULES: don't get hit by the falling objects
FEEDBACK:
FREEDOM: x movement, jumping

'''

# create a game class that carries all the properties of the game and methods
class Game:
    def __init__(self):
        pg.init()
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Evan's really cool game")
        self.playing = True
        self.timer = Timer(self)
        self.score = self.timer.current_time

    def load_data(self):
        self.game_folder = path.dirname(__file__)
        # with open(path.join(self.game_folder, HS_FILE), 'w') as f:
        #     f.write(str(0))
        try:
            with open(path.join(self.game_folder, HS_FILE), 'r') as f:
                self.highscore = int(f.read())
        except:
            self.highscore = 0
            with open(path.join(self.game_folder, HS_FILE), 'w') as f:
              f.write(str(self.highscore))

        
        # load map
        self.map = Map(path.join(self.game_folder, 'level1.txt'))

        # this is where the game creates the stuff you see and hear
    def new(self):
        self.load_data()
        # create a group for sprites and walls using the pg library
        self.all_sprites = pg.sprite.Group()
        self.all_walls = pg.sprite.Group()
        self.all_mobs = pg.sprite.Group()
        self.all_powerups = pg.sprite.Group()
        self.all_coins = pg.sprite.Group()

        # instantiating the classes to create objects
        # self.player = Player(self, 64, 64)
        # self.mob = Mob(self, 50, 50)
        # wall = Wall(self, WIDTH//2, HEIGHT//2)

        # # loop creating wall
        # for i in range(6):
        #     w = Wall(self, TILESIZE*i, TILESIZE*i)
        #     m = Mob(self, TILESIZE*i, TILESIZE*i)

        # Wall(self, WIDTH//2, HEIGHT//2)

        # Create sprites using different characters
        for row, tiles in enumerate(self.map.data):
            # print(row)
            for col,tile in enumerate(tiles):
                # print(col)
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'M':
                    self.mob = Mob(self, col, row,)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'J':
                    Jump(self, col, row)
                if tile == 'L':
                    Life(self, col, row)
                if tile == 'W':
                    Weirdobj(self,col, row)
                if tile == 'F':
                    Fastobj(self, col, row)

    # running the game
    def run(self):
        self.running = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            # input
            self.events()
            # process
            self.update()
            # output
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit

    # input
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.score > self.highscore:
                    with open(path.join(self.game_folder, HS_FILE), 'w') as f:
                      f.write(str(self.score))
                self.playing = False
    # this is where the game updates the game state
    def update(self):
    # this is where the sprites get updated
        self.all_sprites.update()

        self.timer.ticking()
        # what to do when the player runs out of lives
        if self.player.lives == 0:
            self.show_death_screen()
            self.running = False

        # if self.timer.current_time == 10:
        #     Life(self, randint(32, 918), randint(32, 918))
        #     print("uhhh")

    # create a function to draw/create stuff on screen
    def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        surface.blit(text_surface, text_rect)

    # output
    def draw(self):
        # create the screen, and draw/write everything on the screen
        self.screen.fill((0, 0, 0))
        self.all_sprites.draw(self.screen)
        # self.draw_text(self.screen, "asdfdasfasdf", 24, WHITE, WIDTH/2, HEIGHT/2)
        self.draw_text(self.screen, str(self.dt*1000), 24, WHITE, WIDTH/30, HEIGHT/30)
        # self.draw_text(self.screen, str(self.player.coin_count), 24, WHITE, WIDTH-100, 50)
        # draw "lives" and "score"
        self.draw_text(self.screen, "Lives:" + str(self.player.lives), 24, WHITE, WIDTH-32, HEIGHT-32)
        self.draw_text(self.screen, "Score:" + str(self.score), 24, WHITE, 96, HEIGHT-32)
        self.draw_text(self.screen, "Highscore:" + str(self.highscore), 24, WHITE, WIDTH/2, HEIGHT-32)
        pg.display.flip()
    
    # create a death screen
    def show_death_screen(self):
        self.screen.fill(RED)
        self.draw_text(self.screen, "You Died!", 50, WHITE, WIDTH/2, HEIGHT/2)
        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False


#? What does this block of code do?
if __name__ == "__main__":
  # instantiate
  g = Game()
  g.new()
  g.run()  