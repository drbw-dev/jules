import os
import random
import math
import struct
import wave

# Handle imports safely for dev environment
try:
    from PIL import Image, ImageDraw, ImageFilter
except ImportError:
    Image = None
    ImageDraw = None
    ImageFilter = None

try:
    from perlin_noise import PerlinNoise
except ImportError:
    PerlinNoise = None

ASSETS_DIR = "assets"

def ensure_assets_dir():
    if not os.path.exists(ASSETS_DIR):
        os.makedirs(ASSETS_DIR)

def generate_texture(name, width=512, height=512, type="concrete"):
    """
    Generates a seamless texture image and saves it to assets/name.png.
    """
    ensure_assets_dir()
    filepath = os.path.join(ASSETS_DIR, f"{name}.png")

    if os.path.exists(filepath):
        print(f"Texture {name} already exists.")
        return filepath

    if Image is None or PerlinNoise is None:
        print("PIL or perlin_noise not installed. Skipping texture generation.")
        with open(filepath, "w") as f:
            f.write("dummy texture")
        return filepath

    print(f"Generating texture: {name} ({type})...")
    img = Image.new('RGB', (width, height), color=(0, 0, 0))
    pixels = img.load()

    # Create seamless noise by blending edges or using tiling logic
    # Here we simulate seamless by blending multiple octaves
    noise1 = PerlinNoise(octaves=12, seed=random.randint(1, 1000))
    noise2 = PerlinNoise(octaves=6, seed=random.randint(1, 1000))
    noise3 = PerlinNoise(octaves=3, seed=random.randint(1, 1000)) # Base

    for x in range(width):
        for y in range(height):
            # Coordinates normalized
            u = x / width
            v = y / height

            # Simple noise composition
            n = noise1([u, v]) * 0.5 + noise2([u, v]) * 0.3 + noise3([u, v]) * 0.2

            # Create variations based on type
            if type == "concrete":
                # Grey, gritty, high contrast
                val = int((n + 0.5) * 120) + 40
                # Add some random grit
                if random.random() < 0.05:
                    val -= 20
                val = max(0, min(255, val))
                pixels[x, y] = (val, val, val)

            elif type == "rust":
                # Orange/Brown, very noisy
                val = int((n + 0.6) * 150)
                r = min(255, val + 80)
                g = min(255, val + 30)
                b = min(255, val - 20)
                pixels[x, y] = (max(0, r), max(0, g), max(0, b))

            elif type == "blood":
                # Dark Red patches
                val = int((n + 0.5) * 255)
                # Threshold for blood
                if val > 160:
                    # Bloody area
                    pixels[x, y] = (random.randint(100, 180), 0, 0)
                else:
                    # Dark floor
                    base = int(val * 0.2) + 20
                    pixels[x, y] = (base, base, base)

            elif type == "wood":
                # Vertical streaks
                # Use sine wave for grain + noise
                grain = math.sin(x * 0.1 + n * 10) # Warp lines
                val = int((grain + 1) * 60) + 40
                r = val + 40
                g = val + 20
                b = val
                pixels[x, y] = (min(255, r), min(255, g), min(255, b))

            elif type == "metal":
                # Shiny grey/blueish
                val = int((n + 0.5) * 180) + 20
                pixels[x, y] = (val, val, val + 20)

    # Post-process for seamlessness (simple wrap blending)
    # This is a naive approach: crop center and blend edges?
    # Better: generate larger and crop, or rely on engine tiling.
    # For now, let's just make sure it tiles reasonably well by softening edges?
    # Actually, Perlin noise isn't seamless by default.
    # To make it seamless, we can blend the edges: left with right, top with bottom.

    # Simple edge blending (Cross-fading opposite edges)
    edge_size = 32
    for x in range(edge_size):
        for y in range(height):
            # Blend Left edge with Right edge
            factor = x / edge_size
            p1 = pixels[x, y]
            p2 = pixels[width - 1 - (edge_size - 1 - x), y]
            # Linear interpolate
            r = int(p1[0] * factor + p2[0] * (1 - factor))
            g = int(p1[1] * factor + p2[1] * (1 - factor))
            b = int(p1[2] * factor + p2[2] * (1 - factor))
            pixels[x, y] = (r, g, b)
            pixels[width - 1 - (edge_size - 1 - x), y] = (r, g, b)

    for y in range(edge_size):
        for x in range(width):
            # Blend Top edge with Bottom edge
            factor = y / edge_size
            p1 = pixels[x, y]
            p2 = pixels[x, height - 1 - (edge_size - 1 - y)]
            r = int(p1[0] * factor + p2[0] * (1 - factor))
            g = int(p1[1] * factor + p2[1] * (1 - factor))
            b = int(p1[2] * factor + p2[2] * (1 - factor))
            pixels[x, y] = (r, g, b)
            pixels[x, height - 1 - (edge_size - 1 - y)] = (r, g, b)

    img.save(filepath)
    print(f"Texture saved to {filepath}")
    return filepath

def generate_sound(name, duration=1.0, type="hum"):
    """
    Generates a .wav sound file.
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
        wav_file.setsampwidth(2) # 16-bit
        wav_file.setframerate(sample_rate)

        for i in range(n_samples):
            t = i / sample_rate

            if type == "hum":
                # Low frequency varying sine
                freq = 50 + 10 * math.sin(2 * math.pi * 0.2 * t)
                # Add some noise
                noise = random.uniform(-0.1, 0.1)
                value = int(32767 * 0.4 * (math.sin(2 * math.pi * freq * t) + noise))

            elif type == "screech":
                # FM Synthesis for eerie sound
                modulator_freq = 5.0
                modulator_amp = 500.0
                carrier_freq = 800.0

                mod = modulator_amp * math.sin(2 * math.pi * modulator_freq * t)
                value = int(32767 * 0.3 * math.sin(2 * math.pi * (carrier_freq + mod) * t))

            elif type == "footstep":
                # Short burst of white noise with envelope
                if t < 0.05:
                    envelope = 1.0 - (t / 0.05)
                    value = int(random.uniform(-20000, 20000) * envelope)
                else:
                    value = 0

            elif type == "pickup":
                # High pitched chime
                freq = 1000 + 2000 * t # Slide up
                envelope = 1.0 - t/duration
                value = int(32767 * 0.5 * math.sin(2 * math.pi * freq * t) * envelope)

            else:
                value = 0

            # Clamp value
            value = max(-32768, min(32767, value))
            data = struct.pack('<h', value)
            wav_file.writeframesraw(data)

    print(f"Sound saved to {filepath}")
    return filepath

if __name__ == "__main__":
    generate_texture("wall_texture", type="concrete")
    generate_texture("floor_texture", type="rust")
    generate_texture("wood_texture", type="wood")
    generate_sound("pickup", duration=0.5, type="pickup")
