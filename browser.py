from playwright.sync_api import sync_playwright

class Browser:
    def __init__(self):
        self.playwright_runtime = sync_playwright().start()
        self.browser = self.playwright_runtime.chromium.launch(
            headless=False,
        )
        self.context = self.browser.new_context()
        self.page = self.context.new_page()

    def open(self):
        self.page.goto("https://linkedin.com/games/queens/")

        """
        html = self.page.content()
        with open("page.html", "w", encoding="utf-8") as f:
            f.write(html)

        print("Frames:")
        for i, frame in enumerate(self.page.frames):
            print(i, frame.url)
        """

        frame = self.page.frame_locator("iframe[title='games']")
        button = frame.get_by_role("button", name="Start game")
        button.click()

        input("enter to close\n")

    def close(self):
        self.browser.close()
        self.playwright_runtime.stop()
