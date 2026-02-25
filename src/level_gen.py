import random

class LevelGenerator:
    def __init__(self, width=21, height=21):
        # Ensure dimensions are odd for maze generation
        self.width = width if width % 2 != 0 else width + 1
        self.height = height if height % 2 != 0 else height + 1
        self.grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.player_start = (1, 1)
        self.enemy_spawns = []

    def generate(self):
        """
        Generates a maze using recursive backtracking.
        0 = Wall
        1 = Floor
        2 = Player Start
        3 = Enemy Spawn
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

        # Place enemies (find dead ends or far corners)
        possible_spawns = []
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                if self.grid[y][x] == 1:
                    # Check distance from player
                    dist = abs(x - self.player_start[0]) + abs(y - self.player_start[1])
                    if dist > 10:
                        possible_spawns.append((x, y))

        # Pick 3 random spawns
        for _ in range(min(3, len(possible_spawns))):
            sx, sy = random.choice(possible_spawns)
            self.grid[sy][sx] = 3
            self.enemy_spawns.append((sx, sy))
            possible_spawns.remove((sx, sy))

        return self.grid

    def print_grid(self):
        chars = {0: '#', 1: ' ', 2: 'P', 3: 'E'}
        for row in self.grid:
            print("".join(chars.get(cell, '?') for cell in row))

if __name__ == "__main__":
    gen = LevelGenerator(width=21, height=21)
    grid = gen.generate()
    gen.print_grid()
