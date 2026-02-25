from ursina import *
import random
import math

class Monster(Entity):
    def __init__(self, player, position=(0,0,0), **kwargs):
        super().__init__(position=position, **kwargs)

        self.player = player
        self.speed = 6.0 # Faster
        self.attack_range = 2.0
        self.sight_range = 25 # Increased

        # State
        self.state = 'idle' # idle, chase, attack
        self.idle_timer = 0
        self.is_attacking = False

        # Appearance
        self.model = 'cube'
        self.color = color.red
        self.scale = (1, 2, 1)
        self.collider = 'box'

        # Audio
        try:
            self.sound_hum = Audio('assets/ambient_hum.wav', loop=True, autoplay=False, volume=0.5)
            self.sound_screech = Audio('assets/screech.wav', loop=False, autoplay=False)
        except:
            self.sound_hum = None
            self.sound_screech = None

    def update(self):
        dist_to_player = distance(self.position, self.player.position)

        # Determine State
        if self.state == 'idle':
            if dist_to_player < self.sight_range:
                # Direct line of sight check
                hit_info = raycast(self.position + Vec3(0, 1.5, 0), direction=(self.player.position - self.position).normalized(), distance=self.sight_range, ignore=(self,), debug=False)
                if hit_info.hit and hit_info.entity == self.player:
                    self.start_chase()
            else:
                self.idle_behavior()

        elif self.state == 'chase':
            if dist_to_player > self.sight_range * 1.5:
                self.state = 'idle'
                if self.sound_hum: self.sound_hum.stop()
                self.color = color.red # Reset color
            else:
                self.chase_behavior(dist_to_player)

        elif self.state == 'attack':
            # Wait for animation
            pass

    def start_chase(self):
        self.state = 'chase'
        if self.sound_hum: self.sound_hum.play()
        self.color = color.orange # Visual indicator

    def idle_behavior(self):
        self.idle_timer -= time.dt
        if self.idle_timer <= 0:
            self.idle_timer = random.uniform(2, 5)
            self.rotation_y = random.uniform(0, 360)

        # Move forward slowly
        # Simple collision check
        hit_info = raycast(self.position + Vec3(0, 0.5, 0), self.forward, distance=1.5, ignore=(self,), debug=False)
        if not hit_info.hit:
            self.position += self.forward * 2.0 * time.dt
        else:
            self.rotation_y += 180
            self.idle_timer = 0

    def chase_behavior(self, dist):
        # Look at player (smoothly?)
        self.look_at_2d(self.player.position, 'y')

        if dist > self.attack_range:
            # Move towards player
            # Try to move directly. If blocked, slide?
            # Basic ursina movement handles simple collisions if collider is set
            self.position += self.forward * self.speed * time.dt
        else:
            if not self.is_attacking:
                self.start_attack()

    def start_attack(self):
        self.state = 'attack'
        self.is_attacking = True
        print("Monster attacks!")
        self.color = color.black # Flash black
        if self.sound_screech: self.sound_screech.play()

        # Lunge
        self.animate_position(self.position + self.forward * 2, duration=0.2, curve=curve.linear)

        # Damage Player Logic would go here (e.g. self.player.take_damage())

        invoke(self.reset_attack, delay=1.0)

    def reset_attack(self):
        self.is_attacking = False
        self.state = 'chase'
        self.color = color.orange # Back to chase color

if __name__ == "__main__":
    pass
