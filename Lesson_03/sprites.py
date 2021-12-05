import pygame
from settings import *

# platform collision function
# entity must have a self.pos and a self.previous_pos property
def platform_collide(entity, platform):
    plat_left = platform.rect.left
    plat_right = platform.rect.right
    plat_top = platform.rect.top
    
    y1 = entity.previous_pos.y
    y2 = entity.pos.y
    y2 += 1 # improve detection margin of error
    
    # find coordinates of intersection of segment representing top of platform and previos to current entity pos
    x_left = entity.pos.x - entity.rect.width / 2
    x_right = entity.pos.x + entity.rect.width / 2
    
    if (plat_left <= x_left <= plat_right or plat_left <= x_right <= plat_right) and y1 <= plat_top <= y2:
        return True
    else:
        return False


def wall_collide(entity, wall):
    if entity.vel.x > 0:
        wall_x = wall.rect.left
        left_x = entity.previous_pos.x + entity.rect.width / 2
        right_x = entity.pos.x + entity.rect.width / 2
    else:
        wall_x = wall.rect.right
        left_x = entity.pos.x - entity.rect.width / 2
        right_x = entity.previous_pos.x - entity.rect.width / 2
        
    wall_top = wall.rect.top
    wall_bottom = wall.rect.bottom
    y_bottom = entity.pos.y
    y_top = entity.pos.y - entity.rect.height
    
    if (wall_top <= y_bottom <= wall_bottom or wall_top <= y_top <= wall_bottom) and left_x <= wall_x <= right_x:
        return True
    else:
        return False
    
def floor_collide(entity, floor):    
    floor_left = floor.rect.left
    floor_right = floor.rect.right
    floor_bottom = floor.rect.bottom
    
    bottom_y = entity.previous_pos.y - entity.rect.height
    top_y = entity.pos.y - entity.rect.height
    
    x_left = entity.pos.x - entity.rect.width / 2
    x_right = entity.pos.x + entity.rect.width / 2
    
    if (floor_left <= x_left <= floor_right or floor_left <= x_right <= floor_right) and bottom_y >= floor_bottom >= top_y:
        return True
    else:
        return False    
    
def is_between(a, p, c):
    return a <= p <= c or a >= p >= c
            
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
        self.previous_pos = pygame.math.Vector2(self.pos)
        
        
        
    def update(self):
        on_platform = False
        self.acc = pygame.math.Vector2(0, GRAVITY)
        # check platforms only if falling
        if self.vel.y > 0:
            self.jumping = False
            on_platform = self.check_for_platforms()
        
        # check key presses
        self.check_keys()
        
        # apply friction to acceleration in x direction only
        self.acc.x += self.vel.x * FRICTION
        # change vel.y by acc.y
        self.vel.y += self.acc.y
        
        # if player is in the air, then horizontal acceleration is dampened
        if on_platform:
            self.vel.x += self.acc.x
        else:
            self.vel.x += 1/5 * self.acc.x

        # allow for stopping if vel is near zero in either direction
        if abs(self.vel.x) < ZERO_TOLERANCE:
            self.vel.x = 0
        if abs(self.vel.y) < ZERO_TOLERANCE:
            self.vel.y = 0
        
        # store previous pos
        self.previous_pos = pygame.math.Vector2(self.pos)
            
        # use position equation for x only    
        self.pos.x += 1/2 * self.acc.x * self.game.dt ** 2 + self.vel.x * self.game.dt    
        
        self.check_for_wall_collisions()
        
        # use position equaiton for y      dp = 1/2 * a * dt^2 + v*dt
        self.pos.y += 1/2 * self.acc.y * self.game.dt ** 2 + self.vel.y * self.game.dt
        
        if self.vel.y < 0:
            self.check_for_floor_collisions()
        # use bottom middle of sprite to position
        self.rect.midbottom = self.pos
    
    def check_for_floor_collisions(self):
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False, floor_collide)
        if len(hits) > 0:
            floor = hits[0]
            self.vel.y = 0
            self.pos.y = floor.rect.bottom + self.rect.height
    
    def check_for_wall_collisions(self):
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False, wall_collide)
        if len(hits) > 0:
            wall = hits[0]
            if self.vel.x > 0:
                self.pos.x = wall.rect.left - self.rect.width / 2
            elif self.vel.x < 0:
                self.pos.x = wall.rect.right + self.rect.width / 2
            self.vel.x = 0
            self.acc.x = 0
         
    
    def check_for_platforms(self):
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False, platform_collide)
        if len(hits) > 0:
            platform = hits[0]
            self.vel.y = 0
            self.acc.y = 0
            self.pos.y = platform.rect.top
            return True
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