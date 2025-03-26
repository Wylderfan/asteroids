SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

ASTEROID_MIN_RADIUS = 20
ASTEROID_KINDS = 3
ASTEROID_SPAWN_RATE = 0.8  # seconds
ASTEROID_MAX_RADIUS = ASTEROID_MIN_RADIUS * ASTEROID_KINDS

PLAYER_RADUIUS = 20
PLAYER_SPEED = 200
PLAYER_TURN_SPEED = 300
PLAYER_SHOT_SPEED = 500
PLAYER_SHOT_COOLDOWN = 0.3
PLAYER_LIVES = 3
PLAYER_RESPAWN_TIME = 2.0  # seconds of invulnerability after respawn
PLAYER_BLINK_RATE = 0.1  # seconds between visibility toggle during invulnerability
PLAYER_MISSILE_COUNT = 5
PLAYER_ACCELERATION = 200  # acceleration rate (units/second²)
PLAYER_DECELERATION = 400  # deceleration when not accelerating (units/second²)
PLAYER_MAX_SPEED = 250     # maximum player speed
PLAYER_DRIFT_FACTOR = 0.05 # how much the ship drifts (0-1, lower = less drift)

SHOT_RADIUS = 5 

# Missile constants
MISSILE_RADIUS = 7
MISSILE_SPEED = 300
MISSILE_COOLDOWN = 0.5  # seconds

# Explosion constants
EXPLOSION_DURATION = 0.5  # seconds
EXPLOSION_PARTICLES = 12
EXPLOSION_SPEED = 120
EXPLOSION_FADE_SPEED = 2.0  # how quickly particles fade

# Scoring constants
SCORE_ASTEROID_SMALL = 100
SCORE_FONT_SIZE = 36 

# Menu constants
MENU_TITLE_SIZE = 72
MENU_OPTION_SIZE = 48
MENU_TITLE_COLOR = (255, 255, 255)
MENU_OPTION_COLOR = (200, 200, 200)
MENU_SELECTED_COLOR = (255, 255, 0)
