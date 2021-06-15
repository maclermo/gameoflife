import sys
import pygame
import numpy as np
from random import choice
from math import floor

R = (255, 0, 0)
O = (255, 127, 0)
Y = (255, 255, 0)
G = (0, 255, 0)
B = (0, 0, 255)
I = (75, 0, 130)
V = (148, 0, 211)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class GameOfLife:
    def __init__(self, size=15, fps=60, play=False):
        self.size = size
        self.fps = fps
        self.play = play
        self.grid = np.zeros((self.size, self.size), dtype=int)
        self.buffer_grid = np.zeros((self.size, self.size), dtype=int)

    def findNeighbours(self, x, y):
        return (
            self.buffer_grid[(x - 1) % self.size, y]
            + self.buffer_grid[(x + 1) % self.size, y]
            + self.buffer_grid[x, (y - 1) % self.size]
            + self.buffer_grid[x, (y + 1) % self.size]
            + self.buffer_grid[(x - 1) % self.size, (y - 1) % self.size]
            + self.buffer_grid[(x + 1) % self.size, (y - 1) % self.size]
            + self.buffer_grid[(x - 1) % self.size, (y + 1) % self.size]
            + self.buffer_grid[(x + 1) % self.size, (y + 1) % self.size]
        )

    def next(self):
        if self.play:
            self.buffer_grid = np.copy(self.grid)

            for x in range(0, self.size):
                for y in range(0, self.size):
                    self.ruleOne(x, y)
                    self.ruleTwo(x, y)
                    self.ruleThree(x, y)
                    self.ruleFour(x, y)

    def ruleOne(self, x, y):
        # Any live cell with fewer than two live neighbours dies, as if by underpopulation.

        num_of_live_neighbours = self.findNeighbours(x, y)

        if num_of_live_neighbours < 2 and self.grid[x, y]:
            self.grid[x, y] = 0

    def ruleTwo(self, x, y):
        # Any live cell with two or three live neighbours lives on to the next generation.

        num_of_live_neighbours = self.findNeighbours(x, y)

        if (num_of_live_neighbours == 2 or num_of_live_neighbours == 3) and self.grid[x, y]:
            self.grid[x, y] = 1

    def ruleThree(self, x, y):
        # Any live cell with more than three live neighbours dies, as if by overpopulation.

        num_of_live_neighbours = self.findNeighbours(x, y)

        if num_of_live_neighbours > 3 and self.grid[x, y]:
            self.grid[x, y] = 0

    def ruleFour(self, x, y):
        # Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.

        num_of_live_neighbours = self.findNeighbours(x, y)

        if num_of_live_neighbours == 3 and not self.grid[x, y]:
            self.grid[x, y] = 1


def main():
    gol = GameOfLife(size=30, fps=30)

    pygame.init()

    fpsClock = pygame.time.Clock()
    screen = pygame.display.set_mode((gol.size ** 2, gol.size ** 2))
    pygame.display.set_caption("Conway's Game Of Life - Press ENTER to start/pause simulation (stopped)")
    game_mode = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if game_mode:
                        game_mode = 0
                    else:
                        game_mode = 1
                if event.key == pygame.K_RETURN:
                    if gol.play:
                        gol.play = False
                        pygame.display.set_caption(
                            "Conway's Game Of Life - Press ENTER to start/pause simulation (stopped)"
                        )
                    else:
                        gol.play = True
                        pygame.display.set_caption(
                            "Conway's Game Of Life - Press ENTER to start/pause simulation (running)"
                        )
            if event.type == pygame.MOUSEBUTTONUP:
                pos_x, pos_y = pygame.mouse.get_pos()
                x = floor(pos_x / gol.size)
                y = floor(pos_y / gol.size)
                if gol.grid[x, y]:
                    gol.grid[x, y] = 0
                else:
                    gol.grid[x, y] = 1

        gol.next()

        for x in range(0, gol.size):
            for y in range(0, gol.size):
                if gol.grid[x, y]:
                    if game_mode:
                        pygame.draw.rect(
                            screen, choice([R, O, Y, G, B, I, V]), (x * gol.size, y * gol.size, gol.size, gol.size), 0
                        )
                    else:
                        pygame.draw.rect(screen, BLACK, (x * gol.size, y * gol.size, gol.size, gol.size), 0)
                else:
                    pygame.draw.rect(screen, WHITE, (x * gol.size, y * gol.size, gol.size, gol.size), 0)

        pygame.display.update()
        fpsClock.tick(gol.fps)


if __name__ == "__main__":
    main()
