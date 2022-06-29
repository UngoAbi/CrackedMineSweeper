import random
from random import randint


class Minefield:
    def __init__(self, rows, colummns, mines):
        self.rows = rows
        self.columns = colummns
        self.mines = mines

        self.matrix = self.create_matrix()
        self.place_mines()

        self.mine_counter = mines
        self.timer = 0
        self.run = True

    def create_matrix(self):
        matrix = [
            [{'value': 0, 'is_visible': False, 'is_flagged': False} for _ in range(self.columns)]
            for _ in range(self.rows)
        ]
        return matrix

    def place_mines(self):
        mine_positions = self.generate_mine_positions()
        for y, x in mine_positions:
            self.matrix[y][x]['value'] = 'Mine'
            self.increment_neighbor_cells((y, x))

    def generate_mine_positions(self):
        mine_positions = set()
        while len(mine_positions) != self.mines:
            y_position = randint(0, self.rows - 1)
            x_position = randint(0, self.columns - 1)
            mine_positions.add((y_position, x_position))
        return mine_positions

    def increment_neighbor_cells(self, cell_position):
        for neighbor in self.get_neighbor_cells(cell_position):
            neighbor_y, neighbor_x = neighbor
            if self.matrix[neighbor_y][neighbor_x]['value'] != 'Mine':
                self.matrix[neighbor_y][neighbor_x]['value'] += 1

    def get_neighbor_cells(self, cell_position):
        position_offsets = (-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)
        y, x = cell_position
        neighbor_cells = list()
        for y_offset, x_offset in position_offsets:
            new_y = y + y_offset
            new_x = x + x_offset
            if self.is_in_bounds((new_y, new_x)):
                neighbor_cells.append((new_y, new_x))
        return neighbor_cells

    def is_in_bounds(self, cell_position):
        y, x = cell_position
        return 0 <= y < self.rows and 0 <= x < self.columns

    def update_neighbors(self, cell_position):
        y, x = cell_position
        if self.matrix[y][x]['value'] != 0:
            return

        for neighbor in self.get_neighbor_cells(cell_position):
            neighbor_y, neighbor_x = neighbor

            if not self.matrix[neighbor_y][neighbor_x]['is_visible'] and self.matrix[neighbor_y][neighbor_x]['value'] != 'Mine':
                self.matrix[neighbor_y][neighbor_x]['is_visible'] = True
                self.update_neighbors((neighbor_y, neighbor_x))

    def get_mines(self):
        mines = []
        for y, row in enumerate(self.matrix):
            for x, cell in enumerate(row):
                if cell['value'] == 'Mine':
                    mines.append((y, x))
        return mines

    def get_mine_counter(self):
        flagged_cells = len([True for row in self.matrix for cell in row if cell['is_flagged']])
        return self.mines - flagged_cells

    def game_is_finished(self):
        for cell in [cell for row in self.matrix for cell in row]:
            if cell['value'] != 'Mine' and not cell['is_visible']:
                return False
        else:
            return True
