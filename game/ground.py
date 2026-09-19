"""The scrolling ground strip along the bottom of the screen."""

import arcade

from . import assets as A
from . import constants as C


class Ground:
    """Two tiles side by side, looped to give an endless scroll."""

    def __init__(self, game_assets):
        texture = game_assets.ground
        if texture is None:
            texture = A.solid_texture(
                C.SCREEN_WIDTH, C.GROUND_HEIGHT, C.COLOR_GROUND
            )

        self.sprites = arcade.SpriteList()
        self.tile_width = texture.width

        # Enough tiles to cover the screen plus one spare for the wrap-around.
        count = int(C.SCREEN_WIDTH / self.tile_width) + 2
        for i in range(count):
            sprite = arcade.Sprite(texture)
            sprite.left = i * self.tile_width
            sprite.bottom = 0
            self.sprites.append(sprite)

        self.top_y = C.GROUND_HEIGHT
        self.scrolling = True

    def on_update(self, delta_time):
        if not self.scrolling:
            return
        for sprite in self.sprites:
            sprite.center_x -= C.GROUND_SPEED * delta_time
            if sprite.right <= 0:
                sprite.left += self.tile_width * len(self.sprites)

    def draw(self):
        self.sprites.draw()
        # A thin lip on top reads well when no texture is supplied.
        arcade.draw_lrbt_rectangle_filled(
            0, C.SCREEN_WIDTH, self.top_y - 6, self.top_y, C.COLOR_GROUND_EDGE
        )

    def collides_with(self, bird):
        return bird.bottom <= self.top_y
