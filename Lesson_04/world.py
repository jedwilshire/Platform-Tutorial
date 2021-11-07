import pygame
from settings import *
class World:
    def __init__(self, filename):
        self.tiles = []
        with open(filename, 'r') as f:
            for line in f:
                self.tiles.append(line.strip())    
        tile_width = len(self.tiles[0])
        tile_height = len(self.tiles)
        self.width = tile_width * TILE_SIZE
        self.height = tile_height * TILE_SIZE
    
class Camera_Portal:
    def __init__(self, game, x, y, width, height):
        self.game = game
        self.rect = pygame.Rect(x, y, width, height)
        
    
    def update(self):
        if self.game.player.rect.right > self.rect.right:
            self.rect.right = self.game.player.rect.right
        elif self.game.player.rect.left < self.rect.left:
            self.rect.left = self.game.player.rect.left
        if self.game.player.rect.top < self.rect.top:
            self.rect.top = self.game.player.rect.top
        elif self.game.player.rect.bottom > self.rect.bottom:
            self.rect.bottom = self.game.player.rect.bottom
        
        
class Camera:
    def __init__(self, map_width, map_height):
        self.camera_rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
        self.map_width = map_width
        self.map_height = map_height
        
    def update(self, target):
        x = -(target.rect.x + 2 * CAMERA_WIDTH / 3) + WIDTH / 2
        y = -target.rect.centery + HEIGHT / 2 
        x = min(0, x)
        x = max(x, -(self.map_width - self.camera_rect.width))
        y = min(0, y)
        y = max(y, -(self.map_height - self.camera_rect.height))
        self.camera_rect.x = x
        self.camera_rect.y = y

    def apply(self, entity):
        return entity.rect.move(self.camera_rect.topleft) 