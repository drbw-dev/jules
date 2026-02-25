from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random

# Local imports
try:
    from src import assets
    from src import level_gen
    from src import player
    from src import enemy
except ImportError:
    import assets
    import level_gen
    import player
    import enemy

app = Ursina()

# --- Asset Generation ---
print("Generating assets...")
assets.generate_texture("wall_texture", type="concrete")
assets.generate_texture("floor_texture", type="rust")
assets.generate_texture("blood_texture", type="blood")
assets.generate_sound("ambient_hum", duration=2.0, type="hum")
assets.generate_sound("player_step", duration=0.2, type="footstep")
assets.generate_sound("screech", duration=1.0, type="screech")

# --- Scene Setup ---
window.title = "Procedural Horror"
window.borderless = False
window.fullscreen = False
window.exit_button.visible = False
window.fps_counter.enabled = True

# Lighting & Atmosphere
scene.fog_color = color.rgb(10, 10, 20)
scene.fog_density = 0.1
AmbientLight(color=color.rgba(20, 20, 30, 1))

# --- Level Generation ---
print("Generating level...")
generator = level_gen.LevelGenerator(width=21, height=21)
grid = generator.generate()

wall_texture = load_texture('assets/wall_texture.png')
floor_texture = load_texture('assets/floor_texture.png')

# Instantiate Level
scale = 4
for z, row in enumerate(grid):
    for x, cell in enumerate(row):
        if cell == 0: # Wall
            Entity(model='cube', scale=(scale, scale*2, scale), position=(x*scale, scale, z*scale),
                   texture=wall_texture, collider='box', color=color.dark_gray)
        else: # Floor (everywhere not wall, or just under paths?)
             # Floor is usually everywhere
             pass

        # Floor always exists
        Entity(model='plane', scale=(scale, 1, scale), position=(x*scale, 0, z*scale),
               texture=floor_texture, collider='box', color=color.gray)

        # Ceiling
        Entity(model='plane', scale=(scale, 1, scale), position=(x*scale, scale*2, z*scale),
               texture=wall_texture, rotation_x=180, color=color.black)

# --- Spawning ---
player_spawn = generator.player_start
p = player.HorrorPlayer(position=(player_spawn[0]*scale, 2, player_spawn[1]*scale))
p.cursor.visible = False
p.gravity = 0.5

for ex, ey in generator.enemy_spawns:
    e = enemy.Monster(player=p, position=(ex*scale, 1, ey*scale))

# --- Game Logic ---
def update():
    if held_keys['escape']:
        application.quit()

    # Check for win condition (optional, maybe reach a specific point?)
    # For now, just survival.

def input(key):
    if key == 'tab': # Debug: Toggle fog
        scene.fog_density = 0.1 if scene.fog_density == 0 else 0

if __name__ == "__main__":
    app.run()
