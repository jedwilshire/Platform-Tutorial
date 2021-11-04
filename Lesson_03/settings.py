# Screen Settings
TILE_SIZE = 32
WIDTH = TILE_SIZE * 32
HEIGHT = TILE_SIZE * 20
WIDTH_TILES = 32
HEIGHT_TILES = 20
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
PLAYER_WIDTH = TILE_SIZE
PLAYER_HEIGHT = TILE_SIZE
PLAYER_ACC = 32.0
JUMP_VEL = 350.0
TERMINAL_VEL = 6
MAX_FALL_PER_FRAME = PLATFORM_TOP_THICKNESS - PLATFORM_PLAYER_ADJUSTMENT

