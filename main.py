import pickle
from playwright.sync_api import Playwright, sync_playwright, BrowserContext, Browser, Page, TimeoutError
from os import path

from config import URL, EMAIL, PASSWORD, COOKIES_FILE_NAME


class HhCvUp:
    def __init__(self):
        ...

    def start(self):
        with sync_playwright() as playwright:
            context, browser = self.make_context(playwright)
            if not path.exists(COOKIES_FILE_NAME):
                page = context.new_page()
                self.auth(context, page)
            else:
                context_with_cookies = self.add_cookies(context)
                page = context_with_cookies.new_page()
            self.cv_up(page)
            context.close()
            context_with_cookies.close()
            browser.close()

    def make_context(self, playwright: Playwright) -> tuple[BrowserContext, Browser]:
        browser = playwright.chromium.launch()
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        return context, browser

    def add_cookies(self, context) -> BrowserContext:
        cookies = pickle.load(open('cookies.pkl', 'rb'))
        context.add_cookies(cookies)
        return context

    def save_to_cookies(self, cookies: BrowserContext.cookies) -> None:
        pickle.dump(cookies(), open(COOKIES_FILE_NAME, 'wb'))

    def auth(self, context: BrowserContext, page: Page) -> None:
        page.goto(URL)
        page.get_by_role("link", name="Войти").click()
        page.get_by_role("button", name="Войти с паролем").click()
        page.get_by_placeholder("Электронная почта или телефон").click()
        page.get_by_placeholder("Электронная почта или телефон").fill(EMAIL)
        page.get_by_placeholder("Электронная почта или телефон").press("Tab")
        page.get_by_placeholder("Пароль").fill(PASSWORD)
        page.get_by_placeholder("Пароль").press("Enter")
        self.save_to_cookies(context.cookies)

    def cv_up(self, page) -> None:
        page.goto(URL)
        try:
            page.get_by_role("button", name="Обновить дату").click()
        except TimeoutError:
            return


if __name__ == '__main__':
    HhCvUp().start()
