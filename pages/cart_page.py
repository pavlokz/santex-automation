from .base_page import BasePage

class CartPage(BasePage):
    CART_ITEMS = ".cart_item"
    CHECKOUT_BUTTON = "button[data-test='checkout']"
    REMOVE_BUTTON = "button:has-text('Remove')"

    def is_loaded(self) -> bool:
        return self.page.is_visible(self.CART_ITEMS)

    def remove_product_by_name(self, name: str):
        # Busca el item por nombre y clickea Remove
        item = self.page.locator(self.CART_ITEMS).filter(has_text=name).first
        if item and item.count() > 0:
            item.locator("button", has_text="Remove").click()

    def get_items(self) -> list[str]:
        items = []
        for el in self.page.locator(self.CART_ITEMS).all():
            title_el = el.locator(".inventory_item_name")
            title = title_el.text_content().strip() if title_el else ""
            items.append(title)
        return items

    def click_checkout(self):
        self.page.click(self.CHECKOUT_BUTTON)