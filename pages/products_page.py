from .base_page import BasePage
from playwright.sync_api import TimeoutError

class ProductsPage(BasePage):
    PRODUCTS_CONTAINER = ".inventory_list"
    PRODUCT_ITEM = ".inventory_item"
    CART_LINK = ".shopping_cart_link"
    CART_BADGE = ".shopping_cart_badge"
    BURGER_BUTTON = "#react-burger-menu-btn"
    LOGOUT_LINK = "#logout_sidebar_link"
    SORT_SELECT = "select[data-test='product_sort_container']"

    # Mapping label -> value (SauceDemo known values)
    SORT_LABEL_TO_VALUE = {
        "Name (A to Z)": "az",
        "Name (Z to A)": "za",
        "Price (low to high)": "lohi",
        "Price (high to low)": "hilo",
    }

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

    def sort_by(self, option_text: str, timeout: int = 10000):
        """
        Sort products by a visible option label (e.g. "Price (low to high)").
        Fallback: if selecting by label times out or is not available, try selecting by known value mapping.
        """
        locator = self.page.locator(self.SORT_SELECT)
        try:
            locator.wait_for(state="visible", timeout=timeout)
        except TimeoutError:
            raise TimeoutError(f"Sort select {self.SORT_SELECT} not visible after {timeout}ms")

        # Try selecting by label first (convenient for readability)
        try:
            locator.select_option(label=option_text)
            return
        except Exception:
            # fallback: try mapping label to value
            value = self.SORT_LABEL_TO_VALUE.get(option_text)
            if value:
                try:
                    locator.select_option(value=value)
                    return
                except Exception as e2:
                    raise Exception(f"Failed to select sort option by value='{value}': {e2}") from e2
            else:
                raise Exception(f"Could not select sort option: label '{option_text}' not found and no fallback value available")