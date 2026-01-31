import arcade
from ..storage import save_score


class EndView(arcade.View):
    def __init__(self, score):
        super().__init__()
        self.score = score

    def on_show(self):
        arcade.set_background_color(arcade.color.DARK_SLATE_GRAY)

    def on_draw(self):
        self.clear()
        arcade.draw_text("Игра окончена", self.window.width / 2, self.window.height - 80,
                         arcade.color.WHITE, font_size=48, anchor_x="center")
        arcade.draw_text(f"Ваш счет: {self.score}", self.window.width / 2, self.window.height / 2,
                         arcade.color.WHITE, font_size=24, anchor_x="center")
        arcade.draw_text("Нажмите ENTER чтобы вернуться в меню", self.window.width / 2,
                         self.window.height / 2 - 40, arcade.color.WHITE, font_size=16, anchor_x="center")

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ENTER:
            save_score(("Player", self.score))
            from .start_view import StartView
            self.window.show_view(StartView())
