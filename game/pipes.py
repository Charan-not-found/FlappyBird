"""Pipe obstacles and the manager that spawns and recycles them."""

import random

import arcade

from . import assets as A
from . import constants as C


class Pipe(arcade.Sprite):
    """One half of a pipe pair."""

    def __init__(self, texture, is_top: bool):
        super().__init__(texture, scale=C.PIPE_SCALE)
        # NOTE: do not call this `top` -- arcade.Sprite already uses `.top`
        # for the sprite's upper edge position.
        self.is_top = is_top
        # Only the bottom pipe of each pair carries the score flag, so a pair
        # counts once.
        self.scored = False

    def update(self, delta_time: float = 1 / 60, *args, **kwargs):
        self.center_x -= C.PIPE_SPEED * delta_time


class PipeManager:
    """Owns the pipe SpriteList and keeps a steady stream of pairs coming."""

    def __init__(self, game_assets):
        self.sprites = arcade.SpriteList(use_spatial_hash=False)

        self.tex_bottom = game_assets.pipe_bottom or A.solid_texture(
            C.PIPE_WIDTH, C.PIPE_HEIGHT, C.COLOR_PIPE
        )
        self.tex_top = game_assets.pipe_top or A.solid_texture(
            C.PIPE_WIDTH, C.PIPE_HEIGHT, C.COLOR_PIPE
        )

        self.pairs = []          # list of (bottom, top) tuples
        self.spawn_x = C.SCREEN_WIDTH + C.PIPE_WIDTH

        # Start with enough pairs to fill the screen and a little beyond.
        x = C.SCREEN_WIDTH + 120
        while x < C.SCREEN_WIDTH + 120 + C.PIPE_SPACING * 4:
            self._spawn(x)
            x += C.PIPE_SPACING

    # ------------------------------------------------------------------
    def _spawn(self, x):
        gap_center = random.randint(C.PIPE_MIN_CENTER, int(C.PIPE_MAX_CENTER))

        bottom = Pipe(self.tex_bottom, is_top=False)
        bottom.center_x = x
        bottom.top = gap_center - C.PIPE_GAP / 2   # arcade sets center from edge

        top = Pipe(self.tex_top, is_top=True)
        top.center_x = x
        top.bottom = gap_center + C.PIPE_GAP / 2

        self.sprites.append(bottom)
        self.sprites.append(top)
        self.pairs.append((bottom, top))

    def _recycle(self, bottom, top):
        """Move an off-screen pair back to the right with a fresh gap."""
        rightmost = max(b.center_x for b, _ in self.pairs)
        gap_center = random.randint(C.PIPE_MIN_CENTER, int(C.PIPE_MAX_CENTER))

        new_x = rightmost + C.PIPE_SPACING
        bottom.center_x = new_x
        bottom.top = gap_center - C.PIPE_GAP / 2
        bottom.scored = False

        top.center_x = new_x
        top.bottom = gap_center + C.PIPE_GAP / 2

    # ------------------------------------------------------------------
    def on_update(self, delta_time, bird):
        """Move pipes, recycle off-screen pairs, return points scored."""
        points = 0
        self.sprites.update(delta_time)

        for bottom, top in self.pairs:
            if not bottom.scored and bottom.center_x < bird.center_x:
                bottom.scored = True
                points += 1

        for bottom, top in list(self.pairs):
            if bottom.right < 0:
                self._recycle(bottom, top)

        return points

    def draw(self):
        self.sprites.draw()

    def collides_with(self, bird):
        return bool(arcade.check_for_collision_with_list(bird, self.sprites))
