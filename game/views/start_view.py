import arcade
from .game_view import GameView
from ..storage import load_scores


class StartView(arcade.View):
    def __init__(self):
        super().__init__()
        self.title = "Platformer Homework"
        self.background_color = arcade.color.AMAZON
        self.ui_alpha = 255
        self.best_scores = load_scores()

    def on_show(self):
        arcade.set_background_color(self.background_color)

    def on_draw(self):
        self.clear()
        arcade.draw_text(self.title, self.window.width / 2, self.window.height - 80,
                         arcade.color.WHITE, font_size=48, anchor_x="center")

        arcade.draw_text("Нажмите ENTER чтобы начать", self.window.width / 2, self.window.height / 2,
                         arcade.color.WHITE, font_size=24, anchor_x="center")

        arcade.draw_text("Лучшие результаты:", 20, self.window.height - 40,
                         arcade.color.WHITE, font_size=14)
        y = self.window.height - 60
        for score in self.best_scores[:5]:
            arcade.draw_text(f"{score[0]} - {score[1]}", 20, y, arcade.color.WHITE, 12)
            y -= 20

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ENTER:
            game_view = GameView()
            self.window.show_view(game_view)
