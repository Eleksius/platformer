import arcade


class Player(arcade.SpriteSolidColor):
    def __init__(self, x, y):
        # Use SpriteSolidColor to avoid dealing with Texture construction
        super().__init__(32, 32, arcade.color.BLUE)
        self.center_x = x
        self.center_y = y
        # movement
        self.change_x = 0
        self.change_y = 0

        # animation placeholders
        self.textures = []
        self.current_texture_index = 0
        self.time_since_last_frame = 0.0

    def update(self):
        """Update position based on simple velocity (PhysicsEngine will also adjust)."""
        # move horizontally by velocity (PhysicsEnginePlatformer primarily controls vertical physics)
        self.center_x += self.change_x

    def update_animation(self, delta_time: float = 1/60):
        """Simple placeholder animation timer."""
        self.time_since_last_frame += delta_time
        if self.time_since_last_frame > 0.1:
            self.time_since_last_frame = 0.0
            if self.textures:
                self.current_texture_index = (self.current_texture_index + 1) % len(self.textures)
                self.texture = self.textures[self.current_texture_index]
