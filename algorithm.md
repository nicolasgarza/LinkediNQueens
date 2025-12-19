thoughts:
Each tile has attributes of: color, occupied, blocked, and maybe locked.
"occupied" is for when there is a queen on that square,
and "blocked" is for when there's a queen on another square that prevents us
from placing anything on that square.
locked will probaby need to be used in the future - in the game you are given some queens at the
start, we don't want to ever backtrack on those queens, they should be "locked."

Each color, or section, should probably be its own struct.
We should know what area it takes up, and if there's a queen already in that section.

For now, let's just represent the board as an array of... tuples?

initial backtracking algo:
```
class NQueens:
    def solveNQueens(self, n):
        def create_board(state):
            pass

        def backtrack(row, cols, state):
            # base case
            if row == n and all(section.has_queen()):
                return self.board

            for col in range(n):
                # If the queen is not placeable
                if (
                    col in cols
                    or other_queen_in_neighboring_region(x, y)
                ):
                    continue

                # "Add" the queen to the board
                cols.add(col)
                state[row][col] = "Q"

                # Move on to the next row with the updated board state
                backtrack(row + 1, diagonals, anti_diagonals, cols, state)

                # "Remove" the queen from the board since we have already
                # explored all valid paths using the above function call
                cols.remove(col)
                state[row][col] = "."

        ans = []
        empty_board = [["."] * n for _ in range(n)]
        backtrack(0, set(), set(), set(), empty_board)
        return ans
```

would also be cool to make a fuzzer. don't need to autogenerate boards. just generate with different combinations of
 queens being removed from a solved (valid) board.

 """Original board
    board = [
             [(True, "purple"), (False, "orange"), (False, "orange"), (False, "orange"), (False, "orange"),],
             [(False, "blue"), (False, "green"), (False, "blue"), (True, "orange"), (False, "blue"),],
             [(False, "blue"), (True, "green"), (False, "blue"), (False, "blue"), (False, "blue"),],
             [(False, "blue"), (False, "blue"), (False, "blue"), (False, "grey"), (True, "grey"),],
             [(False, "blue"), (False, "blue"), (True, "blue"), (False, "blue"), (False, "blue"),],
            ]

    no queens:
    board = [
             [(False, "purple"), (False, "orange"), (False, "orange"), (False, "orange"), (False, "orange"),],
             [(False, "blue"), (False, "green"), (False, "blue"), (False, "orange"), (False, "blue"),],
             [(False, "blue"), (False, "green"), (False, "blue"), (False, "blue"), (False, "blue"),],
             [(False, "blue"), (False, "blue"), (False, "blue"), (False, "grey"), (False, "grey"),],
             [(False, "blue"), (False, "blue"), (False, "blue"), (False, "blue"), (False, "blue"),],
            ]
    """
