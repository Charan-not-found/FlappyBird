"""Flappy Bird - entry point.

Run with:  python main.py
"""

import arcade

from game import constants as C
from game.assets import Assets
from game.views import MenuView


def main():
    window = arcade.Window(C.SCREEN_WIDTH, C.SCREEN_HEIGHT, C.SCREEN_TITLE)
    game_assets = Assets()
    window.show_view(MenuView(game_assets))
    arcade.run()


if __name__ == "__main__":
    main()
