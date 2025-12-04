import pytest
from pages.login_page import LoginPage
from pages.products_page import ProductsPage

VALID_USER = "standard_user"
VALID_PASS = "secret_sauce"
INVALID_USER = "invalid"
INVALID_PASS = "wrong"

@pytest.mark.regression
def test_tc_1_1_valid_login(page, base_url):
    login = LoginPage(page, base_url)
    login.goto()
    login.login(VALID_USER, VALID_PASS)
    products = ProductsPage(page, base_url)
    # Validate landing on products page: check inventory container visible
    assert page.locator(".inventory_list").is_visible()
    # Alternatively verify url contains /inventory.html
    assert "/inventory.html" in page.url

@pytest.mark.regression
def test_tc_1_2_invalid_login_shows_error(page, base_url):
    login = LoginPage(page, base_url)
    login.goto()
    login.login(INVALID_USER, INVALID_PASS)
    # validate visible error message
    err = login.get_error()
    assert err is not None and "Username and password do not match" in err or "Epic sadface" in err