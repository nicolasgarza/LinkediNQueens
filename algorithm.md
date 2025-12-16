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

        def backtrack(row, diagonals, anti_diagonals, cols, state):
            # Base case
            if row == n:
                ans.append(create_board(state))
                return

            for col in range(n):
                curr_diagonal = row - col
                curr_anti_diagonal = row + col
                # If the queen is not placeable
                if (
                    col in cols
                    or curr_diagonal in diagonals
                    or curr_anti_diagonal in anti_diagonals
                ):
                    continue

                # "Add" the queen to the board
                cols.add(col)
                diagonals.add(curr_diagonal)
                anti_diagonals.add(curr_anti_diagonal)
                state[row][col] = "Q"

                # Move on to the next row with the updated board state
                backtrack(row + 1, diagonals, anti_diagonals, cols, state)

                # "Remove" the queen from the board since we have already
                # explored all valid paths using the above function call
                cols.remove(col)
                diagonals.remove(curr_diagonal)
                anti_diagonals.remove(curr_anti_diagonal)
                state[row][col] = "."

        ans = []
        empty_board = [["."] * n for _ in range(n)]
        backtrack(0, set(), set(), set(), empty_board)
        return ans
```
