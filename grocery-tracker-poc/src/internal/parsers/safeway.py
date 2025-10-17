import inspect
import logging
from patchright.sync_api import expect, Page
import re

STOREFRONT_URL="https://www.safeway.com"

logger = logging.getLogger(__name__)
extract_price_re = re.compile(r"Your Price:\s+\$(?P<price>[0-9]+\.[0-9]{2})")

def navigate_to_storefront(page, storefront_url = STOREFRONT_URL):
    """
    Navigate a playwright browser to the store front so that it is ready for
    further operations. This involves dismissing any modal pop-ups and anything
    else that must be done before reaching the index.

    :param page: valid handle to playwright.sync_api.Page to control browser
    :param storefront_url: leave blank for safeway site index

    :return: None
    """
    tag = __name__ + "." + inspect.stack()[0][0].f_code.co_name

    if not isinstance(page, Page):
        raise ValueError(
            f"({tag}) page parameter is invalid. Expecting type playwright.sync_api.Page, "
            f"instead received {type(page)}"
        )

    logger.info(f"({tag}) Browsing to {storefront_url}...")
    page.goto(storefront_url)


def set_location(page, street_address, zipcode):
    """
    Sets the location using the in-page store locator dialog.

    :param page: valid handle to playwright.sync_api.Page to control browser
    :param street_address: string of the street address to use
    :param zipcode: string of the zipcode to use

    :return: None
    """
    tag = __name__ + "." + inspect.stack()[0][0].f_code.co_name

    if not isinstance(page, Page):
        raise ValueError(
            f"({tag}) page parameter is invalid. Expecting type playwright.sync_api.Page, "
            f"instead received {type(page)}"
        )

    logger.info(f"({tag}) Setting location to {street_address + ' ' + str(zipcode)}...")

    # open address selection modal
    # NOTE: only the inner div responds to the click event and not the element
    # that has the button aria role on it...
    logger.info(f"({tag}) Opening delivery address box modal...")
    address_selector = (
        page
            .get_by_role("button")
            .filter(has=page.locator("id=openFulfillmentModalButton"))
            .locator("id=openFulfillmentModalButton")
    )
    address_selector.click()

    # fill out address form
    zipcode_input = page.get_by_placeholder("Enter ZIP Code to get started.")
    expect(zipcode_input).to_be_visible()

    zipcode_input.fill(zipcode)
    page.get_by_label("search Zipcode").click()

    #page.wait_for_load_state("networkidle")
    page.get_by_role("button").filter(has_text="Load More Stores").click()

    # find address in results
    address_results = page.locator("div.card-store.row")
    address_target = address_results.filter(has_text=street_address)
    if address_target.count() > 0:
        logger.info(f"({tag}) Found exact match! Setting address...")
        address_target.get_by_role("button", name="Select").click()
    elif address_results.count() > 0:
        logger.info(
            f"({tag}) Could not find match, using zipcode only! Setting address "
            f"to {address_results.nth(0).locator('p.body-m').nth(0).inner_text()}..."
        )
        address_results.nth(0).get_by_role("button", name="Select").click()
    else:
        raise ValueError(f"({tag}) Could not find any store locations on page!")

    logger.info(f"({tag}) Waiting for page to update with address info...")
    expect(address_selector).to_be_visible(timeout=30000)
    page.wait_for_load_state("networkidle")
    logger.info(f"({tag}) Page refresh done!")


def get_product_name(page):
    """
    Parse the product name from a product page.

    :param page: valid handle to playwright.sync_api.Page to control browser

    :return: str with product name
    """
    tag = __name__ + "." + inspect.stack()[0][0].f_code.co_name

    product_name = page.locator("div.product-info").get_by_role("heading").inner_text()
    logger.info(f"({tag}) Found product name: {product_name}")
    return product_name


def get_product_inventory_number(page):
    """
    Parse the product inventory number.

    :param page: valid handle to playwright.sync_api.Page to control browser

    :return: str with inventory number
    """
    tag = __name__ + "." + inspect.stack()[0][0].f_code.co_name

    product_inventory_number = (
        page
            .locator("div.product-info")
            .get_by_role("heading")
            .get_attribute("id")
    )
    logger.info(f"({tag}) Found product inventory number: {product_inventory_number}")
    return product_inventory_number


def get_product_price(page):
    """
    Parse the price of the product.

    :param page: valid handle to playwright.sync_api.Page to control browser

    :return: float with product price, or None if none available
    """
    tag = __name__ + "." + inspect.stack()[0][0].f_code.co_name

    try:
        product_price = page.locator("div.product-details__price-box span.sr-only").inner_text()
        product_price = float(product_price_extract.group("price"))
    except IndexError:
        raise ValueError(
            f"({tag}) Could not extract item price. Item Price not formatted as"
            f"expected! -> '" + str(product_price) + "'"
        )

    logger.info(f"({tag}) Found product price: {product_price}")
    return product_price
