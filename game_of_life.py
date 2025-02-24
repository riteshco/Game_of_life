import pygame
from colored import Colored
import random

# Constants
WIN_HEIGHT = 800
WIN_WIDTH = 1200
CELL_SIZE = 5
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BUTTON_COLOR = (100, 50, 80)
RED = (180 , 0 , 0)
GREEN = (0,180,0)
COLOR = (255 , 20 , 200)

BG_IMAGE = "Background.jpg"

# Initialize fonts
font_path_1 = "Fonts/joystix monospace.otf" 
font_path_2 = "Fonts/ka1.ttf" 
font_path_3 = "Fonts/Astron Boy Video.otf"

pygame.font.init()
font_text = pygame.font.Font(font_path_1 , 20)
font_title = pygame.font.Font(font_path_2, 80)
font_button = pygame.font.Font(font_path_3, 30)

button_x, button_y = WIN_WIDTH // 2 - 100, WIN_HEIGHT // 2 + 50
button_width, button_height = 200, 70

def CountNeighbours(grid, rows, cols, x, y):
    total = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            new_x = (x + i) % rows
            new_y = (y + j) % cols
            total += grid[new_x][new_y]
    return total

class GridGame:
    def __init__(self):
        pygame.init()
        self.width = WIN_WIDTH
        self.height = WIN_HEIGHT
        self.cell_size = CELL_SIZE
        self.cols = WIN_WIDTH // self.cell_size
        self.rows = WIN_HEIGHT // self.cell_size
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Game of Life")

        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.col_grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

        self.pause = True
        self.mouse_held = False
        self.mouse_right = False
        self.show = False
        self.random = False

        self.generation = 0

        self.running = True
        self.chance = 50

        #Colored game
        self.Col_Game = Colored(self.screen ,self.col_grid , 0 , self.running , CELL_SIZE)


        self.loading_screen = 1
        self.fps = FPS
        self.clock = pygame.time.Clock()

    def draw_grid(self):
        for row in range(self.rows):
            for col in range(self.cols):
                color = BLACK if self.grid[row][col] == 0 else WHITE
                pygame.draw.rect(
                    self.screen, color, 
                    (col * self.cell_size, row * self.cell_size, self.cell_size - 1, self.cell_size - 1)
                )

    def randomizer(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                chance = random.random()
                if chance * 100 <= self.chance:
                    self.grid[i][j] = 1

    def draw_pixelated_button(self, x, y, width, height, color):
        rects = [
            (x, y, width, height),
            (x + 5, y + 5, width - 10, height - 10),
            (x + 15, y + 15, width - 30, height - 30),
        ]
        for rect in rects:
            pygame.draw.rect(self.screen, color, rect)

    def draw_loading_screen(self):
        self.screen.fill(BLACK)


        background = pygame.image.load(BG_IMAGE)
        background = pygame.transform.scale(background, (WIN_WIDTH, WIN_HEIGHT))

        self.screen.blit(background, (0, 0))  # Draw background


        title_text = font_title.render("Game of Life", True, WHITE)
        self.screen.blit(title_text, (WIN_WIDTH // 2 - title_text.get_width() // 2, 150))

        # Draw pixelated Play Game button
        self.draw_pixelated_button(button_x, button_y, button_width, button_height, BUTTON_COLOR)

        # Draw Play Game text
        play_text = font_button.render("Play Game", True, WHITE)
        self.screen.blit(play_text, (button_x + button_width // 2 - play_text.get_width() // 2,
                                     button_y + button_height // 2 - play_text.get_height() // 2))
        
        #Colored Game button
        self.draw_pixelated_button(button_x - 35, button_y+100, button_width + 70, button_height, BUTTON_COLOR)
        play_col_text = font_button.render("Play Colored Game", True, WHITE)
        self.screen.blit(play_col_text, (button_x + button_width // 2 - play_text.get_width() // 2 - 55,
                                     button_y + button_height // 2 - play_text.get_height() // 2 + 100))
        
        #Controls button
        self.draw_pixelated_button(button_x, button_y + 200, button_width, button_height, BUTTON_COLOR)
        control_button_text = font_button.render("Controls", True, WHITE)
        self.screen.blit(control_button_text, (button_x + button_width // 2 - play_text.get_width() // 2 + 10,
                                     button_y + button_height // 2 - play_text.get_height() // 2 + 200))


        


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.pause = not self.pause
                if event.key == pygame.K_f:
                    if not self.show:
                        self.show = True
                    else:
                        self.show = False
                if event.key == pygame.K_t:
                    self.random = True
                if event.key == pygame.K_b:
                    self.loading_screen = 1
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
                count = CountNeighbours(self.grid, self.rows, self.cols, i, j)

                if state == 0 and count == 3:
                    next_grid[i][j] = 1
                elif state == 1 and (count < 2 or count > 3):
                    next_grid[i][j] = 0
                else:
                    next_grid[i][j] = state

        self.generation += 1
        if self.grid == [[0 for _ in range(self.cols)] for __ in range(self.rows)]:
            self.generation = 0

        self.grid = [row[:] for row in next_grid]

    def run(self):
        """Main game loop."""
        while self.running:
            self.clock.tick(self.fps)

            if self.loading_screen == 1:
                self.draw_loading_screen()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        mx, my = pygame.mouse.get_pos()
                        if button_x <= mx <= button_x + button_width and button_y <= my <= button_y + button_height:
                            self.loading_screen = 0
                        elif button_x - 35 <= mx <= button_x + button_width + 70 and button_y + 100 <= my <= button_y + 100 + button_height:
                            self.loading_screen = 2
                        elif button_x <= mx <= button_x + button_width and button_y + 200 <= my <= button_y + 200 + button_height:
                            self.loading_screen = 3
                pygame.display.flip()

            elif self.loading_screen == 0:
                self.cols = WIN_WIDTH // self.cell_size
                self.rows = WIN_HEIGHT // self.cell_size


                self.handle_events()
                self.screen.fill(BLACK)
                if self.random:
                    self.randomizer()
                    self.random = False
                self.draw_grid()

                if self.show:
                    title_text = font_text.render(f"Generation : {self.generation}", True, COLOR)
                    self.screen.blit(title_text, (20, 20))
                    title_text = font_text.render(f"Is_Running : {not self.pause}", True, COLOR)
                    self.screen.blit(title_text, (20, 60))



                if not self.pause:
                    self.update_generation()

                pygame.display.flip()

            elif self.loading_screen == 2:  # Colored Game
                self.Col_Game.cols = WIN_WIDTH // self.Col_Game.cell_size
                self.Col_Game.rows = WIN_HEIGHT // self.Col_Game.cell_size

                self.Col_Game.handle_events()
                self.screen.fill(BLACK)
                if self.Col_Game.random:
                    self.Col_Game.randomizer()
                    self.Col_Game.random = False
                self.Col_Game.draw_grid()

                if self.Col_Game.back == True:
                    self.loading_screen = 1
                
                if self.Col_Game.show:
                    title_text = font_text.render(f"Generation : {self.Col_Game.generation}", True, COLOR)
                    self.screen.blit(title_text, (20, 20))
                    title_text = font_text.render(f"Is_Running : {not self.Col_Game.pause}", True, COLOR)
                    self.screen.blit(title_text, (20, 60))

                if not self.Col_Game.pause:
                    self.Col_Game.update_generation()

                pygame.display.flip()

            elif self.loading_screen == 3:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_b:
                            self.loading_screen = 1

                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        mx, my = pygame.mouse.get_pos()
                        if 20 <= mx <= 20 + button_width + 30 and 340 <= my <= 340 + button_height:
                            self.Col_Game.cell_size -=1
                            self.cell_size -=1
                            if self.cell_size < 1:
                                self.cell_size = 1
                            if self.Col_Game.cell_size <1:
                                self.Col_Game.cell_size = 1
                        if button_width + 70 <= mx <= 2*button_width + 60 and 340 <= my <= 340 + button_height:
                            self.Col_Game.cell_size +=1
                            self.cell_size +=1

                        
                        if 20 <= mx <= 20 + button_width + 30 and 460 <= my <= 460 + button_height:
                            self.Col_Game.chance -=1
                            self.chance -=1
                            if self.chance < 0:
                                self.chance = 0
                            if self.Col_Game.chance < 0:
                                self.Col_Game.chacne = 0
                        if button_width + 70 <= mx <= 2*button_width + 60 and 460 <= my <= 460 + button_height:
                            self.Col_Game.chance +=1
                            self.chance +=1
                        

                        

                self.screen.fill(BLACK)
                title_text = font_text.render("Press \'F\' to Show the Generation in each Game mode", True, WHITE)
                self.screen.blit(title_text, (20, 20))

                title_text = font_text.render("Press \'Q\' to Start the Generations in each Game mode", True, WHITE)
                self.screen.blit(title_text , (20,60))

                title_text = font_text.render("Press \'B\' to get back to the Main Menu at anytime", True, WHITE)
                self.screen.blit(title_text , (20,100))

                title_text = font_text.render("\"Left Mouse Click\" or \"Hold Left Mouse Click\" to Place Cells ", True, WHITE)
                self.screen.blit(title_text , (20,140))

                title_text = font_text.render("Press \'R\' to reset the generation and grid in each Game mode", True, WHITE)
                self.screen.blit(title_text , (20,180))

                title_text = font_text.render("Press \'T\' to randomize the grid in each Game mode", True, WHITE)
                self.screen.blit(title_text , (20,220))

                title_text = font_text.render(f"Current Cell size : {self.cell_size}", True, WHITE)
                self.screen.blit(title_text , (20,260))

                title_text = font_text.render("Change the cell size by buttons given below :-", True, WHITE)
                self.screen.blit(title_text , (20,300))

                self.draw_pixelated_button( 20, 340, button_width + 30, button_height, RED)
                title_text = font_text.render("Cell size - 1", True, WHITE)
                self.screen.blit(title_text , (30,360))

                self.draw_pixelated_button( button_width + 70, 340, button_width + 25, button_height, GREEN)
                title_text = font_text.render("Cell size + 1", True, WHITE)
                self.screen.blit(title_text , (button_width + 70,360))



                title_text = font_text.render(f"Random Chances for WHITE in Randomizer : {self.chance}%", True, WHITE)
                self.screen.blit(title_text , (20,420))

                self.draw_pixelated_button( 20, 460, button_width + 30, button_height, RED)
                title_text = font_text.render("Chance - 1", True, WHITE)
                self.screen.blit(title_text , (30,480))

                self.draw_pixelated_button( button_width + 70, 460, button_width + 25, button_height, GREEN)
                title_text = font_text.render("Chance + 1", True, WHITE)
                self.screen.blit(title_text , (button_width + 80,480))



                pygame.display.flip()


        pygame.quit()

if __name__ == "__main__":
    game = GridGame()
    game.run()
