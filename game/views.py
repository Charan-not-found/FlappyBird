"""The three screens: menu, gameplay, game over."""

import arcade

from . import assets as A
from . import constants as C
from .bird import Bird
from .ground import Ground
from .pipes import PipeManager
from .score import load_highscore, save_highscore


def draw_background(game_assets):
    if game_assets.background is not None:
        arcade.draw_texture_rect(
            game_assets.background,
            arcade.LBWH(0, 0, C.SCREEN_WIDTH, C.SCREEN_HEIGHT),
        )
    else:
        arcade.draw_lrbt_rectangle_filled(
            0, C.SCREEN_WIDTH, 0, C.SCREEN_HEIGHT, C.COLOR_SKY
        )


def centered_text(text, y, size, color=C.COLOR_TEXT):
    """Build an arcade.Text centred horizontally, with a soft shadow."""
    shadow = arcade.Text(
        text, C.SCREEN_WIDTH / 2 + 2, y - 2, C.COLOR_TEXT_SHADOW, size,
        anchor_x="center", bold=True,
    )
    main = arcade.Text(
        text, C.SCREEN_WIDTH / 2, y, color, size,
        anchor_x="center", bold=True,
    )
    return shadow, main


class BaseView(arcade.View):
    def __init__(self, game_assets):
        super().__init__()
        self.assets = game_assets


# --------------------------------------------------------------------------
class MenuView(BaseView):
    def __init__(self, game_assets):
        super().__init__(game_assets)
        self.title = centered_text("FLAPPY BIRD", C.SCREEN_HEIGHT * 0.66, 42)
        self.prompt = centered_text("Press SPACE to start", C.SCREEN_HEIGHT * 0.46, 20)
        self.hint = centered_text("SPACE / click to flap  -  ESC to quit",
                                  C.SCREEN_HEIGHT * 0.38, 13)
        self.best = centered_text(f"Best: {load_highscore()}",
                                  C.SCREEN_HEIGHT * 0.28, 16)
        self.ground = Ground(game_assets)

    def on_update(self, delta_time):
        self.ground.on_update(delta_time)

    def on_draw(self):
        self.clear()
        draw_background(self.assets)
        self.ground.draw()
        for pair in (self.title, self.prompt, self.hint, self.best):
            for text in pair:
                text.draw()

    def _start(self):
        self.window.show_view(GameView(self.assets))

    def on_key_press(self, key, modifiers):
        if key in (arcade.key.SPACE, arcade.key.UP, arcade.key.ENTER):
            self._start()
        elif key == arcade.key.ESCAPE:
            arcade.exit()

    def on_mouse_press(self, x, y, button, modifiers):
        self._start()


# --------------------------------------------------------------------------
class GameView(BaseView):
    def __init__(self, game_assets):
        super().__init__(game_assets)
        self.bird = Bird(game_assets)
        self.bird_list = arcade.SpriteList()
        self.bird_list.append(self.bird)

        self.pipes = PipeManager(game_assets)
        self.ground = Ground(game_assets)

        self.score = 0
        self.dying = False          # hit something, still falling
        self.score_text = arcade.Text(
            "0", C.SCREEN_WIDTH / 2, C.SCREEN_HEIGHT - 90,
            C.COLOR_TEXT, 44, anchor_x="center", bold=True,
        )
        self.ready = centered_text("Press SPACE to flap", C.SCREEN_HEIGHT * 0.40, 18)

    # ------------------------------------------------------------------
    def _die(self):
        if self.dying:
            return
        self.dying = True
        self.bird.kill_bird()
        self.ground.scrolling = False
        A.play(self.assets.snd_hit, volume=1.5)

    def _game_over(self):
        A.play(self.assets.snd_die, volume=0.5)
        self.window.show_view(GameOverView(self.assets, self.score))

    # ------------------------------------------------------------------
    def on_update(self, delta_time):
        self.bird.update(delta_time)
        self.bird.update_animation(delta_time)

        if not self.dying:
            self.ground.on_update(delta_time)

            if not self.bird.frozen:
                gained = self.pipes.on_update(delta_time, self.bird)
                if gained:
                    self.score += gained
                    self.score_text.text = str(self.score)
                    A.play(self.assets.snd_score, volume=0.4)

            if self.pipes.collides_with(self.bird):
                self._die()

        # Landing on the ground ends the run in both states.
        if self.ground.collides_with(self.bird):
            self.bird.bottom = self.ground.top_y
            self._die()
            self._game_over()

    def on_draw(self):
        self.clear()
        draw_background(self.assets)
        self.pipes.draw()
        self.ground.draw()
        self.bird_list.draw()
        self.score_text.draw()
        if self.bird.frozen:
            for text in self.ready:
                text.draw()

    # ------------------------------------------------------------------
    def on_key_press(self, key, modifiers):
        if key in (arcade.key.SPACE, arcade.key.UP):
            self.bird.flap()
        elif key == arcade.key.ESCAPE:
            self.window.show_view(MenuView(self.assets))

    def on_mouse_press(self, x, y, button, modifiers):
        self.bird.flap()


# --------------------------------------------------------------------------
class GameOverView(BaseView):
    def __init__(self, game_assets, score):
        super().__init__(game_assets)
        self.score = score
        self.best = load_highscore()
        self.is_new_best = score > self.best
        if self.is_new_best:
            self.best = score
            save_highscore(score)

        self.title = centered_text("GAME OVER", C.SCREEN_HEIGHT * 0.66, 40)
        self.score_line = centered_text(f"Score: {score}", C.SCREEN_HEIGHT * 0.54, 24)
        self.best_line = centered_text(
            ("NEW BEST: " if self.is_new_best else "Best: ") + str(self.best),
            C.SCREEN_HEIGHT * 0.47, 20,
        )
        self.prompt = centered_text("SPACE to play again  -  ESC for menu",
                                    C.SCREEN_HEIGHT * 0.34, 15)
        self.ground = Ground(game_assets)
        self.ground.scrolling = False

    def on_draw(self):
        self.clear()
        draw_background(self.assets)
        self.ground.draw()
        for pair in (self.title, self.score_line, self.best_line, self.prompt):
            for text in pair:
                text.draw()

    def on_key_press(self, key, modifiers):
        if key in (arcade.key.SPACE, arcade.key.ENTER):
            self.window.show_view(GameView(self.assets))
        elif key == arcade.key.ESCAPE:
            self.window.show_view(MenuView(self.assets))

    def on_mouse_press(self, x, y, button, modifiers):
        self.window.show_view(GameView(self.assets))
