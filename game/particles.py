import arcade


class ParticleManager:
    def __init__(self):
        self.emitters = []

    def emit_jump(self, x, y):
        # create a short-lived particle effect at x,y
        # using very simple 1-particle emitter
        particle = arcade.SpriteCircle(6, arcade.color.LIGHT_GRAY)
        particle.center_x = x
        particle.center_y = y - 16
        particle.change_y = -2
        particle.life_time = 0.5
        self.emitters.append(particle)

    def update(self, delta_time):
        for p in list(self.emitters):
            p.center_x += getattr(p, 'change_x', 0)
            p.center_y += getattr(p, 'change_y', -1)
            p.life_time -= delta_time
            if p.life_time <= 0:
                self.emitters.remove(p)

    def draw(self):
        for p in self.emitters:
            p.draw()
