import os
import random
import math
import struct
import wave

# Since dependencies might not be installed in the dev environment,
# we wrap imports to allow basic testing without crashing immediately.
try:
    from PIL import Image, ImageDraw
except ImportError:
    Image = None
    ImageDraw = None

try:
    from perlin_noise import PerlinNoise
except ImportError:
    PerlinNoise = None

ASSETS_DIR = "assets"

def ensure_assets_dir():
    if not os.path.exists(ASSETS_DIR):
        os.makedirs(ASSETS_DIR)

def generate_texture(name, width=256, height=256, type="concrete"):
    """
    Generates a texture image and saves it to assets/name.png
    """
    ensure_assets_dir()
    filepath = os.path.join(ASSETS_DIR, f"{name}.png")

    if os.path.exists(filepath):
        print(f"Texture {name} already exists.")
        return filepath

    if Image is None or PerlinNoise is None:
        print("PIL or perlin_noise not installed. Skipping texture generation.")
        # Create a dummy file for testing purposes if libraries missing
        with open(filepath, "w") as f:
            f.write("dummy texture")
        return filepath

    print(f"Generating texture: {name} ({type})...")
    img = Image.new('RGB', (width, height), color=(0, 0, 0))
    pixels = img.load()

    noise1 = PerlinNoise(octaves=10, seed=random.randint(1, 1000))
    noise2 = PerlinNoise(octaves=5, seed=random.randint(1, 1000))

    for x in range(width):
        for y in range(height):
            n = noise1([x/width, y/height]) + 0.5 * noise2([x/width, y/height])

            if type == "concrete":
                # Grey, gritty
                val = int((n + 0.5) * 100) + 50
                val = max(0, min(255, val))
                pixels[x, y] = (val, val, val)

            elif type == "rust":
                # Orange/Brown, noisy
                val = int((n + 0.5) * 150)
                r = min(255, val + 100)
                g = min(255, val + 50)
                b = min(255, val)
                pixels[x, y] = (r, g, b)

            elif type == "blood":
                # Dark Red, splattered
                val = int((n + 0.5) * 255)
                if val > 180: # Splatter threshold
                    pixels[x, y] = (180, 0, 0)
                else:
                    pixels[x, y] = (50, 50, 50) # Dark floor

            elif type == "noise":
                 val = int((n + 1) * 128)
                 pixels[x, y] = (val, val, val)

    img.save(filepath)
    print(f"Texture saved to {filepath}")
    return filepath

def generate_sound(name, duration=1.0, type="hum"):
    """
    Generates a .wav sound file using standard python libraries.
    """
    ensure_assets_dir()
    filepath = os.path.join(ASSETS_DIR, f"{name}.wav")

    if os.path.exists(filepath):
        print(f"Sound {name} already exists.")
        return filepath

    print(f"Generating sound: {name} ({type})...")

    sample_rate = 44100
    n_samples = int(sample_rate * duration)

    with wave.open(filepath, 'w') as wav_file:
        wav_file.setnchannels(1) # Mono
        wav_file.setsampwidth(2) # 2 bytes per sample (16-bit)
        wav_file.setframerate(sample_rate)

        for i in range(n_samples):
            t = i / sample_rate

            if type == "hum":
                # Low frequency sine wave
                freq = 60 + 5 * math.sin(2 * math.pi * 0.5 * t)
                value = int(32767 * 0.5 * math.sin(2 * math.pi * freq * t))

            elif type == "screech":
                # High frequency varying
                freq = 1000 + 500 * math.sin(2 * math.pi * 10 * t)
                value = int(32767 * 0.3 * math.sin(2 * math.pi * freq * t))

            elif type == "footstep":
                # Short burst of noise
                if t < 0.1:
                    value = int(random.uniform(-10000, 10000))
                else:
                    value = 0

            else:
                value = 0

            data = struct.pack('<h', value)
            wav_file.writeframesraw(data)

    print(f"Sound saved to {filepath}")
    return filepath

if __name__ == "__main__":
    # Test generation
    generate_texture("wall_texture", type="concrete")
    generate_texture("floor_texture", type="rust")
    generate_sound("ambient_hum", duration=2.0, type="hum")
    generate_sound("player_step", duration=0.2, type="footstep")
