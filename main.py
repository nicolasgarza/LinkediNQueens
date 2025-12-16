from rich import print
from rich.text import Text

class Tile:

    def __init__(self, color, blocked=False, occupied=False, locked=False):
        self.color = color
        self.occupied = occupied or locked
        self.blocked = blocked or self.occupied
        self.locked = locked

class NQueens:
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

    def __init__(self, starting_board):
        ROWS, COLS = len(starting_board), len(starting_board[0])
        self.board = [[None for _ in range(COLS)] for _ in range(ROWS)]

        color_id, color_map = 0, {}
        for i in range(ROWS):
            for j in range(COLS):
                has_queen, color = starting_board[i][j]
                if color in color_map:
                    square_color = color_map[color]
                else:
                    color_id += 1
                    square_color = self.COLORS[color_id]
                    color_map[color] = square_color

                self.board[i][j] = Tile(square_color, locked=has_queen)

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
                out.append(glyph, style=f"on {tile.color}")
            out.append("\n")

        return out


def main():
    board = [
             [(False, "green"), (False, "green"), (False, "green"), (False, "green"),],
             [(False, "blue"), (False, "blue"), (True, "blue"), (False, "green"),],
             [(True, "orange"), (False, "blue"), (False, "red"), (False, "red"),],
             [(False, "orange"), (False, "blue"), (False, "grey"), (True, "grey"),],
            ]
    print(NQueens(board))


if __name__ == "__main__":
    main()
