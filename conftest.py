import os
import sys
import pathlib
import pytest
import allure
from playwright.sync_api import sync_playwright

# Asegurar que la raíz del proyecto esté en sys.path (importos locales)
ROOT = pathlib.Path(__file__).parent.resolve()
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

DEFAULT_BASE_URL = "https://www.saucedemo.com/"

def pytest_addoption(parser):
    parser.addoption("--base-url", action="store", default=DEFAULT_BASE_URL, help="Base URL for tests")
    parser.addoption("--browser", action="store", default="chromium", choices=["chromium","firefox","webkit"], help="Browser for tests")
    parser.addoption("--channel", action="store", default="", help="Browser channel to use (e.g. chrome, msedge). Works with chromium browser_type.")
    parser.addoption("--headed", action="store_true", default=False, help="Run browser in headed mode")
    parser.addoption("--viewport", action="store", default="1280x720", help="Viewport WxH, e.g. 1280x720")

@pytest.fixture(scope="session")
def base_url(pytestconfig):
    return pytestconfig.getoption("base_url")

@pytest.fixture(scope="session")
def browser_name(pytestconfig):
    return pytestconfig.getoption("browser")

@pytest.fixture(scope="session")
def browser_channel(pytestconfig):
    return pytestconfig.getoption("channel") or None

@pytest.fixture(scope="function")
def page(request, browser_name, browser_channel, pytestconfig):
    """
    Creates a browser, context and page for each test function.
    Supports launching a specific channel for chromium (e.g. chrome).
    """
    headed = pytestconfig.getoption("headed")
    viewport = pytestconfig.getoption("viewport")
    try:
        width, height = map(int, viewport.split("x"))
    except Exception:
        width, height = 1280, 720

    with sync_playwright() as p:
        browser_type = getattr(p, browser_name)
        launch_kwargs = {"headless": not headed}
        # If a channel is requested and we're using chromium, pass the channel
        if browser_channel and browser_name == "chromium":
            launch_kwargs["channel"] = browser_channel
        # Launch browser
        browser = browser_type.launch(**launch_kwargs)
        context = browser.new_context(viewport={"width": width, "height": height}, record_video_dir="reports/videos" if not headed else None)
        page = context.new_page()
        yield page
        # cleanup
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