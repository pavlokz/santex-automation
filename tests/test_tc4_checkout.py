import pytest
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from utils.data import checkout_examples

VALID_USER = "standard_user"
VALID_PASS = "secret_sauce"

@pytest.mark.regression
def test_tc_4_1_successful_checkout(page, base_url):
    login = LoginPage(page, base_url)
    login.goto()
    login.login(VALID_USER, VALID_PASS)
    products = ProductsPage(page, base_url)
    # Add 3 products to meet precondition
    buttons = page.locator("button", has_text="Add to cart")
    count = min(3, buttons.count())
    for i in range(count):
        buttons.nth(i).click()
    assert products.get_cart_count() == count
    products.open_cart()
    cart = CartPage(page, base_url)
    cart.click_checkout()
    # Fill checkout with first example
    checkout = CheckoutPage(page, base_url)
    first, last, zipc = checkout_examples[0]
    checkout.fill_shipping(first, last, zipc)
    # continue to overview and finish
    checkout.finish()
    assert checkout.is_order_complete()

@pytest.mark.regression
@pytest.mark.parametrize("first,last,zipc", checkout_examples)
def test_tc_4_2_checkout_with_missing_details_shows_error(page, base_url, first, last, zipc):
    """
    We'll parametrize with combinations but deliberately leave fields blank for one case.
    For the purpose of the requirement, assert validation when fields missing.
    """
    login = LoginPage(page, base_url)
    login.goto()
    login.login(VALID_USER, VALID_PASS)
    products = ProductsPage(page, base_url)
    products.add_first_product()
    products.open_cart()
    cart = CartPage(page, base_url)
    cart.click_checkout()
    checkout = CheckoutPage(page, base_url)
    # For one scenario, pass empty first name to validate error
    if first == "":
        checkout.fill_shipping(first, last, zipc)
        err = checkout.get_error()
        assert err != ""
    else:
        # normal flow: fill and continue, expect no error
        checkout.fill_shipping(first, last, zipc)
        err = checkout.get_error()
        assert err == "" or err is None