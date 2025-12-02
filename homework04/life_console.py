import curses

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """Отобразить рамку."""

        rows, cols = self.life.rows, self.life.cols
        for col_number in range(1, cols - 1):
            screen.addstr(0, col_number, "-")
            screen.addstr(rows - 1, col_number, "-")
        for row_number in range(1, rows - 1):
            screen.addstr(row_number, 0, "|")
            screen.addstr(row_number, cols - 1, "|")

    def draw_grid(self, screen) -> None:
        """Отобразить состояние клеток."""
        grid = self.life.curr_generation
        rows, cols = self.life.rows, self.life.cols
        for row_number in range(1, rows - 1):
            for col_number in range(1, cols - 1):
                if grid[row_number][col_number] == 1:
                    screen.addstr(row_number, col_number, "#")
                else:
                    screen.addstr(row_number, col_number, " ")

    def run(self) -> None:
        screen = curses.initscr()

        curses.endwin()

        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        screen.nodelay(True)

        try:
            while self.life.is_changing and not self.life.is_max_generations_exceeded:
                screen.clear()
                self.draw_borders(screen)
                self.draw_grid(screen)
                screen.refresh()

                key = screen.getch()
                if key == ord("q"):
                    break

                self.life.step()
                curses.napms(150)

        finally:
            curses.nocbreak()
            curses.echo()
            curses.endwin()
        curses.endwin()


if __name__ == "__main__":
    game = GameOfLife(size=(10, 40), randomize=True)
    ui = Console(game)
    ui.run()
