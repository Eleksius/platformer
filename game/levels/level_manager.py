import arcade


class Level:
    def __init__(self):
        self.platform_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.player_start_x = 64
        self.player_start_y = 128


class LevelManager:
    def __init__(self):
        self.levels = []
        self._create_default_levels()

    def _create_default_levels(self):
        level1 = Level()
        # ground
        for x in range(0, 2000, 64):
            wall = arcade.SpriteSolidColor(64, 32, arcade.color.DARK_BROWN)
            wall.center_x = x + 32
            wall.center_y = 32
            level1.platform_list.append(wall)

        # floating platforms
        for i in range(5):
            plat = arcade.SpriteSolidColor(128, 20, arcade.color.DARK_GRAY)
            plat.center_x = 300 + i * 200
            plat.center_y = 200 + (i % 2) * 80
            level1.platform_list.append(plat)

        # coins
        for i in range(6):
            coin = arcade.SpriteSolidColor(16, 16, arcade.color.GOLD)
            coin.center_x = 200 + i * 150
            coin.center_y = 250
            level1.coin_list.append(coin)

        self.levels.append(level1)

        # Level 2
        level2 = Level()
        for x in range(0, 3000, 64):
            wall = arcade.SpriteSolidColor(64, 32, arcade.color.DARK_BROWN)
            wall.center_x = x + 32
            wall.center_y = 32
            level2.platform_list.append(wall)

        for i in range(8):
            plat = arcade.SpriteSolidColor(128, 20, arcade.color.DARK_GRAY)
            plat.center_x = 300 + i * 300
            plat.center_y = 220 + (i % 3) * 60
            level2.platform_list.append(plat)

        for i in range(10):
            coin = arcade.SpriteSolidColor(16, 16, arcade.color.GOLD)
            coin.center_x = 200 + i * 200
            coin.center_y = 300
            level2.coin_list.append(coin)

        self.levels.append(level2)

    def load_level(self, index):
        return self.levels[index]
