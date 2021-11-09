# Screen Settings
TILE_SIZE = 64
WIDTH = TILE_SIZE * 16
HEIGHT = TILE_SIZE * 10

TITLE = 'Platform Tutorial'
FPS = 60
PLATFORM_LAYER = 1
PLAYER_LAYER = 2

# Physics Settings
GRAVITY = 8
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

# Platform Settings
PLATFORM_TOP_THICKNESS = 7
PLATFORM_EDGE_THICKNESS = 2
PLATFORM_PLAYER_ADJUSTMENT = 1

# Player Settings
PLAYER_WIDTH = TILE_SIZE - 2
PLAYER_HEIGHT = TILE_SIZE - 2
PLAYER_ACC = 45.0
JUMP_VEL = 385.0
TERMINAL_VEL = 6
MAX_FALL_PER_FRAME = PLATFORM_TOP_THICKNESS - PLATFORM_PLAYER_ADJUSTMENT

# Camera Portal Settings
CAMERA_WIDTH = 6 * TILE_SIZE
CAMERA_HEIGHT = 5 * TILE_SIZE

# Images
PLAYER_IMAGES = ['platformChar_idle.png', 'platformChar_idle_left.png', 'platformChar_jump.png', 'platformChar_jump_left.png', 'platformChar_walk1.png', 'platformChar_walk2.png', 'platformChar_walk1_left.png', 'platformChar_walk2_left.png']