# Horror Game (Python 3.14.3 Simulation)

This is a procedural 3D horror game built using Python 3.12 (simulating Python 3.14.3 environment).
It features:
- Procedural Dungeon Generation (Maze/Cave).
- Procedural Textures (Concrete, Rust, Blood).
- Simple Enemy AI.
- Standalone EXE Build.

## Prerequisites

- **Python 3.12** or later installed on your system.
- Ensure `python` is in your system PATH.

## Setup & Running

1.  **Install Dependencies (Local)**:
    Double-click `setup.bat` to install all required libraries into the local `libs` folder. This ensures the game runs without global installations.

2.  **Run Game (Development Mode)**:
    Double-click `run.bat` to start the game directly using the local libraries.

3.  **Build Standalone EXE**:
    Double-click `build.bat` to compile the game into a single executable file (`dist/main.exe`).

## Controls

- **WASD**: Move
- **Space**: Jump
- **Shift**: Sprint
- **F**: Toggle Flashlight
- **Esc**: Pause/Exit

## Developer Notes

- **Assets**: All assets are procedurally generated at runtime. No external image/audio files needed.
- **Libs**: Dependencies are stored in `./libs` to avoid conflicts.
- **Engine**: Uses `ursina` for rendering and physics.
