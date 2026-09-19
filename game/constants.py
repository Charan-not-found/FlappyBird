"""All tunable values and asset paths live here.

Fill in the ASSET PATHS section with your own files. Any path left as an
empty string is skipped and the game falls back to simple coloured shapes
(and silence), so the game runs fine before you have art.
"""

from pathlib import Path

# --------------------------------------------------------------------------
# Window
# --------------------------------------------------------------------------
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 700
SCREEN_TITLE = "Flappy Bird"

# --------------------------------------------------------------------------
# Physics
# --------------------------------------------------------------------------
GRAVITY = -1800.0          # pixels / second^2 (negative = downward)
FLAP_VELOCITY = 520.0      # instant upward velocity on a flap
MAX_FALL_SPEED = -900.0    # terminal velocity, keeps collisions sane
UP_TILT = -40.0            # degrees nose-up when rising
DOWN_TILT = 55.0           # degrees nose-down when falling
TILT_RATE = 240.0          # degrees / second the bird rotates toward target

# --------------------------------------------------------------------------
# Bird
# --------------------------------------------------------------------------
BIRD_START_X = SCREEN_WIDTH * 0.30
BIRD_START_Y = SCREEN_HEIGHT * 0.60
BIRD_SCALE = 1.3
BIRD_WIDTH = 65           # used for the fallback rectangle
BIRD_HEIGHT = 65
BIRD_ANIM_SPEED = 0.09     # seconds per frame of the flap animation

# --------------------------------------------------------------------------
# Pipes
# --------------------------------------------------------------------------
PIPE_SCALE = 1.0
PIPE_WIDTH = 78            # used for the fallback rectangle
PIPE_HEIGHT = 500
PIPE_GAP = 190             # vertical opening the bird flies through
PIPE_SPACING = 240         # horizontal distance between pipe pairs
PIPE_SPEED = 180.0         # pixels / second the world scrolls left
PIPE_MIN_CENTER = 200      # lowest the gap centre may sit
PIPE_MAX_CENTER = SCREEN_HEIGHT - 150

# --------------------------------------------------------------------------
# Ground
# --------------------------------------------------------------------------
GROUND_HEIGHT = 1
GROUND_SPEED = PIPE_SPEED

# --------------------------------------------------------------------------
# Colours used when an asset path is blank
# --------------------------------------------------------------------------
COLOR_SKY = (112, 197, 206)
COLOR_GROUND = (222, 216, 149)
COLOR_GROUND_EDGE = (115, 191, 44)
COLOR_BIRD = (255, 214, 66)
COLOR_PIPE = (86, 190, 60)
COLOR_TEXT = (255, 255, 255)
COLOR_TEXT_SHADOW = (40, 40, 40)

# --------------------------------------------------------------------------
# ASSET PATHS  -->  fill these in
# --------------------------------------------------------------------------
ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"
IMAGES_DIR = ASSETS_DIR / "images"
SOUNDS_DIR = ASSETS_DIR / "sounds"

# Images. Give a filename relative to assets/images, e.g. "bird_1.png"
MODIFIER = ""
#MODIFIER = "special/"

"""
You can add custom files for the flappy bird frames
Try some of your friends' faces (with their consent ofcourse)
"""

BIRD_TEXTURES = [
    MODIFIER + "fap_1.png",
    MODIFIER + "fap_2.png",
    MODIFIER + "fap_3.png",
    MODIFIER + "fap_4.png"
    ]  # 4 frames of the flap cycle
PIPE_TEXTURE = "pipe.png"     # a single upward-facing pipe; flipped for the top
BACKGROUND_TEXTURE = "bg.jpg"
GROUND_TEXTURE = ""

# Sounds. Filename relative to assets/sounds, e.g. "wing.wav"
SOUND_FLAP_1 = "chacha_1.wav"
SOUND_FLAP_2 = "chacha_2.wav"
SOUND_SCORE = ""
SOUND_HIT = "death.wav"
SOUND_DIE = ""

# --------------------------------------------------------------------------
# Save file for the high score
# --------------------------------------------------------------------------
HIGHSCORE_FILE = Path(__file__).resolve().parent.parent / "highscore.txt"
