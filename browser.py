from playwright.sync_api import sync_playwright
from time import sleep

class Browser:
    def __init__(self):
        self.playwright_runtime = sync_playwright().start()
        self.browser = self.playwright_runtime.chromium.launch(
            headless=False,
        )
        self.context = self.browser.new_context()
        self.page = self.context.new_page()

    def open_incognito(self):
        self.page.goto("https://linkedin.com/games/queens/")

        # self.log_html_and_frames()

        frame = self.page.frame_locator("iframe[title='games']")
        frame.get_by_role("button", name="Start game").click()

        # self.log_html_and_frames()

        frame = self.page.frame_locator("iframe[title='games']")
        frame.get_by_role("button", name="Dismiss").click()

        board, tile_pointers = self.get_tiles()

        return board, tile_pointers

    def open_login(self):
        self.login()
        self.page.goto("https://linkedin.com/games/queens/")


        sleep(3)

        # self.log_html_and_frames()
        board, tile_pointers = self.get_tiles()
        # print(board)

        return board, tile_pointers

    def login(self):
        # im just going to type in the credentials myself i dont want to look like a bot
        self.page.goto("https://linkedin.com/login/")
        sleep(20)

    def write_solution(self, board, tile_pointers, starting_queens):
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j].has_queen and (i, j) not in starting_queens:
                    tile_pointers[i][j].dblclick()
        sleep(15)
        print("wrote solution")


    def close(self):
        self.browser.close()
        self.playwright_runtime.stop()

    def get_tiles(self):

        frame = self.page.frame_locator("iframe[title='games']")
        queens_grid = frame.locator("#queens-grid")
        self.log_html_and_frames()

        children = queens_grid.locator(":scope > div")
        board, tile_pointers, curr_row = [[]], [[]], 1
        for child in children.all():
            label = child.get_attribute("aria-label")
            if not label: continue

            label = label.split(" ")
            has_queen = label[0] == "Queen"
            color = self.extract_color(label)

            label_row = int(label[label.index("row") + 1].rstrip(","))
            if label_row == curr_row + 1:
                board.append([])
                tile_pointers.append([])
                curr_row += 1

            board[-1].append((has_queen, color))
            tile_pointers[-1].append(child)

        return board, tile_pointers

    def extract_color(self, words):
        color = []
        collecting = False

        for w in words:
            if w == "color":
                collecting = True
                continue

            if collecting:
                color.append(w.rstrip(","))

                if w.endswith(","):
                    break

        return " ".join(color)

    def log_html_and_frames(self):
        html = self.page.content()
        with open("page.html", "w", encoding="utf-8") as f:
            f.write(html)

        print("Frames1:")
        for i, frame in enumerate(self.page.frames):
            print(i, frame.url)

