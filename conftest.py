import os
import pytest
import allure
from playwright.sync_api import sync_playwright

DEFAULT_BASE_URL = "https://www.saucedemo.com/"

def pytest_addoption(parser):
    parser.addoption("--base-url", action="store", default=DEFAULT_BASE_URL, help="Base URL for tests")
    parser.addoption("--browser", action="store", default="chromium", choices=["chromium","firefox","webkit"], help="Browser for tests")
    parser.addoption("--headed", action="store_true", default=False, help="Run browser in headed mode")
    parser.addoption("--viewport", action="store", default="1280x720", help="Viewport WxH, e.g. 1280x720")

@pytest.fixture(scope="session")
def base_url(pytestconfig):
    return pytestconfig.getoption("base_url")

@pytest.fixture(scope="session")
def browser_name(pytestconfig):
    return pytestconfig.getoption("browser")

@pytest.fixture(scope="function")
def page(request, browser_name, pytestconfig):
    """
    Creates a browser, context and page for each test function.
    Records screenshots on failure via pytest hook.
    """
    headed = pytestconfig.getoption("headed")
    viewport = pytestconfig.getoption("viewport")
    try:
        width, height = map(int, viewport.split("x"))
    except Exception:
        width, height = 1280, 720

    with sync_playwright() as p:
        browser_type = getattr(p, browser_name)
        browser = browser_type.launch(headless=not headed)
        context = browser.new_context(viewport={"width": width, "height": height}, record_video_dir="reports/videos" if not headed else None)
        page = context.new_page()
        yield page
        context.close()
        browser.close()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    On test failure, capture a screenshot and attach to Allure (if present).
    """
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        page = item.funcargs.get("page", None)
        if page:
            screenshots_dir = os.path.join(os.getcwd(), "reports", "screenshots")
            os.makedirs(screenshots_dir, exist_ok=True)
            safe_name = item.name.replace("/", "_").replace(":", "_")
            path = os.path.join(screenshots_dir, f"{safe_name}.png")
            try:
                page.screenshot(path=path, full_page=True)
                # attach to allure if available
                try:
                    with open(path, "rb") as f:
                        allure.attach(f.read(), name=f"{safe_name}.png", attachment_type=allure.attachment_type.PNG)
                except Exception:
                    pass
            except Exception:
                pass