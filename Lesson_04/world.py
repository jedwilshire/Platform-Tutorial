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
    

class Camera:
    def __init__(self, map_width, map_height):
        self.camera_rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
        self.map_width = map_width
        self.map_height = map_height
        
    def update(self, target):
        x = -target.rect.x + WIDTH / 2
        y = -target.rect.y + HEIGHT / 2
        x = min(0, x)
        x = max(x, -(self.map_width - self.camera_rect.width))
        y = min(0, y)
        y = max(y, -(self.map_height - self.camera_rect.height))
        self.camera_rect.x = x
        self.camera_rect.y = y

    def apply(self, entity):
        return entity.rect.move(self.camera_rect.topleft) 