import pytest
from pages.login_page import LoginPage
from pages.products_page import ProductsPage

VALID_USER = "standard_user"
VALID_PASS = "secret_sauce"

@pytest.mark.regression
def test_tc_5_1_sort_products_by_price_low_to_high(page, base_url):
    login = LoginPage(page, base_url)
    login.goto()
    login.login(VALID_USER, VALID_PASS)
    products = ProductsPage(page, base_url)
    # ensure products loaded
    assert products.is_loaded()
    products.sort_by("Price (low to high)")
    # collect prices and verify ascending
    prices = []
    for item in page.locator(".inventory_item").all():
        price_text = item.locator(".inventory_item_price").text_content().strip().replace("$", "")
        try:
            prices.append(float(price_text))
        except Exception:
            pass
    assert prices == sorted(prices)