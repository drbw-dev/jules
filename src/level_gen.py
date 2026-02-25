import random

class LevelGenerator:
    def __init__(self, width=31, height=31):
        # Ensure dimensions are odd for maze generation
        self.width = width if width % 2 != 0 else width + 1
        self.height = height if height % 2 != 0 else height + 1
        self.grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.player_start = (1, 1)
        self.enemy_spawns = []
        self.key_spawns = []
        self.exit_pos = None

    def generate(self):
        """
        Generates a maze using recursive backtracking.
        0 = Wall
        1 = Floor
        2 = Player Start
        3 = Enemy Spawn
        4 = Key
        5 = Exit
        """
        # Start with all walls
        self.grid = [[0 for _ in range(self.width)] for _ in range(self.height)]

        # Carve maze
        start_x, start_y = 1, 1
        self.grid[start_y][start_x] = 1
        stack = [(start_x, start_y)]

        while stack:
            x, y = stack[-1]
            neighbors = []

            # Check neighbors (jump 2 cells)
            moves = [(0, -2), (0, 2), (-2, 0), (2, 0)]
            for dx, dy in moves:
                nx, ny = x + dx, y + dy
                if 0 < nx < self.width - 1 and 0 < ny < self.height - 1:
                    if self.grid[ny][nx] == 0:
                        neighbors.append((nx, ny, dx, dy))

            if neighbors:
                nx, ny, dx, dy = random.choice(neighbors)
                # Carve path to neighbor (remove wall between)
                self.grid[y + dy // 2][x + dx // 2] = 1
                self.grid[ny][nx] = 1
                stack.append((nx, ny))
            else:
                stack.pop()

        # Place player start
        self.grid[self.player_start[1]][self.player_start[0]] = 2

        # Identify all floor tiles for placements
        floor_tiles = []
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                if self.grid[y][x] == 1:
                    floor_tiles.append((x, y))

        # Place Exit (farthest from start)
        self.exit_pos = max(floor_tiles, key=lambda p: abs(p[0]-start_x) + abs(p[1]-start_y))
        self.grid[self.exit_pos[1]][self.exit_pos[0]] = 5
        floor_tiles.remove(self.exit_pos)

        # Place 3 Keys (spread out)
        for _ in range(3):
            if not floor_tiles: break
            # Pick random far from start and other keys
            best_k = max(random.sample(floor_tiles, min(10, len(floor_tiles))),
                         key=lambda p: abs(p[0]-start_x) + abs(p[1]-start_y))
            self.grid[best_k[1]][best_k[0]] = 4
            self.key_spawns.append(best_k)
            floor_tiles.remove(best_k)

        # Place Enemies
        for _ in range(5): # Increase enemy count
            if not floor_tiles: break
            spawn = random.choice(floor_tiles)
            if abs(spawn[0]-start_x) + abs(spawn[1]-start_y) > 5: # Don't spawn on player
                self.grid[spawn[1]][spawn[0]] = 3
                self.enemy_spawns.append(spawn)
                floor_tiles.remove(spawn)

        return self.grid

    def print_grid(self):
        chars = {0: '#', 1: ' ', 2: 'P', 3: 'E', 4: 'K', 5: 'X'}
        for row in self.grid:
            print("".join(chars.get(cell, '?') for cell in row))

if __name__ == "__main__":
    gen = LevelGenerator(width=31, height=31)
    grid = gen.generate()
    gen.print_grid()
