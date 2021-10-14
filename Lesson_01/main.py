import pygame, sprites
from settings import *

class Application:
    def __init__(self):
        self.screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.all_sprites = pygame.sprite.Group()
        self.player = sprites.Player(self, WIDTH / 2, HEIGHT / 2)
        self.running = True
        self.debugging = False  
    
    def gameloop(self):
        while self.running:
            self.dt = self.clock.tick(FPS) / 1000
            self.update_events()
            self.all_sprites.update()
            self.update_screen()
    
    def update_screen(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        if self.debugging:
            self.draw_grid()
            self.show_statistics()
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