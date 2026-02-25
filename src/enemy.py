from ursina import *
import random
import math

class Monster(Entity):
    def __init__(self, player, position=(0,0,0), **kwargs):
        super().__init__(position=position, **kwargs)

        self.player = player
        self.speed = 4
        self.attack_range = 1.5
        self.sight_range = 15

        # State
        self.state = 'idle' # idle, chase, attack
        self.idle_timer = 0
        self.idle_direction = Vec3(0, 0, 0)
        self.is_attacking = False

        # Appearance
        self.model = 'cube'
        self.color = color.red
        self.scale_y = 2
        self.collider = 'box'

        # Audio
        # Assuming asset exists, otherwise fallback?
        # Assets are generated in assets.py
        try:
            self.sound_hum = Audio('assets/ambient_hum.wav', loop=True, autoplay=False, volume=0.5)
            self.sound_screech = Audio('assets/screech.wav', loop=False, autoplay=False)
        except:
            self.sound_hum = None
            self.sound_screech = None

    def update(self):
        dist_to_player = distance(self.position, self.player.position)

        # Simple AI State Machine
        if self.state == 'idle':
            self.idle_behavior()
            # Check line of sight periodically or every frame
            if dist_to_player < self.sight_range:
                hit_info = raycast(self.position + Vec3(0, 1.5, 0), direction=(self.player.position - self.position).normalized(), distance=self.sight_range, ignore=(self,), debug=False)
                if hit_info.hit and hit_info.entity == self.player:
                    self.state = 'chase'
                    if self.sound_hum: self.sound_hum.play()

        elif self.state == 'chase':
            self.chase_behavior(dist_to_player)
            if dist_to_player > self.sight_range * 1.5: # Lose interest if too far
                self.state = 'idle'
                if self.sound_hum: self.sound_hum.stop()

        elif self.state == 'attack':
            self.attack_behavior(dist_to_player)

    def idle_behavior(self):
        self.idle_timer -= time.dt
        if self.idle_timer <= 0:
            self.idle_timer = random.uniform(2, 5)
            self.rotation_y = random.uniform(0, 360)

        # Move forward slowly
        hit_info = raycast(self.position + Vec3(0, 0.5, 0), self.forward, distance=1, ignore=(self,), debug=False)
        if not hit_info.hit:
            self.position += self.forward * self.speed * 0.5 * time.dt
        else:
            # Turn around if hit wall
            self.rotation_y += 180
            self.idle_timer = 0

    def chase_behavior(self, dist):
        self.look_at_2d(self.player.position, 'y')
        if dist > self.attack_range:
            self.position += self.forward * self.speed * time.dt
        else:
            if not self.is_attacking:
                self.state = 'attack'
                self.start_attack()

    def start_attack(self):
        self.is_attacking = True
        print("Monster attacks!")
        if self.sound_screech: self.sound_screech.play()

        # Lunge
        self.animate_position(self.position + self.forward * 2, duration=0.2, curve=curve.linear)

        # Reset state after attack animation
        invoke(self.reset_attack, delay=1.0)

    def attack_behavior(self, dist):
        # Already attacking, waiting for reset
        pass

    def reset_attack(self):
        self.is_attacking = False
        self.state = 'chase'

if __name__ == "__main__":
    pass
