from copy import deepcopy
from random import choice, randint
from typing import List, Optional, Tuple, Union

import pandas as pd


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    return [["■"] * cols for _ in range(rows)]


def remove_wall(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param coord:
    :return:
    """
    x, y = coord
    rows, cols = len(grid), len(grid[0])

    directions = []
    if x > 1 and grid[x - 2][y] == " ":
        directions.append((-1, 0))

    if y < cols - 2 and grid[x][y + 2] == " ":
        directions.append((0, 1))

    if not directions:
        return grid

    dx, dy = choice(directions)
    grid[x + dx][y + dy] = " "

    return grid


def bin_tree_maze(rows: int = 15, cols: int = 15, random_exit: bool = True) -> List[List[Union[str, int]]]:
    """

    :param rows:
    :param cols:
    :param random_exit:
    :return:
    """

    grid = create_grid(rows, cols)
    empty_cells = []
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if x % 2 == 1 and y % 2 == 1:
                grid[x][y] = " "
                empty_cells.append((x, y))

    # 1. выбрать любую клетку
    # 2. выбрать направление: наверх или направо.
    # Если в выбранном направлении следующая клетка лежит за границами поля,
    # выбрать второе возможное направление
    # 3. перейти в следующую клетку, сносим между клетками стену
    # 4. повторять 2-3 до тех пор, пока не будут пройдены все клетки
    for cell in empty_cells:
        x, y = cell
        neighbors = []
        if x > 1:
            neighbors.append((x - 1, y))
        if y < cols - 2:
            neighbors.append((x, y + 1))
        if neighbors:
            nx, ny = choice(neighbors)
            grid[nx][ny] = " "
    # генерация входа и выхода
    if random_exit:
        x_in, x_out = randint(0, rows - 1), randint(0, rows - 1)
        y_in = randint(0, cols - 1) if x_in in (0, rows - 1) else choice((0, cols - 1))
        y_out = randint(0, cols - 1) if x_out in (0, rows - 1) else choice((0, cols - 1))
    else:
        x_in, y_in = 0, cols - 2
        x_out, y_out = rows - 1, 1

    grid[x_in][y_in], grid[x_out][y_out] = "X", "X"

    return grid


def get_exits(grid: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:
    """

    :param grid:
    :return:
    """
    exits = []
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == "X":
                exits.append((i, j))
    return exits


def make_step(grid: List[List[Union[str, int]]], k: int) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param k:
    :return:
    """
    rows, cols = len(grid), len(grid[0])

    for x in range(rows):
        for y in range(cols):
            if grid[x][y] == k:
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < rows and 0 <= ny < cols:
                        if grid[nx][ny] == 0:
                            grid[nx][ny] = k + 1
    return grid


def shortest_path(
    grid: List[List[Union[str, int]]], exit_coord: Tuple[int, int]
) -> Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]:
    """

    :param grid:
    :param exit_coord:
    :return:
    """
    path = []
    x, y = exit_coord
    k = grid[x][y]

    if k == 0:
        return None

    while k > 1:
        path.append((x, y))
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]):
                if grid[nx][ny] == k - 1:
                    x, y = nx, ny
                    k -= 1
                    break
        else:
            grid[x][y] = " "
            if not path:
                return None
            x, y = path.pop()
            k += 1

    path.append((x, y))
    path.reverse()

    if len(path) == 1:
        return path[0]
    return path


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    """

    :param grid:
    :param coord:
    :return:
    """
    rows, cols = len(grid), len(grid[0])
    x, y = coord

    corners = {(0, 0), (0, cols - 1), (rows - 1, 0), (rows - 1, cols - 1)}
    if coord in corners:
        walls = 0
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols:
                if grid[nx][ny] == "■":
                    walls += 1
        return walls >= 2

    if x == 0 or x == rows - 1 or y == 0 or y == cols - 1:
        walls = 0
        open_paths = 0
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols:
                if grid[nx][ny] == "■":
                    walls += 1
                elif grid[nx][ny] == " ":
                    open_paths += 1
        if walls >= 3:
            return True
        return False

    return False


def solve_maze(
    grid: List[List[Union[str, int]]],
) -> Tuple[List[List[Union[str, int]]], Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]]:
    """

    :param grid:
    :return:
    """
    exits = get_exits(grid)
    if len(exits) < 2:
        return grid, exits[0] if exits else None

    start, end = exits[0], exits[1]

    if encircled_exit(grid, start):
        return grid, None

    rows, cols = len(grid), len(grid[0])
    for x in range(rows):
        for y in range(cols):
            if (x, y) == start:
                grid[x][y] = 1
            elif grid[x][y] == " " or grid[x][y] == "X":
                grid[x][y] = 0

    k = 1

    exit_x, exit_y = end
    while grid[exit_x][exit_y] == 0:
        grid = make_step(grid, k)
        k += 1
        if k > rows * cols:
            return grid, None
    path = shortest_path(grid, end)
    return grid, path


def add_path_to_grid(
    grid: List[List[Union[str, int]]], path: Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]
) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param path:
    :return:
    """

    if path:
        for i, row in enumerate(grid):
            for j, _ in enumerate(row):
                if (i, j) in path:
                    grid[i][j] = "X"
    return grid


if __name__ == "__main__":
    print(pd.DataFrame(bin_tree_maze(15, 15)))
    GRID = bin_tree_maze(15, 15)
    print(pd.DataFrame(GRID))
    _, PATH = solve_maze(GRID)
    MAZE = add_path_to_grid(GRID, PATH)
    print(pd.DataFrame(MAZE))
