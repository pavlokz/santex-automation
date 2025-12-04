import pytest
from pages.login_page import LoginPage
from pages.products_page import ProductsPage

VALID_USER = "standard_user"
VALID_PASS = "secret_sauce"

@pytest.mark.regression
def test_tc_6_1_logout(page, base_url):
    login = LoginPage(page, base_url)
    login.goto()
    login.login(VALID_USER, VALID_PASS)
    products = ProductsPage(page, base_url)
    assert products.is_loaded()
    products.logout()
    # after logout should be at login page
    assert "/index.html" in page.url or page.locator("input#login-button").is_visible()