from .base_page import BasePage
from playwright.sync_api import TimeoutError

class ProductsPage(BasePage):
    PRODUCTS_CONTAINER = ".inventory_list"
    PRODUCT_ITEM = ".inventory_item"
    CART_LINK = ".shopping_cart_link"
    CART_BADGE = ".shopping_cart_badge"
    BURGER_BUTTON = "#react-burger-menu-btn"
    LOGOUT_LINK = "#logout_sidebar_link"

    # posibles selectores para el control de ordenamiento (underscore / hyphen / clase)
    SORT_SELECT_CANDIDATES = [
        "select[data-test='product_sort_container']",
        "select[data-test='product-sort-container']",
        "select.product_sort_container",
        "select.product-sort-container",
        "select[class*='product_sort']",
        "select[class*='product-sort']",
        "[data-test='product_sort_container']",
        "[data-test='product-sort-container']",
    ]

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

    def _find_sort_locator(self, timeout: int = 5000):
        """
        Try multiple candidate selectors and return the first locator that exists.
        Returns (selector_str, locator) or (None, None)
        """
        for sel in self.SORT_SELECT_CANDIDATES:
            try:
                loc = self.page.locator(sel).first
                # use a short wait to see if exists in DOM (visible not required here)
                if loc.count() > 0:
                    return sel, loc
            except Exception:
                continue
        return None, None

    def sort_by(self, option_text: str, timeout: int = 10000):
        """
        Sort products by a visible option label (e.g. "Price (low to high)").
        Robust: tries multiple selectors, fallback to value mapping, and gives diagnostic info on failure.
        """
        # ensure page loaded minimally
        try:
            self.page.wait_for_selector(self.PRODUCTS_CONTAINER, state="visible", timeout=5000)
        except TimeoutError:
            # if products container not visible, fail early
            raise TimeoutError("Products container not visible before trying to sort")

        # find a candidate selector for the sort control
        sel, locator = self._find_sort_locator(timeout=timeout//2)
        if not locator:
            # diagnostic: try to capture any element that contains 'product' and 'sort' in data-test/class
            diagnostics = []
            candidates = self.page.locator("[data-test], [class]").all()
            # to avoid heavy operations, collect a few matches that mention product/sort
            for el in candidates[:100]:
                try:
                    attrs = {}
                    # get attributes we care about
                    tag = el.evaluate("e => e.tagName")
                    dt = el.get_attribute("data-test")
                    cls = el.get_attribute("class")
                    txt = (el.text_content() or "").strip()[:200]
                    if (dt and ("product" in dt or "sort" in dt)) or (cls and ("product" in cls or "sort" in cls)):
                        diagnostics.append({"tag": tag, "data-test": dt, "class": cls, "text": txt})
                except Exception:
                    continue
            raise Exception(f"Sort control not found. Tried candidates {self.SORT_SELECT_CANDIDATES}. Diagnostics: {diagnostics}")

        # if we found a locator, try to interact
        # If it's a native <select> element, prefer select_option
        try:
            tag = locator.evaluate("e => e.tagName.toLowerCase()")
        except Exception:
            tag = None

        if tag == "select":
            # try select by label first, then by value fallback
            try:
                locator.wait_for(state="visible", timeout=timeout)
                # try label
                locator.select_option(label=option_text)
                return
            except Exception:
                # fallback to mapped value
                val = self.SORT_LABEL_TO_VALUE.get(option_text)
                if val:
                    try:
                        locator.select_option(value=val)
                        return
                    except Exception as e:
                        raise Exception(f"Failed to select by value '{val}': {e}") from e
                else:
                    raise Exception(f"Could not select label '{option_text}' and no mapped value available")
        else:
            # Not a select element: attempt to click the control and then click the option by visible text
            try:
                locator.wait_for(state="attached", timeout=timeout//2)
                locator.click()
                # options might appear as buttons or divs; try generic visible text click
                option_loc = self.page.locator(f"text={option_text}")
                if option_loc.count() > 0:
                    option_loc.first.click()
                    return
                # try value mapping: look for the mapped label or value in option text
                val = self.SORT_LABEL_TO_VALUE.get(option_text)
                if val:
                    # try options that contain the value string
                    option_loc2 = self.page.locator(f"text={val}")
                    if option_loc2.count() > 0:
                        option_loc2.first.click()
                        return
                # If we reach here, no option clicked -> diagnostic
                outer = locator.evaluate("e => e.outerHTML") if locator else "<no-locator>"
                raise Exception(f"Non-select sort control found (selector={sel}) but option '{option_text}' not clickable. Control HTML: {outer}")
            except Exception as e:
                raise Exception(f"Failed interacting with non-select sort control: {e}") from e