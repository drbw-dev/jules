# Project Guidelines

This project is a procedural 3D horror game using Python 3.12 (simulating 3.14.3).

## Constraints
1.  **No External Assets**: All textures, models, and sounds must be procedurally generated at runtime. Do not add image or audio files to the repository.
2.  **Local Dependencies**: Do not rely on global pip packages. All dependencies are managed in `./libs`.
3.  **Standalone**: The game must run from `run.bat` without requiring system-wide installations (except Python itself).

## Architecture
- `src/main.py`: Entry point.
- `src/assets.py`: Procedural asset generation.
- `src/level_gen.py`: Map generation.
- `src/player.py`: Player controller.
- `src/enemy.py`: Enemy logic.

## Testing
- Since the environment is headless, use unit tests or simple Python scripts to verify logic (e.g., `python tests/test_level_gen.py`).
- Do not attempt to run `ursina` app in this environment as it requires a window. Mock `ursina` classes for testing.

## Build
- Use `build.bat` (Windows) to create the executable.
