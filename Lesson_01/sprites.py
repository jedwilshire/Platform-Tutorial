import pygame
from settings import *
class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self.game.all_sprites.add(self)
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(ORANGE)
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)
        self.pos = pygame.math.Vector2(x, y)
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)
        #self.jumping = False
        
    def update(self):
        self.acc = pygame.math.Vector2(0, 0)
        self.check_keys()
        # applay friction to acceleration in x, y direction
        # turn off y direction later
        self.acc += self.vel * FRICTION
        self.vel += self.acc
        # allow for stopping if vel is near zero in either direction
        if abs(self.vel.x) < ZERO_TOLERANCE:
            self.vel.x = 0
        if abs(self.vel.y) < ZERO_TOLERANCE:
            self.vel.y = 0
    
        # dp = 1/2 * a * dt^2 + v*dt
        self.pos += 1/2 * self.acc * self.game.dt ** 2 + self.vel * self.game.dt
        # use bottom middle of sprite to position
        self.rect.midbottom = self.pos

    def check_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pygame.K_RIGHT]:
            self.acc.x = PLAYER_ACC
        if keys[pygame.K_UP]:
            self.acc.y = -PLAYER_ACC
        if keys[pygame.K_DOWN]:
            self.acc.y = PLAYER_ACC

class Platform(pygame.sprite.Sprite):
    def __init__(self, game, x, y, width, height):
        super().__init__()
        self.game = game
        self.game.platforms.add(self)
        self.game.all_sprites.add(self)
        self.image = pygame.Surface((width, height))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y