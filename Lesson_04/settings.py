# Screen Settings
TILE_SIZE = 64
WIDTH = TILE_SIZE * 16
HEIGHT = TILE_SIZE * 10

TITLE = 'Platform Tutorial'
FPS = 60
PLATFORM_LAYER = 1
PLAYER_LAYER = 2

# Physics Settings
GRAVITY = 20
FRICTION = -0.2 # A friction force
ZERO_TOLERANCE = 0.2 # A value less than this is considered 0.0

# Color Constants
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
GREY = (20, 20, 20)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
WHITE = (255, 255, 255)

# Player Settings
PLAYER_WIDTH = TILE_SIZE - 2
PLAYER_HEIGHT = TILE_SIZE - 2
PLAYER_ACC = 45.0
JUMP_VEL = 600.0

# Camera Portal Settings
CAMERA_WIDTH = 6 * TILE_SIZE
CAMERA_HEIGHT = 5 * TILE_SIZE