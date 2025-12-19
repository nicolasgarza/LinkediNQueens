from queens import NQueens
from browser import Browser
from time import sleep

def main():
    # run_queens()
    browser = Browser()
    board, tile_pointers = browser.open() # TODO: make the variable/function names better here

    queens = NQueens(board)
    solution = queens.solve()
    for row in solution:
        print(row)
    # print(solution)

    browser.write_solution(solution, tile_pointers, queens.starting_queens)
    print(board)
    sleep(10)
    browser.close()


if __name__ == "__main__":
    main()
