import math
from playwright.sync_api import sync_playwright
from playwright.sync_api import expect
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
        sleep(1)

        self.log_html_and_frames()
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
        print("wrote solution")


    def close(self):
        self.browser.close()
        self.playwright_runtime.stop()

    def get_game_scope(self):
        # If game is in top-level
        if self.page.locator("#queens-grid").count() > 0:
            return self.page

        if self.page.locator("[data-testid='interactive-grid']").count() > 0:
            return self.page

        # Otherwise, look through frames
        for f in self.page.frames:
            try:
                if f.locator("#queens-grid").count() > 0:
                    print("Using frame:", f.url)
                    return f
                if f.locator("[data-testid='interactive-grid']").count() > 0:
                    return f
            except Exception:
                pass

        # Fallback: locate by the tile aria-label pattern
        for f in self.page.frames:
            try:
                if f.locator("[aria-label*='row'][aria-label*='column']").count() > 0:
                    print("Using frame (tile aria-labels):", f.url)
                    return f
            except Exception:
                pass

        raise RuntimeError("could not find game scope (no #queens-grid and no tile aria-label tiles)")

    def get_tiles(self):
        grid = self.page.locator("[data-testid='interactive-grid']")
        cells = grid.locator("[data-testid^='cell-']")

        n = cells.count()
        if n == 0:
            raise RuntimeError("No cells found under interactive-grid")

        side = int(math.isqrt(n))
        if side * side != n:
            raise RuntimeError(f"Expected square board, got {n} cells")

        all_cells = cells.all()

        # get common classes, need to determine what is unique per color
        common = set(all_cells[0].get_attribute("class").split())
        for c in all_cells[1:]:
            common &= set(c.get_attribute("class").split())

        board, tile_pointers = [[]], [[]]

        for cell in all_cells:
            idx = int(cell.get_attribute("data-cell-idx"))
            if idx != 0 and idx % side == 0:
                board.append([])
                tile_pointers.append([])

            has_queen = cell.locator("[data-testid='queen-svg'], svg[aria-label='Queen']").count() > 0

            classes = set(cell.get_attribute("class").split())
            extras = sorted(classes - common)
            color = extras[0] if extras else "unknown"  # region key

            board[-1].append((has_queen, color))
            tile_pointers[-1].append(cell)

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
        with open("page.html", "w", encoding="utf-8") as f:
            f.write(self.page.content())

        for i, fr in enumerate(self.page.frames):
            try:
                with open(f"frame_{i}.html", "w", encoding="utf-8") as f:
                    f.write(fr.content())
            except Exception:
                pass

        print("Frames:")
        for i, fr in enumerate(self.page.frames):
            print(i, fr.url)


