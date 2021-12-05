import pygame, os, pytmx
from settings import *
class World:
    def __init__(self, filename):
        self.tmxdata = pytmx.load_pygame(filename, pixelalpha = True)
        self.width = self.tmxdata.width * self.tmxdata.tilewidth
        self.height = self.tmxdata.height * self.tmxdata.tileheight

    def render(self, surface):
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = self.tmxdata.get_tile_image_by_gid(gid)
                    if tile:
                        surface.blit(tile,
                                     (x * self.tmxdata.tilewidth, y * self.tmxdata.tileheight))
    def make_world(self):
        surface = pygame.Surface((self.width, self.height))
        self.render(surface)
        return surface

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
    
    def apply_to_rect(self, rect):
        return rect.move(self.camera_rect.topleft)