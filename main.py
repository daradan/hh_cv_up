import pickle
from playwright.sync_api import Playwright, sync_playwright

from config import URL, EMAIL, PASSWORD


class HhCvUp():
    def __init__(self):
        ...

    def start(self):
        with sync_playwright() as playwright:
            self.auth_and_up_cv(playwright)

    def auth_and_up_cv(self, playwright: Playwright) -> None:
        browser = playwright.chromium.launch()
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = context.new_page()
        page.goto(URL)
        page.get_by_role("link", name="Войти").click()
        page.get_by_role("button", name="Войти с паролем").click()
        page.get_by_placeholder("Электронная почта или телефон").click()
        page.get_by_placeholder("Электронная почта или телефон").fill(EMAIL)
        page.get_by_placeholder("Электронная почта или телефон").press("Tab")
        page.get_by_placeholder("Пароль").fill(PASSWORD)
        page.get_by_placeholder("Пароль").press("Enter")
        page.is_visible('div.resume-sidebar-background')
        page.get_by_role("button", name="Обновить дату").click()
        pickle.dump(context.cookies(), open('cookies.pkl', 'wb'))
        context.close()
        browser.close()


if __name__ == '__main__':
    HhCvUp().start()
