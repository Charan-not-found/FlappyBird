"""Tolerant asset loading.

Every loader returns None when the path is blank or the file is missing,
instead of raising. Callers treat None as "draw a placeholder" or
"play nothing", which is what lets the game run with an empty assets folder.
"""

import arcade

from . import constants as C


def _resolve(directory, name):
    if not name:
        return None
    path = directory / name
    return path if path.is_file() else None


def load_texture(name, flipped_vertically=False):
    """Load a texture from assets/images, or return None."""
    path = _resolve(C.IMAGES_DIR, name)
    if path is None:
        return None
    try:
        texture = arcade.load_texture(path)
    except Exception as exc:  # corrupt file, unsupported format, ...
        print(f"[assets] could not load image {path.name}: {exc}")
        return None
    if flipped_vertically:
        texture = texture.flip_vertically()
    return texture


def load_texture_list(names):
    """Load several textures; returns only the ones that loaded."""
    textures = [load_texture(n) for n in names]
    return [t for t in textures if t is not None]


def load_sound(name):
    """Load a sound from assets/sounds, or return None."""
    path = _resolve(C.SOUNDS_DIR, name)
    if path is None:
        return None
    try:
        return arcade.load_sound(path)
    except Exception as exc:
        print(f"[assets] could not load sound {path.name}: {exc}")
        return None


def play(sound, volume=3.5):
    """Play a sound if it exists; do nothing otherwise."""
    if sound is not None:
        arcade.play_sound(sound, volume=volume)


def solid_texture(width, height, color, radius=0):
    """Build a plain coloured texture in memory.

    Used as a stand-in for missing sprites so the game is playable with an
    empty assets folder. Pillow ships with arcade, so no extra dependency.
    """
    from PIL import Image, ImageDraw

    image = Image.new("RGBA", (int(width), int(height)), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    box = (0, 0, int(width) - 1, int(height) - 1)
    if radius > 0:
        draw.rounded_rectangle(box, radius=radius, fill=tuple(color) + (255,))
    else:
        draw.rectangle(box, fill=tuple(color) + (255,))
    return arcade.Texture(image)


class Assets:
    """Loaded once by the window and handed to each view."""

    def __init__(self):
        self.bird_frames = load_texture_list(C.BIRD_TEXTURES)
        self.pipe_bottom = load_texture(C.PIPE_TEXTURE)
        self.pipe_top = load_texture(C.PIPE_TEXTURE, flipped_vertically=True)
        self.background = load_texture(C.BACKGROUND_TEXTURE)
        self.ground = load_texture(C.GROUND_TEXTURE)

        self.snd_flap_1 = load_sound(C.SOUND_FLAP_1)
        self.snd_flap_2 = load_sound(C.SOUND_FLAP_2)
        self.snd_score = load_sound(C.SOUND_SCORE)
        self.snd_hit = load_sound(C.SOUND_HIT)
        self.snd_die = load_sound(C.SOUND_DIE)
