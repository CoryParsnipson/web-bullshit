import inspect
import logging
import playwright
from playwright.sync_api import expect
import re

DEFAULT_ZIPCODE = "94041"
STOREFRONT_URL = "https://sameday.costco.com"

logger = logging.getLogger(__name__)
extract_price_re = re.compile(r"Current price:\s+\$(?P<price>[0-9]+\.[0-9]{2})")

def navigate_to_storefront(page, storefront_url = STOREFRONT_URL):
    """
    Navigate a playwright browser to the store front so that it is ready for
    further operations. This involves dismissing any modal pop-ups and anything
    else that must be done before reaching the index.

    :param page: valid handle to playwright.sync_api.Page to control browser
    :param storefront_url: leave blank for costco sameday index

    :return: None
    """
    tag = __name__ + "." + inspect.stack()[0][0].f_code.co_name

    if not isinstance(page, playwright.sync_api.Page):
        raise ValueError(
            f"({tag}) page parameter is invalid. Expecting type playwright.sync_api.Page, "
            f"instead received {type(page)}"
        )

    logger.info(f"({tag}) Browsing to {storefront_url}...")
    page.goto(storefront_url)

    # if this is a completely new user, costco may show an address select
    # box before sending you to a storefront
    if page.get_by_placeholder("Enter ZIP Code").is_visible():
        logger.info(f"({tag}) Zip code landing page detected...")
        page.get_by_placeholder("Enter ZIP Code").fill(DEFAULT_ZIPCODE)

        submit_btn = page.get_by_role("button").filter(has_text="Start Shopping")
        if submit_btn.is_visible():
            logger.info(f"({tag}) Clicking through zip code landing page...")
            submit_btn.click()

        page.wait_for_load_state("networkidle")

    # dismiss modal notification if present
    modal_notification = page.get_by_role("button").filter(has_text="Start Shopping")
    if modal_notification.is_visible():
        logger.info(f"({tag}) TOS modal detected. Dismissing modal...")
        modal_notification.click()


def set_location(page, street_address, zipcode):
    """
    Sets the location using the in-page store locator dialog.

    :param page: valid handle to playwright.sync_api.Page to control browser
    :param street_address: string of the street address to use
    :param zipcode: string of the zipcode to use

    :return: None
    """
    tag = __name__ + "." + inspect.stack()[0][0].f_code.co_name

    if not isinstance(page, playwright.sync_api.Page):
        raise ValueError(
            f"({tag}) page parameter is invalid. Expecting type playwright.sync_api.Page, "
            f"instead received {type(page)}"
        )

    logger.info(f"({tag}) Setting location to {street_address + ' ' + zipcode}...")

    logger.info(f"({tag}) Waiting for delivery address box to load...")
    expect(page.get_by_role("button").filter(has_text="Delivery")).to_be_visible(timeout=30000)

    set_address_modal = page.get_by_role("button").filter(has_text="Delivery")
    expect(set_address_modal).to_be_enabled()
    logger.info(f"({tag}) Opening delivery address box modal...")
    set_address_modal.click()

    logger.info(f"({tag}) Filling out street address for " + street_address)
    page.get_by_role("button").filter(has_text="Edit").click()
    page.locator("id=streetAddress").fill(street_address + ", " + zipcode)
    page.locator("id=address-suggestion-list_0").get_by_role("button").click()

    address_submit_btn = page.get_by_role("button").filter(has_text="Save Address")
    expect(address_submit_btn).to_be_enabled()
    logger.info(f"({tag}) Saving address...")
    address_submit_btn.click()

    logger.info(f"({tag}) Waiting for page to update with address info...")
    page.wait_for_load_state("networkidle")
    logger.info(f"({tag}) Page refresh done!")


def get_product_name(page):
    """
    Parse the product name from a product page.

    :param page: valid handle to playwright.sync_api.Page to control browser

    :return: str with product name
    """
    tag = __name__ + "." + inspect.stack()[0][0].f_code.co_name

    content = page.locator("id=item_details").locator("div").nth(1)
    product_name = content.locator("h1").inner_text()
    logger.info(f"({tag}) Found product name: {product_name}")
    return product_name


def get_product_inventory_number(page):
    """
    Parse the product inventory number.

    :param page: valid handle to playwright.sync_api.Page to control browser

    :return: str with inventory number
    """
    tag = __name__ + "." + inspect.stack()[0][0].f_code.co_name

    content = page.locator("id=item_details").locator("div").nth(1)
    product_inventory_number = content \
        .locator("div:text('Item:')") \
        .inner_text() \
        .replace("Item: ", "") \

    logger.info(f"({tag}) Found product inventory number: {product_inventory_number}")
    return product_inventory_number


def get_product_price(page):
    """
    Parse the price of the product.

    :param page: valid handle to playwright.sync_api.Page to control browser

    :return: float with product price, or None if none available
    """
    tag = __name__ + "." + inspect.stack()[0][0].f_code.co_name

    content = page.locator("id=item_details").locator("div").nth(1)

    if not (
        content
            .locator("span:not(.screen-reader-only)")
            .filter(has_text="Current price")
            .is_visible()
    ):
        logger.info(f"({tag}) No pricing data on this page!")
        return None

    product_price = (
        content
            .locator("span:not(.screen-reader-only)")
            .filter(has_text="Current price")
            .inner_text()
    )

    try:
        product_price_extract = extract_price_re.search(product_price)
        product_price = float(product_price_extract.group("price"))
    except IndexError:
        raise ValueError(
            f"({tag}) Could not extract item price. Item Price not formatted as"
            f"expected! -> '" + str(product_price) + "'"
        )

    logger.info(f"({tag}) Found product price: {product_price}")
    return product_price


def get_product_availability(page):
    """
    Parse any product availability messages, if exists.

    :param page: valid handle to playwright.sync_api.Page to control browser

    :return: str with availability string, or None if doesn't exist
    """
    tag = __name__ + "." + inspect.stack()[0][0].f_code.co_name

    product_availability = None
    content = page.locator("id=item_details").locator("div").nth(1)
    if content.filter(has_text="Out of stock").count() > 0:
        # selecting random gibberish class, but it seems to be the easiest way for now...
        product_availability = content.locator("div.e-i9gxme").inner_text()
    elif content.locator("div.e-pftdsf").count() > 0:
        product_availability = content.locator("div.e-pftdsf").inner_text()

    if product_availability != None:
        logger.info(f"({tag}) Found product availability: '{product_availability}'")
    else:
        logger.info(f"({tag}) Product availability information not available...")

    return product_availability
