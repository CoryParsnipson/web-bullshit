from datetime import datetime
import inspect
import logging
from playwright.sync_api import expect, Page, Playwright, sync_playwright, TimeoutError
from playwright_stealth import Stealth

from parsers import costco_sameday, safeway

# NOTE: hard code these urls for now, but real product should either crawl or
# let the user search and bookmark items
PRODUCT_URLS = {
    "costco" : [
        "https://sameday.costco.com/store/costco/products/18876359-strawberries-2-lbs-2-lb",
        "https://sameday.costco.com/store/costco/products/18848254-organic-strawberries-2",
    ],
    "safeway": [
        "https://www.safeway.com/shop/product-details.184070124.html", # 1lb prepacked strawberries
        "https://www.safeway.com/shop/product-details.960012546.html", # 2lb prepacked strawberries
        "https://www.safeway.com/shop/product-details.184700156.html", # 1lb organic strawberries
    ],
    "smart-and-final": [
        "https://www.smartandfinal.com/sm/planning/rsid/327/product/strawberries-id-00853447003390",
        "https://www.smartandfinal.com/sm/planning/rsid/327/product/organic-strawberries-id-00853447003642"
    ],
    "trader-joes": [
        "https://www.traderjoes.com/home/products/pdp/strawberries-1-lb-035878",
        "https://www.traderjoes.com/home/products/pdp/strawberries-2-lb-078515",
        "https://www.traderjoes.com/home/products/pdp/organic-strawberries-1-lb-080331",
    ],
    "whole-foods": [
        "https://www.amazon.com/Produce-ambient-room-temperature-Strawberries/dp/B08911ZP3Y?almBrandId=VUZHIFdob2xlIEZvb2Rz&fpw=alm&s=wholefoods",
        "https://www.amazon.com/Fresh-Produce-Brands-Vary-040/dp/B002B8Z98W?almBrandId=VUZHIFdob2xlIEZvb2Rz&fpw=alm&s=wholefoods",
        "https://www.amazon.com/Fresh-Produce-Brands-May-Vary/dp/B07PQNBKCK?almBrandId=VUZHIFdob2xlIEZvb2Rz&fpw=alm&s=wholefoods"
    ],
}

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


def check_sannysoft(page: Page):
    """
    Go to sannysoft diagnostic page. Also print some useful info.

    :param page: playwright page object
    """
    tag = __name__ + "." + inspect.stack()[0][0].f_code.co_name

    if not isinstance(page, Page):
        raise ValueError(
            f"({tag}) invalid page parameter. Expecting type playwright.sync_api.Page, "
            f"received {type(page)} instead"
        )

    logger.info(f"({tag}) running diagnostics...")

    webdriver_status = page.evaluate("navigator.webdriver")
    logger.info(f"({tag}) webdriver status -> navigator.webdriver == {'True' if webdriver_status else 'False'}")

    logger.warning(f"({tag}) Page load may get stuck. You may need to Ctrl+C out of this...")
    page.goto("https://bot.sannysoft.com/", timeout = 0)
    page.pause()


def get_safeway_products(page: Page):
    safeway_loc = {
        "street": "639 S Bernardo Ave",
        "zip": "94087",
    }

    safeway.navigate_to_storefront(page)
    safeway.set_location(page, safeway_loc["street"], safeway_loc["zip"])

    for url in PRODUCT_URLS["safeway"]:
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


def get_costco_products():
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
    for url in PRODUCT_URLS["costco"]:
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

        check_sannysoft(page)

        browser.close()
