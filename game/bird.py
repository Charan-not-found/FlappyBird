"""The player-controlled bird."""

import arcade
import random
from . import assets as A
from . import constants as C


class Bird(arcade.Sprite):
    def __init__(self, game_assets):
        self.frames = game_assets.bird_frames
        if self.frames:
            first = self.frames[0]
        else:
            first = A.solid_texture(C.BIRD_WIDTH, C.BIRD_HEIGHT, C.COLOR_BIRD, radius=8)
            self.frames = [first]

        super().__init__(first, scale=C.BIRD_SCALE)

        self.center_x = C.BIRD_START_X
        self.center_y = C.BIRD_START_Y

        self.velocity_y = 0.0
        self.frame_index = 0
        self.frame_timer = 0.0
        self.alive = True
        self.frozen = True          # no gravity until the first flap
        self.snd_flap_1 = game_assets.snd_flap_1
        self.snd_flap_2 = game_assets.snd_flap_2

        self.width = C.BIRD_WIDTH
        self.height = C.BIRD_HEIGHT


    # ------------------------------------------------------------------
    def flap(self):
        if not self.alive:
            return
        self.frozen = False
        self.velocity_y = C.FLAP_VELOCITY
        A.play(self.snd_flap_1 if random.random() > 0.5 else self.snd_flap_2 , volume=0.25)

    def kill_bird(self):
        """Stop input but keep falling, like the original game."""
        self.alive = False

    # ------------------------------------------------------------------
    def update_animation(self, delta_time: float = 1 / 60, *args, **kwargs):
        if len(self.frames) < 2:
            return
        # Stop flapping the wings once the bird is diving to its death.
        if not self.alive:
            return
        self.frame_timer += delta_time
        if self.frame_timer >= C.BIRD_ANIM_SPEED:
            self.frame_timer = 0.0
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.texture = self.frames[self.frame_index]

    def _update_tilt(self, delta_time):
        target = C.UP_TILT if self.velocity_y < 0 else C.DOWN_TILT
        dt = C.TILT_RATE * delta_time

        if target > 0:
            self.angle -= dt
        else:
            self.angle += dt

        self.angle = max(min(self.angle,C.DOWN_TILT),C.UP_TILT)


    def update(self, delta_time: float = 1 / 60, *args, **kwargs):
        # NOTE: arcade 3.x removed Sprite.on_update -- update() is the hook now
        # and it receives delta_time.
        if self.frozen:
            return

        self.velocity_y += C.GRAVITY * delta_time
        self.velocity_y = max(self.velocity_y, C.MAX_FALL_SPEED)
        self.center_y += self.velocity_y * delta_time

        # Never let the bird leave the top of the screen.
        ceiling = C.SCREEN_HEIGHT - self.height / 2
        if self.center_y > ceiling:
            self.center_y = ceiling
            self.velocity_y = 0.0

        self._update_tilt(delta_time)
