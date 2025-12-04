from .base_page import BasePage

class CheckoutPage(BasePage):
    FIRST_NAME = "input[data-test='firstName'], input#first-name"
    LAST_NAME = "input[data-test='lastName'], input#last-name"
    ZIP = "input[data-test='postalCode'], input#postal-code"
    CONTINUE_BTN = "input[data-test='continue'], input#continue"
    FINISH_BTN = "button[data-test='finish'], button#finish"
    ERROR_MSG = "h3[data-test='error']"
    COMPLETE_CONTAINER = ".checkout_complete_container"

    def fill_shipping(self, first_name: str, last_name: str, zip_code: str):
        self.page.fill(self.FIRST_NAME, first_name)
        self.page.fill(self.LAST_NAME, last_name)
        self.page.fill(self.ZIP, zip_code)
        self.page.click(self.CONTINUE_BTN)

    def finish(self):
        self.page.click(self.FINISH_BTN)

    def get_error(self) -> str:
        if self.page.is_visible(self.ERROR_MSG):
            return self.page.text_content(self.ERROR_MSG).strip()
        return ""

    def is_order_complete(self) -> bool:
        return self.page.is_visible(self.COMPLETE_CONTAINER)