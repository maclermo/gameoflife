# import pygame
import numpy as np
from time import sleep
from termcolor import colored


class GameOfLife:
    def __init__(self):
        self.num_of_rows = 25
        self.num_of_cols = 50
        self.speed = 2
        self.grid = np.zeros((self.num_of_rows, self.num_of_cols), dtype=int)
        self.buffer_grid = np.zeros((self.num_of_rows, self.num_of_cols), dtype=int)

    def setShape(self):  # Glider
        self.grid[3][2] = 1
        self.grid[4][3] = 1
        self.grid[4][4] = 1
        self.grid[2][4] = 1
        self.grid[3][4] = 1

    def findNeighbours(self, x, y):
        return (
            self.buffer_grid[(x - 1) % self.num_of_rows, y]
            + self.buffer_grid[(x + 1) % self.num_of_rows, y]
            + self.buffer_grid[x, (y - 1) % self.num_of_cols]
            + self.buffer_grid[x, (y + 1) % self.num_of_cols]
            + self.buffer_grid[(x - 1) % self.num_of_rows, (y - 1) % self.num_of_cols]
            + self.buffer_grid[(x + 1) % self.num_of_rows, (y - 1) % self.num_of_cols]
            + self.buffer_grid[(x - 1) % self.num_of_rows, (y + 1) % self.num_of_cols]
            + self.buffer_grid[(x + 1) % self.num_of_rows, (y + 1) % self.num_of_cols]
        )

    def tick(self):
        self.buffer_grid = np.copy(self.grid)

        sleep(self.speed * 0.1)

        for x in range(0, self.num_of_rows):
            for y in range(1, self.num_of_cols):
                self.ruleOne(x, y)
                self.ruleTwo(x, y)
                self.ruleThree(x, y)
                self.ruleFour(x, y)

    def ruleOne(self, x, y):
        # Any live cell with fewer than two live neighbours dies, as if by underpopulation.

        no_of_live_neighbours = self.findNeighbours(x, y)

        if no_of_live_neighbours < 2 and self.grid[x, y]:
            self.grid[x, y] = 0

    def ruleTwo(self, x, y):
        # Any live cell with two or three live neighbours lives on to the next generation.

        no_of_live_neighbours = self.findNeighbours(x, y)

        if (no_of_live_neighbours == 2 or no_of_live_neighbours == 3) and self.grid[x, y]:
            self.grid[x, y] = 1

    def ruleThree(self, x, y):
        # Any live cell with more than three live neighbours dies, as if by overpopulation.

        no_of_live_neighbours = self.findNeighbours(x, y)

        if no_of_live_neighbours > 3 and self.grid[x, y]:
            self.grid[x, y] = 0

    def ruleFour(self, x, y):
        # Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.

        no_of_live_neighbours = self.findNeighbours(x, y)

        if no_of_live_neighbours == 3 and not self.grid[x, y]:
            self.grid[x, y] = 1

    def showOutput(self):
        for x in self.grid:
            for y in x:
                if y:
                    print(colored("  ", "red", attrs=["reverse"]), end="")
                else:
                    print(colored("  ", "white", attrs=["reverse"]), end="")
            print("")
        print("-----------------------")


def main():
    gol = GameOfLife()
    gol.setShape()

    while True:
        gol.tick()
        gol.showOutput()


if __name__ == "__main__":
    main()
