from rich import print
from rich.text import Text
from itertools import cycle
from dataclasses import dataclass

COLORS = ["#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FF00FF", "#00FFFF", "#000000",
        "#FFFFFF", "#808080", "#FFA500",]

@dataclass
class Tile:
    section: "Section"
    has_queen: bool = False

    def __repr__(self):
        return f"{self.has_queen}"

class Section:
    def __init__(self, color):
        self.color = color
        self.tiles = set()
        self.contains_queen = False

    def __rich__(self):
        return Text(str(self.tiles), style=f"on {self.color}")

class NQueens:
    DIRS = [[1, 0], [0, 1], [-1, 0], [0, -1],
        [1, 1], [-1, 1], [-1, -1], [1, -1]]
    color_picker = cycle(COLORS)

    def __init__(self, starting_board):
        self.ROWS, self.COLS = len(starting_board), len(starting_board[0])
        self.board = [[None for _ in range(self.COLS)] for _ in range(self.ROWS)]
        self.sections = []
        self.static_rows, self.static_cols, self.starting_queens = set(), set(), set()

        color_map = {} # color string: Section
        for i in range(self.ROWS):
            for j in range(self.COLS):
                has_queen, region_key = starting_board[i][j]

                if region_key in color_map:
                    # get section for this color
                    section = color_map[region_key]
                else:
                    # doesn't exist, create new section
                    section = Section(next(self.color_picker))
                    self.sections.append(section)
                    color_map[region_key] = section

                section.tiles.add((i, j))
                self.board[i][j] = Tile(section)

                if has_queen:
                    self.starting_queens.add((i, j))
                    self.add_queen(i, j)
                    self.static_rows.add(i)
                    self.static_cols.add(j)

    def has_adjacent_queen(self, x, y):
        for dx, dy in self.DIRS:
            new_x = x + dx
            new_y = y + dy

            if (new_x >= 0 and new_x < self.ROWS and new_y >= 0 and new_y < self.COLS) and \
                    self.board[new_x][new_y].has_queen:
                return True

        return False

    def solve(self):
        for i in range(self.ROWS):
            if self._backtrack(i, set()): # found solution
                break

        # print(self)
        return self.board

    """
    This backtracking algorithm is taken from the leetcode editorial for n-queens, and adapted for
    the linkedin version of the game
    """
    def _backtrack(self, row, cols):
        # base case
        if all([section.contains_queen for section in self.sections]):
            print("found solution")
            return True
        if row >= self.ROWS:
            return False

        for col in range(self.COLS):
            # If the queen is not placeable
            if (
                col in cols
                or self.has_adjacent_queen(row, col)
                or self.board[row][col].section.contains_queen
                or row in self.static_rows
                or col in self.static_cols
            ):
                continue

            # add the queen to the board
            cols.add(col)
            self.add_queen(row, col)

            res = self._backtrack(row + 1, cols)
            if res:
                return True

            # remove queen from the board since we have already
            # explored all valid paths using the above function call
            cols.remove(col)
            self.remove_queen(row, col)

        return False

    def add_queen(self, row, col):
        tile = self.board[row][col]
        tile.has_queen = True
        tile.section.contains_queen = True

    def remove_queen(self, row, col):
        tile = self.board[row][col]
        tile.has_queen = False
        tile.section.contains_queen = False

    def __repr__(self):
        res = []
        for row in self.board:
            for tile in row:
                glyph = " Q " if tile.has_queen else " _ "
                res.append(glyph)
            res.append("\n")

        return "".join(res)

    def __rich__(self):
        out = Text()
        for row in self.board:
            for tile in row:
                glyph = " Q " if tile.has_queen else " _ "
                out.append(glyph, style=f"on {tile.section.color}")
            out.append("\n")

        return out

    def print_sections(self):
        print("sections:")
        for section in self.sections:
            print(section, )
