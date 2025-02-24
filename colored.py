import pygame
import random

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)



pygame.font.init()
font_text = pygame.font.Font(None, 40)

class Colored:
    def __init__(self, screen, col_grid, generation , running ,size, show = False ):
        self.grid = col_grid
        self.rows = len(col_grid)
        self.cols = len(col_grid[0])
        self.generation = generation
        self.screen = screen
        self.cell_size = size
        self.show = show
        self.running = running
        self.mouse_held = False
        self.mouse_right = False
        self.pause = True
        self.back = False
        self.chance = 50
        self.random = False

    def randomizer(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                chance = random.random()
                if chance * 100 < self.chance:
                    self.grid[i][j] = 1

    def CountNeighbours(self, x, y):
        total = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                new_x = (x + i) % self.rows
                new_y = (y + j) % self.cols
                if self.grid[new_x][new_y] > 0:
                    total += 1
        return total

    def draw_grid(self):
        for row in range(self.rows):
            for col in range(self.cols):
                state = self.grid[row][col]

                if state == 0:
                    color = BLACK
                elif state == 1:
                    color = WHITE
                elif state <= 50:
                    color = (0, 255 - state * 5, 0)
                elif state <= 100:
                    color = (state * 2, 255 - state * 2, 0)
                else:
                    color = (255, max(0, 200 - (state - 100) * 5), max(0, 200 - (state - 100) * 5))

                pygame.draw.rect(
                    self.screen, color,
                    (col * self.cell_size, row * self.cell_size, self.cell_size - 1, self.cell_size - 1)
                )

                
    def handle_events(self):
        self.back = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.pause = not self.pause
                if event.key == pygame.K_f:
                    if not self.show:
                        self.show = True
                    else:
                        self.show = False
                if event.key == pygame.K_b:
                    self.back = True
                if event.key == pygame.K_t:
                    self.random = True
                if event.key == pygame.K_r:
                    self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
                    self.generation = 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                row, col = y // self.cell_size, x // self.cell_size

                if event.button == 1:
                    self.mouse_held = True
                    if 0 <= row < self.rows and 0 <= col < self.cols:
                        self.grid[row][col] = 1
                if event.button == 3:
                    self.mouse_right = True
                    if 0 <= row < self.rows and 0 <= col < self.cols:
                        self.grid[row][col] = 0

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.mouse_held = False
                if event.button == 3:
                    self.mouse_right = False

        if self.mouse_held or self.mouse_right:
            x, y = pygame.mouse.get_pos()
            row, col = y // self.cell_size, x // self.cell_size
            if 0 <= row < self.rows and 0 <= col < self.cols:
                self.grid[row][col] = 1 if self.mouse_held else 0

    def update_generation(self):
        next_grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        
        for i in range(self.rows):
            for j in range(self.cols):
                state = self.grid[i][j]
                count = self.CountNeighbours(i, j)

                if state == 0 and count == 3:
                    next_grid[i][j] = 1
                elif state > 0 and (count < 2 or count > 3):
                    next_grid[i][j] = 0
                else:
                    if state > 0:
                        next_grid[i][j] = min(255, state + 1)

        self.generation += 1

        if all(cell == 0 for row in next_grid for cell in row):
            self.generation = 0

        self.grid = next_grid
