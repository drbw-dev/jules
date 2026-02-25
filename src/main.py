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
assets.generate_texture("wood_texture", type="wood")
assets.generate_texture("metal_texture", type="metal")
assets.generate_sound("ambient_hum", duration=2.0, type="hum")
assets.generate_sound("player_step", duration=0.2, type="footstep")
assets.generate_sound("screech", duration=1.0, type="screech")
assets.generate_sound("pickup", duration=0.5, type="pickup")

# --- Scene Setup ---
window.title = "Procedural Horror: The Escape"
window.borderless = False
window.fullscreen = False
window.exit_button.visible = False
window.fps_counter.enabled = True

# Atmosphere
scene.fog_color = color.rgb(5, 5, 10)
scene.fog_density = 0.15 # Thicker fog
AmbientLight(color=color.rgba(10, 10, 20, 1))

# --- Game State ---
keys_collected = 0
total_keys = 3
game_over = False

# UI
ui_keys = Text(text=f"Keys: {keys_collected}/{total_keys}", position=(-0.85, 0.45), scale=2, color=color.white)
ui_status = Text(text="", origin=(0,0), scale=3, color=color.red, enabled=False)

# --- Level Generation ---
print("Generating level...")
generator = level_gen.LevelGenerator(width=31, height=31)
grid = generator.generate()

wall_tex = load_texture('assets/wall_texture.png')
floor_tex = load_texture('assets/floor_texture.png')
wood_tex = load_texture('assets/wood_texture.png')
metal_tex = load_texture('assets/metal_texture.png')

# Instantiate Level
scale = 4
for z, row in enumerate(grid):
    for x, cell in enumerate(row):
        # Floor (Everywhere)
        Entity(model='plane', scale=(scale, 1, scale), position=(x*scale, 0, z*scale),
               texture=floor_tex, collider='box', color=color.gray)

        # Ceiling
        Entity(model='plane', scale=(scale, 1, scale), position=(x*scale, scale*2, z*scale),
               texture=wall_tex, rotation_x=180, color=color.black)

        if cell == 0: # Wall
            Entity(model='cube', scale=(scale, scale*2, scale), position=(x*scale, scale, z*scale),
                   texture=wall_tex, collider='box', color=color.dark_gray)

        elif cell == 4: # Key Spawn
            k = Entity(model='cube', scale=(0.5, 0.5, 0.5), position=(x*scale, 1, z*scale),
                   texture=metal_tex, color=color.gold, collider='box')
            k.animate_rotation_y(360, duration=2, loop=True)
            k.type = 'key'

        elif cell == 5: # Exit
            exit_gate = Entity(model='cube', scale=(scale, scale*2, scale), position=(x*scale, scale, z*scale),
                   texture=wood_tex, color=color.brown, collider='box')
            exit_gate.type = 'exit'

# Add Props (Random Pillars)
for _ in range(20):
    px = random.randint(1, 30)
    pz = random.randint(1, 30)
    if grid[pz][px] == 1: # Floor
        Entity(model='cylinder', scale=(1, scale*2, 1), position=(px*scale, scale, pz*scale),
               texture=wall_tex, collider='box', color=color.gray)

# --- Spawning ---
player_spawn = generator.player_start
p = player.HorrorPlayer(position=(player_spawn[0]*scale, 2, player_spawn[1]*scale))
p.cursor.visible = False
p.gravity = 0.5

# Enemies
monsters = []
for ex, ey in generator.enemy_spawns:
    e = enemy.Monster(player=p, position=(ex*scale, 1, ey*scale))
    monsters.append(e)

# Audio
pickup_sound = Audio('assets/pickup.wav', autoplay=False)

# --- Game Logic ---
def update():
    global keys_collected, game_over

    if held_keys['escape']:
        application.quit()

    if game_over:
        return

    # Check for interactions
    hit_info = p.intersects()
    if hit_info.hit:
        if hasattr(hit_info.entity, 'type'):
            if hit_info.entity.type == 'key':
                print("Collected Key!")
                destroy(hit_info.entity)
                keys_collected += 1
                ui_keys.text = f"Keys: {keys_collected}/{total_keys}"
                pickup_sound.play()

            elif hit_info.entity.type == 'exit':
                if keys_collected >= total_keys:
                    print("You Escaped!")
                    ui_status.text = "YOU SURVIVED"
                    ui_status.color = color.green
                    ui_status.enabled = True
                    game_over = True
                    invoke(application.quit, delay=3)
                else:
                    ui_status.text = "NEED MORE KEYS"
                    ui_status.enabled = True
                    invoke(disable_status, delay=2)

    # Check for death (Monster too close?)
    for m in monsters:
        if distance(m.position, p.position) < 1.0:
            print("You Died!")
            ui_status.text = "GAME OVER"
            ui_status.color = color.red
            ui_status.enabled = True
            p.enabled = False # Disable controls
            game_over = True
            invoke(application.quit, delay=3)

def disable_status():
    if not game_over:
        ui_status.enabled = False

def input(key):
    if key == 'tab': # Debug: Toggle fog
        scene.fog_density = 0.15 if scene.fog_density == 0 else 0

if __name__ == "__main__":
    app.run()
