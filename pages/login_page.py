from playwright.sync_api import Page
from .base_page import BasePage

class LoginPage(BasePage):
    # Locators
    USER_INPUT = "input#user-name"
    PASS_INPUT = "input#password"
    LOGIN_BUTTON = "input#login-button"
    ERROR_CONTAINER = "h3[data-test='error']"

    def goto(self):
        super().goto("")

    def login(self, username: str, password: str):
        self.page.fill(self.USER_INPUT, username)
        self.page.fill(self.PASS_INPUT, password)
        self.page.click(self.LOGIN_BUTTON)

    def get_error(self):
        return self.page.text_content(self.ERROR_CONTAINER)