from .base_page import BasePage

class ProductsPage(BasePage):
    # Example locators
    PRODUCT_TITLE = ".inventory_list .inventory_item"
    ADD_TO_CART_BTN = "button[data-test='add-to-cart-sauce-labs-backpack']"  # use dynamic locators in real code
    CART_BADGE = ".shopping_cart_badge"
    BURGER_BUTTON = "#react-burger-menu-btn"
    LOGOUT_LINK = "#logout_sidebar_link"

    def add_first_product(self):
        # Add the first product button more generically
        btn = self.page.locator("button", has_text="Add to cart").first
        btn.click()

    def add_product_by_name(self, name: str):
        # find product container by name and click its add button
        item = self.page.locator(".inventory_item").filter(has_text=name)
        item.locator("button").click()

    def open_cart(self):
        self.page.click(".shopping_cart_link")