from rich import print
from rich.text import Text

class Color:
    id = 0
    COLORS = [
        "#FF0000",  # red
        "#00FF00",  # green
        "#0000FF",  # blue
        "#FFFF00",  # yellow
        "#FF00FF",  # magenta
        "#00FFFF",  # cyan
        "#000000",  # black
        "#FFFFFF",  # white
        "#808080",  # gray
        "#FFA500",  # orange
    ]

    def __init__(self):
        pass

    def get_color(self):
        color = self.COLORS[self.id]
        self.id = (self.id + 1) % len(self.COLORS)
        return color
class Tile:
    def __init__(self, section, has_queen=False, locked=False):
        self.has_queen = has_queen or locked
        self.locked = locked
        self.section = section

class Section:
    def __init__(self, color):
        self.color = color
        self.tiles = set()
        self.contains_queen = False

    def section_contains_queen(self):
        return self.contains_queen

    def __rich__(self):
        return Text(str(self.tiles), style=f"on {self.color}")

class NQueens:

    color_picker = Color()
    def __init__(self, starting_board):
        self.ROWS, self.COLS = len(starting_board), len(starting_board[0])
        self.board = [[None for _ in range(self.COLS)] for _ in range(self.ROWS)]
        self.sections = []
        self.static_rows, self.static_cols = set(), set()

        color_map = {} # color string: Section
        for i in range(self.ROWS):
            for j in range(self.COLS):
                has_queen, color = starting_board[i][j]

                if color in color_map:
                    # get section for this color
                    section = color_map[color]
                else:
                    # doesn't exist, create new section
                    section = Section(self.color_picker.get_color())
                    self.sections.append(section)
                    color_map[color] = section

                if has_queen:
                    section.contains_queen = True
                    self.static_rows.add(i)
                    self.static_cols.add(j)

                section.tiles.add((i, j))
                self.board[i][j] = Tile(section, locked=has_queen)

    def other_queen_in_neighboring_region(self, x, y):
        dirs = [[1, 0], [0, 1], [-1, 0], [0, -1],
                [1, 1], [-1, 1], [-1, -1], [1, -1]]

        for dx, dy in dirs:
            new_x = x + dx
            new_y = y + dy

            if (new_x >= 0 and new_x < self.ROWS and new_y >= 0 and new_y < self.COLS) and \
                    self.board[new_x][new_y].has_queen:
                return True

        return False

    def Solution(self):
        for i in range(self.ROWS):
            if self._backtrack(i, set()): # found solution
                break

        print(self)

    """
    This backtracking algorithm is taken from the leetcode editorial for n-queens, and adapted for
    the linkedin version of the game
    """
    def _backtrack(self, row, cols):
        n = len(self.board)
        # base case
        if all([section.section_contains_queen() for section in self.sections]):
            print("found solution")
            return True

        for col in range(n):
            print(f"processing [{row}][{col}]")
            # If the queen is not placeable
            if (
                col in cols
                or self.other_queen_in_neighboring_region(row, col)
                or self.board[row][col].section.section_contains_queen()
                or row in self.static_rows
                or col in self.static_cols
            ):
                print(f"skipping [{row}][{col}]")
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

def main():
    """Original board
    board = [
             [(True, "purple"), (False, "orange"), (False, "orange"), (False, "orange"), (False, "orange"),],
             [(False, "blue"), (False, "green"), (False, "blue"), (True, "orange"), (False, "blue"),],
             [(False, "blue"), (True, "green"), (False, "blue"), (False, "blue"), (False, "blue"),],
             [(False, "blue"), (False, "blue"), (False, "blue"), (False, "grey"), (True, "grey"),],
             [(False, "blue"), (False, "blue"), (True, "blue"), (False, "blue"), (False, "blue"),],
            ]
    """
    board = [
             [(False, "purple"), (False, "orange"), (False, "orange"), (False, "orange"), (False, "orange"),],
             [(False, "blue"), (False, "green"), (False, "blue"), (False, "orange"), (False, "blue"),],
             [(False, "blue"), (False, "green"), (False, "blue"), (False, "blue"), (False, "blue"),],
             [(False, "blue"), (False, "blue"), (False, "blue"), (False, "grey"), (False, "grey"),],
             [(False, "blue"), (False, "blue"), (False, "blue"), (False, "blue"), (False, "blue"),],
            ]
    solution = NQueens(board)
    print(solution)
    solution.print_sections()

    # run algorithm
    solution.Solution()

if __name__ == "__main__":
    main()
