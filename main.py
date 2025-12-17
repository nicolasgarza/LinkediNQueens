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
    def __init__(self, section, blocked=False, occupied=False, locked=False):
        self.occupied = occupied or locked
        self.blocked = blocked or self.occupied
        self.locked = locked
        self.section = section

class Section:
    def __init__(self, color, has_queen):
        self.color = color
        self.tiles = set()
        self.has_queen = has_queen

    # might want to just move this to NQueens class
    def add(self, x, y):
        self.tiles.add((x, y))

    def remove(self, x, y):
        self.tiles.remove((x, y))

    def has_queen(self):
        return self.has_queen

    def __rich__(self):
        return Text(str(self.tiles), style=f"on {self.color}")

class NQueens:

    color_picker = Color()
    def __init__(self, starting_board):
        self.ROWS, self.COLS = len(starting_board), len(starting_board[0])
        self.board = [[None for _ in range(self.COLS)] for _ in range(self.ROWS)]
        self.sections = []

        color_map = {} # color string: Section
        for i in range(self.ROWS):
            for j in range(self.COLS):
                has_queen, color = starting_board[i][j]

                if color in color_map:
                    # get section for this color
                    section = color_map[color]
                else:
                    # doesn't exist, create new section
                    section = Section(self.color_picker.get_color(), has_queen)
                    self.sections.append(section)
                    color_map[color] = section

                section.add(i, j)
                self.board[i][j] = Tile(section, locked=has_queen)

    def __repr__(self):
        res = []
        for row in self.board:
            for tile in row:
                glyph = " Q " if tile.occupied else " _ "
                res.append(glyph)
            res.append("\n")

        return "".join(res)

    def __rich__(self):
        out = Text()
        for row in self.board:
            for tile in row:
                glyph = " Q " if tile.occupied else " _ "
                out.append(glyph, style=f"on {tile.section.color}")
            out.append("\n")

        return out

    def print_sections(self):
        print("sections:")
        for section in self.sections:
            print(section, )



def main():
    board = [
             [(True, "purple"), (False, "orange"), (False, "orange"), (False, "orange"), (False, "orange"),],
             [(False, "blue"), (False, "green"), (False, "blue"), (True, "orange"), (False, "blue"),],
             [(False, "blue"), (True, "green"), (False, "blue"), (False, "blue"), (False, "blue"),],
             [(False, "blue"), (False, "blue"), (False, "blue"), (False, "grey"), (True, "grey"),],
             [(False, "blue"), (False, "blue"), (True, "blue"), (False, "blue"), (False, "blue"),],
            ]
    solution = NQueens(board)
    print(solution)
    solution.print_sections()



if __name__ == "__main__":
    main()
