import copy
import pathlib
import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        cell_height, cell_width = self.rows, self.cols
        grid: list[list[int]] = []
        for _ in range(cell_height):
            row = (
                [random.randint(0, 1) for _ in range(cell_width)]
                if randomize == True
                else [0 for _ in range(cell_width)]
            )
            grid.append(row)

        return grid

    def _cell_exists(self, cell_coordinates: tuple[int, int]) -> bool:
        last_element_height, last_element_width = self.rows - 1, self.cols - 1
        cell_row, cell_col = cell_coordinates
        if 0 <= cell_row <= last_element_height and 0 <= cell_col <= last_element_width:
            return True
        return False

    def get_neighbours(self, cell: Cell) -> Cells:
        cell_row, cell_col = cell
        candidates = [
            (cell_row - 1, cell_col),
            (cell_row, cell_col - 1),
            (cell_row + 1, cell_col),
            (cell_row, cell_col + 1),
            (cell_row - 1, cell_col - 1),
            (cell_row + 1, cell_col - 1),
            (cell_row - 1, cell_col + 1),
            (cell_row + 1, cell_col + 1),
        ]
        checked_candidates: list[int] = []
        for candidate in candidates:
            if self._cell_exists(candidate):
                candidate_row, candidate_col = candidate
                checked_candidates.append(self.curr_generation[candidate_row][candidate_col])
        return checked_candidates

    def get_next_generation(self) -> Grid:
        actual_grid = copy.deepcopy(self.curr_generation)
        for row_number, row in enumerate(actual_grid):
            for col_number, col in enumerate(row):
                alive_cells = sum(self.get_neighbours((row_number, col_number)))
                if actual_grid[row_number][col_number] == 1:
                    actual_grid[row_number][col_number] = 1 if 2 <= alive_cells <= 3 else 0
                else:
                    actual_grid[row_number][col_number] = 1 if alive_cells == 3 else 0
        return actual_grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = self.curr_generation
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if self.max_generations == None:
            raise ValueError("There is no max generations value")
        return self.generations >= self.max_generations

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.prev_generation != self.curr_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        rows: list[list[int]] = []
        with open(filename, "r") as inp:
            for line in inp:
                rows.append(list(map(int, line.strip().split())))
        row_count, col_count = len(rows), len(rows[0])
        output = GameOfLife((row_count, col_count), False)
        output.curr_generation = rows
        return output

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with open(filename, "w") as out:
            current_state = self.curr_generation
            for row in current_state:
                out.write(" ".join(map(str, row)) + "\n")
