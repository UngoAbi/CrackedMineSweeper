from random import randrange


class Cell:
    def __init__(self) -> None:
        self.value = 0
        self.is_visible = False
        self.is_flagged = False


class Minefield:
    def __init__(self, rows: int, columns: int, mines: int) -> None:
        self.rows = rows
        self.columns = columns
        self.mines = mines

        self.matrix = self.make_matrix()
        self.place_mines()

        self.mine_counter = self.mines
        self.timer = 0
        self.run = True

    def __repr__(self) -> str:
        return "\n".join([" ".join([str(cell.value) for cell in row]) for row in self.matrix])

    def get_unique_mine_position(self) -> tuple[int, int]:
        y, x = randrange(self.rows), randrange(self.columns)
        while self.matrix[y][x].value == -1:
            y, x = randrange(self.rows), randrange(self.columns)
        return y, x

    def get_neighbor_cells(self, cell_position: tuple) -> list[tuple[int, int]]:
        position_offsets = (-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)
        y, x = cell_position
        neighbor_cells = list()

        for y_offset, x_offset in position_offsets:
            new_y = y + y_offset
            new_x = x + x_offset
            if self.is_in_bounds(new_y, new_x):
                neighbor_cells.append((new_y, new_x))

        return neighbor_cells

    def get_mines(self) -> list[tuple[int, int]]:
        mines = []
        for y, row in enumerate(self.matrix):
            for x, cell in enumerate(row):
                if cell.value == -1:
                    mines.append((y, x))
        return mines

    def get_mine_counter(self):
        flagged_cells = len([True for row in self.matrix for cell in row if cell.is_flagged])
        return self.mines - flagged_cells

    def is_in_bounds(self, y: int, x: int) -> bool:
        return 0 <= y < self.rows and 0 <= x < self.columns

    def make_matrix(self) -> list[list[Cell]]:
        matrix = [[Cell() for _ in range(self.columns)] for _ in range(self.rows)]
        return matrix

    def place_mines(self) -> None:
        for _ in range(self.mines):
            y, x = self.get_unique_mine_position()
            self.matrix[y][x].value = -1
            self.increment_neighbor_cells((y, x))

    def increment_neighbor_cells(self, cell_position: tuple[int, int]) -> None:
        for neighbor in self.get_neighbor_cells(cell_position):
            y, x = neighbor
            if self.matrix[y][x].value != -1:
                self.matrix[y][x].value += 1

    def update_neighbors(self, cell_position) -> None:
        y, x = cell_position
        if self.matrix[y][x].value != 0:
            return

        for neighbor in self.get_neighbor_cells(cell_position):
            neighbor_y, neighbor_x = neighbor

            if not self.matrix[neighbor_y][neighbor_x].is_visible and self.matrix[neighbor_y][neighbor_x].value != -1:
                self.matrix[neighbor_y][neighbor_x].is_visible = True
                self.update_neighbors((neighbor_y, neighbor_x))

    def all_cells_cleared(self) -> bool:
        for cell in [cell for row in self.matrix for cell in row]:
            if cell.value != 'Mine' and not cell.is_visible:
                return False
        return True
