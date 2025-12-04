from .base_page import BasePage

class ProductsPage(BasePage):
    # Page-level selectors
    PRODUCTS_CONTAINER = ".inventory_list"
    PRODUCT_ITEM = ".inventory_item"
    CART_LINK = ".shopping_cart_link"
    CART_BADGE = ".shopping_cart_badge"
    BURGER_BUTTON = "#react-burger-menu-btn"
    LOGOUT_LINK = "#logout_sidebar_link"
    SORT_SELECT = "select[data-test='product_sort_container']"

    def is_loaded(self) -> bool:
        return self.page.is_visible(self.PRODUCTS_CONTAINER)

    def add_first_product(self):
        btn = self.page.locator("button", has_text="Add to cart").first
        btn.click()

    def add_product_by_name(self, name: str):
        item = self.page.locator(self.PRODUCT_ITEM).filter(has_text=name).first
        item.locator("button", has_text="Add to cart").click()

    def add_products_by_names(self, names: list[str]):
        for n in names:
            self.add_product_by_name(n)

    def open_cart(self):
        self.page.click(self.CART_LINK)

    def get_cart_count(self) -> int:
        if self.page.is_visible(self.CART_BADGE):
            text = self.page.text_content(self.CART_BADGE).strip()
            try:
                return int(text)
            except Exception:
                return 0
        return 0

    def open_menu(self):
        self.page.click(self.BURGER_BUTTON)

    def logout(self):
        self.open_menu()
        self.page.click(self.LOGOUT_LINK)

    def sort_by(self, option_text: str):
        # options e.g. "Price (low to high)"
        self.page.select_option(self.SORT_SELECT, label=option_text)