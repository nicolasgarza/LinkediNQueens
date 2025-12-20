from queens import NQueens
from browser import Browser
from time import sleep

def main():
    # run_queens()
    browser = Browser()
    board, tile_pointers = browser.open_login() # TODO: make the variable/function names better here

    queens = NQueens(board)
    solution = queens.solve()
    # for row in solution:
    #     print(row)
    # print(solution)

    browser.write_solution(solution, tile_pointers, queens.starting_queens)
    while True:
        continue
    # browser.close()


if __name__ == "__main__":
    main()
