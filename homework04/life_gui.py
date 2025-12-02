import typing as tp

import pygame
from life import GameOfLife
from pygame.locals import *
from ui import UI

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        self.height = cell_size * self.life.rows
        self.width = cell_size * self.life.cols
        self.cell_size = cell_size
        self.cell_height = self.cell_width = cell_size
        self.screen_size = (self.height, self.width)
        self.screen = pygame.display.set_mode(self.screen_size)
        self.grid = self.life.create_grid(True)
        self.speed = 10

    def draw_lines(self) -> None:
        # Copy from previous assignment
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def draw_grid(self) -> None:
        # Copy from previous assignment
        surface = self.screen
        for row_number, row in enumerate(self.life.curr_generation):
            for col_number, cell in enumerate(row):
                color = "green" if cell == 1 else "white"
                rect = (row_number * self.cell_height, col_number * self.cell_width, self.cell_height, self.cell_width)
                pygame.draw.rect(surface, color, rect)

    def run(self) -> None:
        # Copy from previous assignment
        """Запустить игру"""
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))
        is_paused = False

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    is_paused = not is_paused
                if is_paused and event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    row = x // self.cell_size
                    col = y // self.cell_size
                    self.life.curr_generation[row][col] = (self.life.curr_generation[row][col] + 1) % 2

            if not is_paused:

                self.life.step()

            self.draw_lines()
            self.draw_grid()
            pygame.display.flip()
            clock.tick(self.speed)

        pygame.quit()


if __name__ == "__main__":
    game = GameOfLife(size=(64, 48))
    gui = GUI(game)
    gui.run()
