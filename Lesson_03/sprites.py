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
        self.previous_pos = self.pos
        self.previous_pos.y = self.pos.y - PLATFORM_TOP_THICKNESS
        
    def update(self):
        self.acc = pygame.math.Vector2(0, GRAVITY)
        self.check_keys()
        # apply friction to acceleration in x direction only
        self.acc.x += self.vel.x * FRICTION
        self.vel += self.acc
        
        on_platform = False
        
        # check platforms only if falling
        if self.vel.y > 0:
            self.jumping = False
            on_platform = self.check_for_platforms()
        
        # allow for stopping if vel is near zero in either direction
        if abs(self.vel.x) < ZERO_TOLERANCE:
            self.vel.x = 0
        if abs(self.vel.y) < ZERO_TOLERANCE:
            self.vel.y = 0
        self.pos.x += 1/2 * self.acc.x * self.game.dt ** 2 + self.vel.x * self.game.dt    
        
        self.check_for_wall_collisions()
        
        # dp = 1/2 * a * dt^2 + v*dt
        self.pos.y += 1/2 * self.acc.y * self.game.dt ** 2 + self.vel.y * self.game.dt
        
        if self.pos.y - self.previous_pos.y >= PLATFORM_TOP_THICKNESS:
            self.pos.y = self.previous_pos.y + PLATFORM_TOP_THICKNESS - 1      
        
        # use bottom middle of sprite to position
        self.rect.midbottom = self.pos
    
    def collide_point(self, sprite1, sprite2):
        right = self.pos.x + self.rect.width / 2
        left = self.pos.x - self.rect.width / 2
        top = self.pos.y - self.rect.height
        bottom = self.pos.y
        return (right >= sprite2.rect.left and
                left <= sprite2.rect.right and
                bottom >= sprite2.rect.top and
                top <= sprite2.rect.bottom)
        

    def check_for_wall_collisions(self):
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False, self.collide_point)
        if len(hits) > 0:
            for p in hits:
                # if self.pos.y > p.rect.centery and self.vel.y < 0 and self.pos.x > p.rect.left + self.rect.width / 2 and self.pos.x < p.rect.right - self.rect.width / 2:
                # if self.pos.y > p.rect.centery and self.vel.y < 0: # has issue with hitting side while jumping
                if self.pos.y > p.rect.centery and self.vel.y < 0 and self.pos.x > p.rect.left + PLATFORM_EDGE_THICKNESS and self.pos.x < p.rect.right - PLATFORM_EDGE_THICKNESS:
                    self.vel.y = 0
                    self.pos.y = p.rect.bottom + self.rect.height
                    return
                elif self.pos.x < p.rect.centerx and not self.pos.y <= p.rect.top:
                    self.vel.x = 0
                    self.acc.x = 0
                    self.pos.x = p.rect.left - self.rect.width / 2
                    return
                elif self.pos.x > p.rect.centerx and not self.pos.y <= p.rect.top:
                    self.vel.x = 0
                    self.acc.x = 0
                    self.pos.x = p.rect.right + self.rect.width / 2
                    return
            
    
    def check_for_platforms(self):
        self.pos.y += 2 # move down temporarily
        bottom_left = (self.pos.x - self.rect.width / 2, self.pos.y)
        bottom_right = (self.pos.x + self.rect.width / 2, self.pos.y)
        for platform in self.game.platforms:
            if platform.rect.collidepoint(bottom_left) or platform.rect.collidepoint(bottom_right):
                if self.pos.y <= platform.rect.top + PLATFORM_TOP_THICKNESS:
                    self.pos.y = platform.rect.top
                    self.vel.y = 0
                    self.acc.y = 0
                    return True
        self.pos.y -= 2 # move back to position
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