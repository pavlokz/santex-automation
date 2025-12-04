import pytest
from pages.login_page import LoginPage
from pages.products_page import ProductsPage

VALID_USER = "standard_user"
VALID_PASS = "secret_sauce"

@pytest.mark.regression
def test_tc_2_1_add_single_product_to_cart(page, base_url):
    login = LoginPage(page, base_url)
    login.goto()
    login.login(VALID_USER, VALID_PASS)
    products = ProductsPage(page, base_url)
    assert products.is_loaded()
    products.add_first_product()
    assert products.get_cart_count() == 1
    products.open_cart()
    assert "/cart.html" in page.url
    assert page.locator(".cart_item").count() == 1

@pytest.mark.regression
def test_tc_2_2_add_multiple_products_to_cart(page, base_url):
    login = LoginPage(page, base_url)
    login.goto()
    login.login(VALID_USER, VALID_PASS)
    products = ProductsPage(page, base_url)
    assert products.is_loaded()
    # add 3 distinct products by clicking first 3 add buttons
    buttons = page.locator("button", has_text="Add to cart")
    count = min(3, buttons.count())
    for i in range(count):
        buttons.nth(i).click()
    assert products.get_cart_count() == count
    products.open_cart()
    assert page.locator(".cart_item").count() == count