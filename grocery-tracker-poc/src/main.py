from datetime import datetime
import inspect
import logging
from playwright.sync_api import expect, Page, Playwright, sync_playwright, TimeoutError
from playwright_stealth import Stealth
import random
import time

from lib import config, diagnostic
from lib.parsers import costco_sameday, safeway

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format = "[%(levelname)s] %(message)s")


def make_browser(playwright: Playwright, launch_config = {}, browser_config = {}):
    """
    Make a playwright browser instance

    :param playwright: playwright instance
    :param launch_config: dictionary with playwright launch config parameters
    :param browser_config: dictionary with playwright browser context parameters

    :returns: tuple with browser and context
    """
    tag = __name__ + "." + inspect.stack()[0][0].f_code.co_name

    if not isinstance(playwright, Playwright):
        raise ValueError(
            f"({tag}) invalid playwright parameter. Expecting type playwright.sync_api.Playwright, "
            f"received {type(playwright)} instead"
        )

    browser = p.firefox.launch(**launch_config)

    logger.info("Creating new browser instance...")
    context = browser.new_context(**browser_config)

    return (browser, context)


def get_safeway_products(page: Page):
    tag = __name__ + "." + inspect.stack()[0][0].f_code.co_name

    if not isinstance(page, Page):
        raise ValueError(
            f"({tag}) invalid page parameter. Expecting type playwright.sync_api.Page, "
            f"received {type(page)} instead"
        )

    safeway_loc = {
        "street": "639 S Bernardo Ave",
        "zip": "94087",
    }

    safeway.navigate_to_storefront(page)
    safeway.set_location(page, safeway_loc["street"], safeway_loc["zip"])

    for url in config.PRODUCT_URLS["safeway"]:
        page_nav_delay = 10 + random.uniform(-5, 30)

        logger.info(f"({tag}) sleeping for {page_nav_delay} seconds before navigating...")
        time.sleep(page_nav_delay)

        logger.info(f"({tag}) browsing to {url} now...")
        page.goto(url)

        # extract information
        product = {
            "name": safeway.get_product_name(page),
            "sku": safeway.get_product_inventory_number(page),
            "price": safeway.get_product_price(page),
            "availability": None,
            "date": datetime.now(),
            "location": safeway_loc["street"] + ", " + safeway_loc["zip"],
        }

        logger.info(f"Extracted information for \"{product['name']}\" from {url}...")
        logger.info(f"{product}")

    logger.info("Taking screenshot...")
    page.screenshot(path="test-screenshot.no-git.png")


def get_costco_products(page: Page):
    tag = __name__ + "." + inspect.stack()[0][0].f_code.co_name

    if not isinstance(page, Page):
        raise ValueError(
            f"({tag}) invalid page parameter. Expecting type playwright.sync_api.Page, "
            f"received {type(page)} instead"
        )

    # hardcoded for now
    costco_loc = {
        "street": "Rengstorff Avenue",
        "zip": "94041"
    }

    # get to the website
    costco_sameday.navigate_to_storefront(page)

    try:
        costco_sameday.set_location(page, costco_loc["street"], costco_loc["zip"])
    except TimeoutError:
        logger.warning("set_location has timed out! This probably is fine... proceeding anyway.")

    # now go to a product
    for url in config.PRODUCT_URLS["costco"]:
        page.goto(url)

        # extract information
        product = {
            "name": costco_sameday.get_product_name(page),
            "sku": costco_sameday.get_product_inventory_number(page),
            "price": costco_sameday.get_product_price(page),
            "availability": costco_sameday.get_product_availability(page),
            "date": datetime.now(),
            "location": costco_loc["street"] + ", " + costco_loc["zip"],
        }

        logger.info(f"Extracted information for \"{product['name']}\" from {url}...")
        logger.info(f"{product}")

    logger.info("Taking screenshot...")
    page.screenshot(path="test-screenshot.no-git.png")


if __name__ == "__main__":
    with Stealth().use_sync(sync_playwright()) as p:
        browser, context = make_browser(
            playwright = p,
            launch_config = { "headless": False },
            browser_config = { "viewport": {"width": 1920, "height": 1080 } },
        )

        logger.info("Loading new tab...")
        page = context.new_page()

        diagnostic.goto_sannysoft(page)

        browser.close()
