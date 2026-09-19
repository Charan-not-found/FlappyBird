# Flappy Bird (Python + Arcade 3.3.3)

## Run

```bash
pip install -r requirements.txt
python main.py
```

The game runs straight away with coloured placeholder shapes and no sound.

## Controls

| Key | Action |
| --- | --- |
| `SPACE` / `UP` / click | Flap (and start the round) |
| `ESC` | Back to menu / quit from menu |

## Adding your own art and audio

1. Drop your files into `assets/images/` and `assets/sounds/`.
2. Open `game/constants.py` and fill in the **ASSET PATHS** section with the
   filenames — just the filename, not the full path:

```python
BIRD_TEXTURES = ["bird_up.png", "bird_mid.png", "bird_down.png"]
PIPE_TEXTURE = "pipe.png"          # upward-facing; flipped automatically for the top pipe
BACKGROUND_TEXTURE = "background.png"
GROUND_TEXTURE = "ground.png"

SOUND_FLAP = "wing.wav"
SOUND_SCORE = "point.wav"
SOUND_HIT = "hit.wav"
SOUND_DIE = "die.wav"
```

Any entry left as `""` keeps using the placeholder, so you can add assets one
at a time. A missing or unreadable file prints a warning and falls back rather
than crashing.

Notes on sizing:
- The background should be about 500x700 to fill the window.
- The ground tile's width determines the scroll loop; anything tiles fine.
- Pipe art taller than `PIPE_HEIGHT` is fine — only the gap position matters.

## Tuning the difficulty

Everything lives in `game/constants.py`: `GRAVITY`, `FLAP_VELOCITY`,
`PIPE_GAP`, `PIPE_SPACING`, `PIPE_SPEED`.

## Layout

```
flappy_bird/
├── main.py              entry point
├── requirements.txt
├── README.md
├── assets/
│   ├── images/          your sprites go here
│   └── sounds/          your audio goes here
└── game/
    ├── __init__.py
    ├── constants.py     all tunables + asset paths
    ├── assets.py        tolerant loaders, placeholder generator
    ├── bird.py          player physics, tilt, animation
    ├── pipes.py         obstacle spawning and recycling
    ├── ground.py        scrolling floor
    ├── score.py         high score file
    └── views.py         menu / game / game over
```
