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
        self.worlds_dir = os.path.join(self.home_dir, 'worlds')
        self.world_file = os.path.join(self.worlds_dir, 'world_01.tmx')
        self.world_obj = world.World(self.world_file)
        self.world_image = self.world_obj.make_world()
        self.world_rect = self.world_image.get_rect()
        for item in self.world_obj.tmxdata.objects:
            if item.name == 'platform':
                sprites.Platform(self, item.x, item.y, item.width, item.height)
            elif item.name == 'player':
                self.player = sprites.Player(self, item.x, item.y)
                    # a camera portal around the player
                self.camera_portal = world.Camera_Portal(self,
                                                         self.player.rect.x,
                                                         self.player.rect.y,
                                                         CAMERA_WIDTH,
                                                         CAMERA_HEIGHT)
        
        self.camera = world.Camera(self.world_obj.width, self.world_obj.height)

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
        self.screen.blit(self.world_image, self.camera.apply_to_rect(self.world_rect))
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        if self.debugging:
            self.draw_platform_outlines()
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
    
    def draw_platform_outlines(self):
        for plat in self.platforms:
            pygame.draw.rect(self.screen, WHITE, self.camera.apply(plat), width = 1)
            
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