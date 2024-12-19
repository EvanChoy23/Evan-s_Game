# This file was created by Evan Choy

import pygame as pg
from pygame.sprite import Sprite
from random import randint
import random
from settings import *

vec = pg.math.Vector2



#create the player class with a superclass of Sprite
class Player(Sprite):
    # this initializse the properties of the player class including x/y location and the game perameter so the player can interact with the game.
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((32, 32))
        self.image.fill((GRAY))
        # self.image = self.game.player_img
        self.rect = self.image.get_rect()
        # self.rect.x = x
        # self.rect.y = y
        # self.x = x * TILESIZE
        # self.y = y * TILESIZE
        self.pos = vec(x*TILESIZE, y*TILESIZE)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.speed = 5
        # self.vx, self.vy = 0, 0
        self.coin_count = 0
        self.lives = 3
        self.jump_power = 20
        self.jumping = False

    # Tell the game what to do when we press a certain key
    def get_keys(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.jump()
        if keys[pg.K_a]:
            self.vel.x -= self.speed
        # if keys[pg.K_s]:
        #     self.vy += self.speed
        if keys[pg.K_d]:
            self.vel.x += self.speed

    # tell the game how the player jumps
    def jump(self):
        # print("im trying to jump")
        # print(self.vel.y)
        self.rect.y += 2
        hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
        self.rect.y -= 2
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -self.jump_power

    # telling the game what to do when the player hits a wall
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - TILESIZE
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - TILESIZE
                    self.vel.y = 0
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y
                self.jumping = False
                    
        #         print("this works")
        #     else:
        #         print("not working for hits")
        # else:
        #     print("not working for dir check")

    # tells the game what to do when the player collides with something
    def collide_with_stuff(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            # if str(hits[0].__class__.__name__) == "Jump":
            #     self.jump_power += 10
            # print("ive gotten a powerup")
            if str(hits[0].__class__.__name__) == "Coin":
                self.coin_count += 1
                print("ive gotten a coin")
            if str(hits[0].__class__.__name__) == "Mob":
                self.lives -= 1
                print("ouch")
                self.game.score += 1
            if str(hits[0].__class__.__name__) == "Fastobj":
                self.lives -= 1
                print("ouch")
            if str(hits[0].__class__.__name__) == "Wierdobj":
                self.lives -= 1
                print("ouch")

            if str(hits[0].__class__.__name__) == "Life":
                self.lives += 1



    # tells the game what to do to update the player
    def update(self):
        self.acc = vec(0, GRAVITY)
        self.get_keys()
        self.acc.x += self.vel.x * FRICTION
        self.vel += self.acc
        # self.x += self.vx * self.game.dt
        # self.y += self.vy * self.game.dt

        if self.rect.x > WIDTH:
            self.rect.x = 0
            self.pos.x = self.rect.x

        if self.rect.x < 0:
            self.rect.x = WIDTH
            self.pos.x = self.rect.x

        if self.rect.y > HEIGHT:
            self.lives = 0


        # round tiny velocities down
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0

        # updating the player's position
        self.pos += self.vel + 0.5 *self.acc

        # checking for collisions
        self.rect.x = self.pos.x
        self.collide_with_walls('x')

        self.rect.y = self.pos.y
        self.collide_with_walls('y')

        self.collide_with_stuff(self.game.all_powerups, True)
        self.collide_with_stuff(self.game.all_coins, True)
        self.collide_with_stuff(self.game.all_mobs, True)

# add mobs
class Mob(Sprite):
    def __init__(self, game, x, y,):
        self.groups = game.all_sprites, game.all_mobs
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((randint(32, 96), randint(32, 96)))
        self.image.fill(LIGHTBLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.speed = randint(5, 10)
        #ChatGPT: resizing image sprites
        self.mob_img = pg.transform.scale(self.game.mob_img, self.image.get_size())
        self.mob2_img = pg.transform.scale(self.game.mob2_img, self.image.get_size())
        self.mob3_img = pg.transform.scale(self.game.mob3_img, self.image.get_size())
        self.image.blit(random.choice([self.mob_img, self.mob2_img, self.mob3_img]), (0, 0))
        # self.score = 0

    # tells the game what to do to update mobs.
    def update(self):
        self.rect.y += self.speed
        # if self.rect.x > WIDTH or self.rect.x < 0:
        #     self.speed *= -1
        #     self.rect.y += 32

        # what to do when the mob goes below the screen
        if self.rect.y > HEIGHT:
            self.rect.y = 0
            self.rect.x = randint(32, 918)
            self.speed += random.choice([-1,0.5,1])


# add weird objects
class Weirdobj(Sprite):
    def __init__(self, game, x, y,):
        self.groups = game.all_sprites, game.all_mobs
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((randint(32, 96), randint(32, 96)))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.speed = 10

    # update weird mobs
    def update(self):
        self.rect.y += self.speed
        self.rect.x += (randint(-32, 32))

        # what to do when the mob goes below the screen
        # if self.rect.y > HEIGHT:
        #     self.rect.y = 0
        #     self.rect.x = randint(32, 918)
        #     self.speed += random.choice([-1,0.5,1])

# add fast objects
class Fastobj(Sprite):
    def __init__(self, game, x, y,):
        self.groups = game.all_sprites, game.all_mobs
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((16, 64))
        # self.image.fill(GRAY)
        self.image = self.game.lightning_img
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.speed = 32

    # uptate fast objects
    def update(self):
        self.rect.y += self.speed
        
        if self.rect.y > HEIGHT:
            self.rect.y = 0
            self.rect.x = randint(32, 918)

# add walls
class Wall(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_walls
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((32,32))
        # self.image.fill(BLUE)
        self.image = self.game.floor_img
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


    def update(self):
        pass

# add powerups
class Jump(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_powerups
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

# add extra life powerup
class Life(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_powerups
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.speed = 1

    def update(self):
        self.rect.y += self.speed
