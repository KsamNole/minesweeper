import pygame
import sys
import random
import math

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
LIGHT_GRAY = (198, 198, 198)


class Minesweeper:

    def __init__(self, width, height, cell_size, fps=30):
        self.width = width
        self.height = height
        self.fps = fps
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()

        self.cell_size = cell_size
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size
        self.margin = 10

    def draw_3d_box(self, x_0, y_0, x_1, y_1, margin):
        padding = 3
        up_left = (x_0 + margin, y_0 + margin)
        up_right = (x_1 - margin, y_0 + margin)
        down_left = (x_0 + margin, y_1 - margin)
        down_right = (x_1 - margin, y_1 - margin)
        pygame.draw.line(self.screen, GRAY, up_left, up_right, padding)
        pygame.draw.line(self.screen, GRAY, up_left, down_left, padding)
        pygame.draw.line(self.screen, WHITE, down_left, down_right, padding)
        pygame.draw.line(self.screen, WHITE, up_right, down_right, padding)

    def draw_field(self):
        self.draw_3d_box(0, 0, self.width, 70, self.margin)
        self.draw_3d_box(0, 70, self.width, self.height, self.margin)
        # 80 это отступ сверху от header (header занимает 70 пикселей + 10 пикселей margin)
        for i in range(self.margin + self.cell_size, self.width - self.margin, self.cell_size):
            pygame.draw.line(self.screen, BLACK, (i, 80), (i, self.height - self.margin))
        for i in range(80, self.height - self.margin, self.cell_size):
            pygame.draw.line(self.screen, BLACK, (self.margin, i), (self.width - self.margin, i))

    def create_grid(self):
        grid = []
        size = (self.width - self.margin) // self.cell_size
        for i in range(0, size):
            grid.append([])
            for j in range(0, size):
                grid[i].append(0)

        return grid

    def fill_grid(self, grid):
        size = (self.width - self.margin) // self.cell_size
        count = 0
        while count != 10:
            x = random.randint(0, 8)
            y = random.randint(0, 8)
            if grid[x][y] != 666:
                grid[x][y] = 666
                count += 1

        for x in range(0, size):
            for y in range(0, size):
                if grid[x][y] == 666:
                    for k in range(-1, 2):
                        for h in range(-1, 2):
                            if 0 <= x + k <= 8 and 0 <= y + h <= 8 and grid[x + k][y + h] != 666:
                                grid[x + k][y + h] += 1
        return grid

    def update_grid(self, grid):
        size = (self.width - self.margin) // self.cell_size
        # Подгружаем изображения
        bomb = pygame.image.load("images/bomb.png")
        one = pygame.image.load("images/1.png")
        two = pygame.image.load("images/2.png")
        three = pygame.image.load("images/3.png")
        four = pygame.image.load("images/4.png")
        cell = pygame.image.load("images/cell.png")
        flag = pygame.image.load("images/flag.png")

        for x in range(0, size):
            for y in range(0, size):
                coordinate = (self.margin + x * self.cell_size, 80 + y * self.cell_size)
                if grid[x][y] == 0:
                    self.screen.blit(cell, coordinate)
                if grid[x][y] == 666:
                    self.screen.blit(bomb, coordinate)
                if grid[x][y] == 1:
                    self.screen.blit(one, coordinate)
                if grid[x][y] == 2:
                    self.screen.blit(two, coordinate)
                if grid[x][y] == 3:
                    self.screen.blit(three, coordinate)
                if grid[x][y] == 4:
                    self.screen.blit(four, coordinate)
                if grid[x][y] == -1:
                    self.screen.blit(flag, coordinate)

    def clear_area(self, fill_grid, grid, x, y):
        array = [(x, y)]
        self.rec(array, fill_grid, x, y)
        for i in array:
            grid[i[0]][i[1]] = fill_grid[i[0]][i[1]] if fill_grid[i[0]][i[1]] != 0 else -5

    def rec(self, array, fill_grid, x, y):
        for i in range(-1, 2):
            for j in range(-1, 2):
                if 0 <= x + i <= 8 and 0 <= y + j <= 8 and not i == j == 0:
                    if fill_grid[x + i][y + j] == 0:
                        if (x + i, y + j) not in array:
                            array.append((x + i, y + j))
                            self.rec(array, fill_grid, x + i, y + j)
                    elif (x + i, y + j) not in array:
                        array.append((x + i, y + j))

    def run(self):
        pygame.init()
        pygame.font.init()

        font = pygame.font.SysFont('ebrima', 30)
        count, fill_grid, flags, grid, clock = self.restart()

        running = True

        while 1:
            self.clock.tick(self.fps)

            if count == 10:
                winner = font.render('You won!!!', True, (0, 200, 0))
                self.screen.blit(winner, (160, 10))
                running = False

            if count == -1:
                loser = font.render('Press R to restart', True, (200, 0, 0))
                self.screen.blit(loser, (120, 10))
                running = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == 114:
                        count, fill_grid, flags, grid, clock = self.restart()
                        running = True

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x = math.ceil((event.pos[0] - 10) / self.cell_size) - 1
                    y = math.ceil((event.pos[1] - 80) / self.cell_size) - 1

                    if event.button == 1:
                        if fill_grid[x][y] == 666:
                            count = -1

                        if fill_grid[x][y] == 0:
                            self.clear_area(fill_grid, grid, x, y)

                        grid[x][y] = fill_grid[x][y] if fill_grid[x][y] != 0 else -5

                    if event.button == 3:
                        if flags > 0 and grid[x][y] != -1 and fill_grid[x][y] != 0:
                            grid[x][y] = -1
                            flags -= 1
                            if fill_grid[x][y] == 666:
                                count += 1
                        elif grid[x][y] == -1:
                            grid[x][y] = 0
                            flags += 1
                            if fill_grid[x][y] == 666:
                                count -= 1

            if running:
                self.screen.fill(LIGHT_GRAY)
                self.draw_field()
                self.update_grid(grid)

                flags_text = font.render(str(flags), True, (112, 56, 230))
                self.screen.blit(flags_text, (30, 10))

                clock += 1 / self.fps
                time = font.render(str(round(clock, 1)), True, BLACK)
                self.screen.blit(time, (385, 10))

            pygame.display.flip()

    def restart(self):
        self.screen.fill(LIGHT_GRAY)
        grid = self.create_grid()
        fill_grid = self.fill_grid(self.create_grid())
        self.draw_field()
        self.update_grid(grid)
        count = 0
        flags = 10
        clock = 0
        return count, fill_grid, flags, grid, clock


if __name__ == '__main__':
    game = Minesweeper(470, 540, 50, 60)
    game.run()