import arcade
from game.entities.player import Player
from game.levels.level_manager import LevelManager
from game.particles import ParticleManager
from game.views.end_view import EndView
from game.audio import ensure_sounds


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        ensure_sounds()
        self.jump_sound = arcade.load_sound("assets/audio/jump.wav")
        self.coin_sound = arcade.load_sound("assets/audio/coin.wav")
        self.hit_sound = arcade.load_sound("assets/audio/hit.wav")

        self.level_index = 0
        self.levels = LevelManager()
        self.current_level = self.levels.load_level(self.level_index)
        self.player = Player(self.current_level.player_start_x, self.current_level.player_start_y)

        # Sprite lists
        self.wall_list = self.current_level.platform_list
        self.enemy_list = self.current_level.enemy_list
        self.coin_list = self.current_level.coin_list

        # Physics
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player, self.wall_list, gravity_constant=1.0)

        # Camera offsets
        self.camera_x = 0
        self.camera_y = 0

        self.particle_manager = ParticleManager()

        # Game state
        self.game_over = False

        self.score = 0

    def on_show(self):
        arcade.set_background_color(arcade.color.SKY_BLUE)

    def on_draw(self):
        self.clear()

        # Camera offsets
        cam_x = self.camera_x
        cam_y = self.camera_y

        # helper to shift and draw a sprite list
        def shift_and_draw(sprite_list):
            shifted = []
            for s in sprite_list:
                old_x, old_y = s.center_x, s.center_y
                s.center_x -= cam_x
                s.center_y -= cam_y
                shifted.append((s, old_x, old_y))
            try:
                sprite_list.draw()
            finally:
                for s, ox, oy in shifted:
                    s.center_x = ox
                    s.center_y = oy

        # Draw sprite lists with camera offset
        shift_and_draw(self.wall_list)
        shift_and_draw(self.coin_list)
        shift_and_draw(self.enemy_list)

        # draw player by temporarily placing it into a SpriteList and drawing that (safer across arcade versions)
        old_px, old_py = self.player.center_x, self.player.center_y
        self.player.center_x -= cam_x
        self.player.center_y -= cam_y
        try:
            temp_list = arcade.SpriteList()
            temp_list.append(self.player)
            try:
                temp_list.draw()
            finally:
                # clear temp_list to avoid modifying original lists
                temp_list.clear()
        finally:
            self.player.center_x, self.player.center_y = old_px, old_py

        # draw particles (they are simple Sprites stored in emitters list)
        for p in getattr(self.particle_manager, 'emitters', []):
            old_x, old_y = getattr(p, 'center_x', 0), getattr(p, 'center_y', 0)
            try:
                arcade.draw_circle_filled(old_x - cam_x, old_y - cam_y, 6, arcade.color.LIGHT_GRAY)
            except Exception:
                pass

        # HUD: draw in screen coordinates
        arcade.draw_text(f"Score: {self.score}", 10, self.window.height - 20, arcade.color.WHITE, 16)

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.LEFT:
            self.player.change_x = -4
        elif symbol == arcade.key.RIGHT:
            self.player.change_x = 4
        elif symbol == arcade.key.SPACE:
            if self.physics_engine.can_jump():
                self.player.change_y = 25  # jump impulse
                # particle effect
                self.particle_manager.emit_jump(self.player.center_x, self.player.center_y)
                arcade.play_sound(self.jump_sound)

    def on_key_release(self, symbol, modifiers):
        if symbol == arcade.key.LEFT or symbol == arcade.key.RIGHT:
            self.player.change_x = 0

    def on_update(self, delta_time):
        # Don't update game logic after game over
        if self.game_over:
            return

        self.physics_engine.update()
        self.player.update_animation(delta_time)
        self.particle_manager.update(delta_time)

        # If player has fallen far below the level, treat it as death
        # Threshold: 200 pixels below the lowest platform or a hard limit.
        try:
            lowest_platform_y = min([p.center_y for p in self.wall_list]) if len(self.wall_list) else 0
        except Exception:
            lowest_platform_y = 0

        fall_threshold = lowest_platform_y - 200
        if self.player.center_y < fall_threshold or self.player.center_y < -1000:
            # prevent multiple triggers
            self.game_over = True
            try:
                arcade.play_sound(self.hit_sound)
            except Exception:
                pass
            end_view = EndView(self.score)
            self.window.show_view(end_view)
            return

        # coin collection
        coins_hit = arcade.check_for_collision_with_list(self.player, self.coin_list)
        for coin in coins_hit:
            coin.remove_from_sprite_lists()
            self.score += 10
            arcade.play_sound(self.coin_sound)

        # enemy collision
        enemies_hit = arcade.check_for_collision_with_list(self.player, self.enemy_list)
        if enemies_hit:
            arcade.play_sound(self.hit_sound)
            # Game over for simplicity
            end_view = EndView(self.score)
            self.window.show_view(end_view)

        # Level finish condition
        if len(self.coin_list) == 0:
            # advance level
            self.level_index += 1
            if self.level_index >= len(self.levels.levels):
                end_view = EndView(self.score)
                self.window.show_view(end_view)
            else:
                self.current_level = self.levels.load_level(self.level_index)
                self.wall_list = self.current_level.platform_list
                self.enemy_list = self.current_level.enemy_list
                self.coin_list = self.current_level.coin_list
                self.player.center_x = self.current_level.player_start_x
                self.player.center_y = self.current_level.player_start_y
                self.physics_engine = arcade.PhysicsEnginePlatformer(self.player, self.wall_list, gravity_constant=1.0)

        # camera follow
        self.center_camera_to_player()

    def center_camera_to_player(self):
        # simple immediate camera follow
        self.camera_x = int(self.player.center_x - (self.window.width / 2))
        self.camera_y = int(self.player.center_y - (self.window.height / 2))
