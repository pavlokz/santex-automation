import pytest
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.cart_page import CartPage

VALID_USER = "standard_user"
VALID_PASS = "secret_sauce"

@pytest.mark.regression
def test_tc_3_1_remove_product_from_cart(page, base_url):
    login = LoginPage(page, base_url)
    login.goto()
    login.login(VALID_USER, VALID_PASS)
    products = ProductsPage(page, base_url)
    # ensure at least one product in cart
    products.add_first_product()
    assert products.get_cart_count() >= 1
    products.open_cart()
    cart = CartPage(page, base_url)
    assert cart.is_loaded()
    items_before = cart.get_items()
    assert len(items_before) >= 1
    # remove first item
    cart.remove_product_by_name(items_before[0])
    # validate removed (cart badge updates or cart items decrease)
    page.wait_for_timeout(500)
    items_after = cart.get_items()
    assert len(items_after) == max(0, len(items_before) - 1)