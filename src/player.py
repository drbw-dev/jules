from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random

class HorrorPlayer(FirstPersonController):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cursor.visible = False

        # Stats
        self.max_stamina = 100
        self.stamina = self.max_stamina
        self.stamina_regen = 10
        self.stamina_drain = 20
        self.is_sprinting = False

        # Mechanics
        self.flashlight = None
        self.flashlight_on = True

        # Head Bob
        self.bob_speed = 8
        self.bob_amount = 0.05
        self.default_y = self.camera_pivot.y
        self.bob_timer = 0

        # Audio
        self.step_sound = None
        self.step_timer = 0
        self.step_interval = 0.5

        # Initialize Flashlight
        # We attach it to the camera pivot so it follows the view
        self.flashlight = SpotLight(parent=self.camera_pivot, position=(0, 0, 0.5), rotation=(0, 0, 0))
        self.flashlight.color = color.rgba(255, 255, 200, 1) # Warm light
        self.flashlight.shadows = True
        self.flashlight.range = 15
        self.flashlight.angle = 45

        # Setup audio
        try:
            self.step_sound = Audio('assets/player_step.wav', loop=False, autoplay=False)
        except Exception as e:
            print(f"Audio failed to load: {e}")

    def update(self):
        super().update()

        # Movement & Stamina
        if held_keys['left shift'] and self.stamina > 0 and (held_keys['w'] or held_keys['a'] or held_keys['s'] or held_keys['d']):
            self.speed = 8
            self.is_sprinting = True
            self.stamina -= self.stamina_drain * time.dt
        else:
            self.speed = 5
            self.is_sprinting = False
            self.stamina += self.stamina_regen * time.dt

        self.stamina = clamp(self.stamina, 0, self.max_stamina)

        # Flashlight Toggle
        if held_keys['f']: # Simple toggle check, improved in input()
            pass

        # Head Bob & Footsteps
        if (held_keys['w'] or held_keys['a'] or held_keys['s'] or held_keys['d']) and self.grounded:
            self.bob_timer += time.dt * self.bob_speed * (1.5 if self.is_sprinting else 1)
            self.camera_pivot.y = self.default_y + math.sin(self.bob_timer) * self.bob_amount

            # Footstep Sound
            if self.step_sound:
                current_interval = self.step_interval / (1.5 if self.is_sprinting else 1)
                self.step_timer += time.dt
                if self.step_timer > current_interval:
                    self.step_sound.pitch = random.uniform(0.9, 1.1)
                    self.step_sound.play()
                    self.step_timer = 0
        else:
            # Return to default height smoothly
            self.camera_pivot.y = self.default_y # lerp(self.camera_pivot.y, self.default_y, time.dt * 5)
            self.bob_timer = 0

    def input(self, key):
        super().input(key)
        if key == 'f':
            self.flashlight_on = not self.flashlight_on
            if self.flashlight:
                self.flashlight.enabled = self.flashlight_on
                # Play click sound (optional)
