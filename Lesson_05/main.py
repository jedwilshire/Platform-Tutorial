import pygame, sprites, world, os
from settings import *

class Application:
    def __init__(self):
        self.screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        # a sprite group for holding all sprites
        self.all_sprites = pygame.sprite.LayeredUpdates()
        # a sprite group for platforms
        self.platforms = pygame.sprite.Group()
        self.running = True
        self.debugging = False
        self.home_dir = os.path.dirname(__file__)
        self.load_images()
        self.load_game()
    
    def load_images(self):
        images_dir = os.path.join(self.home_dir, 'images')
        self.player_images = {'idle' : pygame.image.load(os.path.join(images_dir, PLAYER_IMAGES[0])).convert_alpha(),
                              'idle_left' : pygame.image.load(os.path.join(images_dir, PLAYER_IMAGES[1])).convert_alpha(),
                              'jump' : pygame.image.load(os.path.join(images_dir, PLAYER_IMAGES[2])).convert_alpha(),
                              'walk1' : pygame.image.load(os.path.join(images_dir, PLAYER_IMAGES[4])).convert_alpha(),
                              'walk2' : pygame.image.load(os.path.join(images_dir, PLAYER_IMAGES[5])).convert_alpha(),
                              'jump_left' : pygame.image.load(os.path.join(images_dir, PLAYER_IMAGES[3])).convert_alpha(),
                              'walk1_left' : pygame.image.load(os.path.join(images_dir, PLAYER_IMAGES[6])).convert_alpha(),
                              'walk2_left' : pygame.image.load(os.path.join(images_dir, PLAYER_IMAGES[7])).convert_alpha()}
        for img in self.player_images.keys():
            self.player_images[img] = pygame.transform.scale(self.player_images[img],(PLAYER_WIDTH, PLAYER_HEIGHT))
       
    def load_game(self):
        map_file = os.path.join(self.home_dir, 'map1.txt')
        self.map = world.World(map_file)
        self.camera = world.Camera(self.map.width, self.map.height)
        # end file read
        for y, row in enumerate(self.map.tiles):
            plat_begin = False
            plat_width = 0
            for x, tile in enumerate(row):
                if tile == '1':
                    plat_width += 1
                    plat_begin = True
                elif tile == '.' and plat_begin:
                    plat_begin = False
                    sprites.Platform(self, x - plat_width - 1, y, plat_width, 1)
                    plat_width = 0
                elif tile == 'P':
                    self.player = sprites.Player(self, x, y)
                    # a camera portal around the player
                    self.camera_portal = world.Camera_Portal(self,
                                                             self.player.rect.x,
                                                             self.player.rect.y,
                                                             CAMERA_WIDTH,
                                                             CAMERA_HEIGHT)
                                                             
            if plat_width > 0:
                sprites.Platform(self, x - plat_width - 1, y, plat_width, 1)
    def gameloop(self):
        while self.running:
            self.dt = self.clock.tick(FPS) / 1000
            self.update_events()
            
            # update sprite positions
            self.all_sprites.update()
            
            # update camera portal
            self.camera_portal.update()
            
            self.camera.update(self.camera_portal)
            self.update_screen()
    
    def update_screen(self):
        self.screen.fill(BLACK)
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        if self.debugging:
            self.draw_grid()
            self.show_statistics()
            pygame.draw.rect(self.screen, WHITE, self.camera.apply(self.camera_portal), width = 1)
        pygame.display.flip()
    
    def update_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    self.debugging = not self.debugging
                    
    def draw_grid(self):
        for x in range(0, WIDTH, TILE_SIZE):
            pygame.draw.line(self.screen, GREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILE_SIZE):
            pygame.draw.line(self.screen, GREY, (0, y), (WIDTH, y))
    
    def show_statistics(self):
        fps_str = 'FPS: = {:.2f}'.format(self.clock.get_fps())      
        acc_str = 'ACC: = <{:.2f}, {:.2f}>'.format(self.player.acc.x, self.player.acc.y)
        vel_str = 'VEL: = <{:.2f}, {:.2f}>'.format(self.player.vel.x, self.player.vel.y)
        pos_str = 'POS: = <{:.2f}, {:.2f}>'.format(self.player.pos.x, self.player.pos.y)
        self.draw_text(fps_str, 5, 10)
        self.draw_text(acc_str, 5, 30)
        self.draw_text(vel_str, 5, 50)
        self.draw_text(pos_str, 5, 70)
        
    def draw_text(self, text, x, y, font_name = None, size = 24, color = WHITE, align = 'upper-left'):
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == 'center':
            text_rect.center = (x, y)
        elif align == 'left':
            text_rect.left = x
            text_rect.centery = y
        elif align == 'upper-left':
            text_rect.left = x
            text_rect.top = y
        self.screen.blit(text_surface, text_rect)
        
    
def main():
    pygame.init()
    game = Application()
    game.gameloop()
    pygame.quit()
    
if __name__ == '__main__':
    main()