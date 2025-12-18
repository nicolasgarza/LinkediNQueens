from queens import NQueens
from browser import Browser

def run_queens():
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
    solution.solve()

def run_browser():
    browser = Browser()
    browser.open()
    browser.close()

def main():
    # run_queens()
    run_browser()

if __name__ == "__main__":
    main()
