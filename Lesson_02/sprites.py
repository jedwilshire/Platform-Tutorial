import pygame
from settings import *
class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self.game.all_sprites.add(self, layer = PLAYER_LAYER)
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(ORANGE)
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)
        self.pos = pygame.math.Vector2(x, y)
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)
        self.jumping = False
        
    def update(self):
        self.acc = pygame.math.Vector2(0, GRAVITY)
        self.check_keys()
        # apply friction to acceleration in x direction only
        self.acc.x += self.vel.x * FRICTION
        self.vel += self.acc
        
        # check platforms only if falling
        if self.vel.y > 0:
            self.jumping = False
            self.check_for_platforms()
        
        # allow for stopping if vel is near zero in either direction
        if abs(self.vel.x) < ZERO_TOLERANCE:
            self.vel.x = 0
        if abs(self.vel.y) < ZERO_TOLERANCE:
            self.vel.y = 0
    
        # dp = 1/2 * a * dt^2 + v*dt
        self.pos += 1/2 * self.acc * self.game.dt ** 2 + self.vel * self.game.dt
        
        # use bottom middle of sprite to position
        self.rect.midbottom = self.pos
    
    def check_for_platforms(self):
        self.rect.bottom += 2 # move down temporarily
        for platform in self.game.platforms:
            if platform.rect.collidepoint(self.rect.midbottom):
                self.pos.y = platform.rect.top
                self.vel.y = 0
                self.acc.y = 0
                return True
        self.rect.bottom -= 2 # move back to position
        return False
    
    def check_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pygame.K_RIGHT]:
            self.acc.x = PLAYER_ACC
        if keys[pygame.K_UP]:
            # check if on a platform need also be not jumping or you can boost jump through a platform
            if not self.jumping and self.check_for_platforms():
                self.vel.y = -JUMP_VEL
                self.jumping = True

class Platform(pygame.sprite.Sprite):
    def __init__(self, game, x, y, width, height):
        super().__init__()
        self.game = game
        self.game.platforms.add(self)
        self.game.all_sprites.add(self, layer = PLATFORM_LAYER)
        self.image = pygame.Surface((width * TILE_SIZE, height * TILE_SIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE