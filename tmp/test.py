import logging
from playwright.sync_api import expect, sync_playwright
import re

ZIP_CODE = "94041"
STREET_ADDRESS = "Rengstorff Avenue"
WEBSITE="https://sameday.costco.com"

STRAWBERRIES_2LBS_URL = "https://sameday.costco.com/store/costco/products/18876359-strawberries-2-lbs-2-lb"
STRAWBERRIES_2LBS_ORGANIC_URL = "https://sameday.costco.com/store/costco/products/18848254-organic-strawberries-2-lbs-2-lb"

WATERMELON_SEEDLESS_WHOLE_URL = "https://sameday.costco.com/store/costco/products/18848208-seedless-watermelon-each"

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format = "[%(levelname)s] %(message)s")

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.firefox.launch(headless = False)

        logger.info("Creating new browser instance...")
        context = browser.new_context(viewport = {'width': 1920, 'height': 1080})

        logger.info("Loading new tab...")
        page = context.new_page()

        # try to pull something off the costco delivery website
        logger.info("Browsing to " + WEBSITE + "...")
        page.goto(WEBSITE)

        # if this is a completely new user, costco may show an address select
        # box before sending you to a storefront
        if page.get_by_placeholder("Enter ZIP Code").is_visible():
            logger.info("Zip code landing page detected...")
            page.get_by_placeholder("Enter ZIP Code").fill(ZIP_CODE)

            submit_btn = page.get_by_role("button").filter(has_text="Start Shopping")
            if submit_btn.is_visible():
                logger.info("Clicking through zip code landing page...")
                submit_btn.click()

            page.wait_for_load_state("networkidle")

        # dismiss modal notification if present
        modal_notification = page.get_by_role("button").filter(has_text="Start Shopping")
        if modal_notification.is_visible():
            logger.info("TOS modal detected. Dismissing modal...")
            modal_notification.click()

        page.wait_for_load_state("networkidle")

        # set location
        logger.info("Waiting for delivery address box to load...")
        expect(page.get_by_role("button").filter(has_text="Delivery")).to_be_visible(timeout=30000)
        set_address_modal = page.get_by_role("button").filter(has_text="Delivery")
        expect(set_address_modal).to_be_enabled()
        logger.info("Opening delivery address box modal...")
        set_address_modal.click()

        logger.info("Filling out street address for " + STREET_ADDRESS)
        page.get_by_role("button").filter(has_text="Edit").click()
        page.locator("id=streetAddress").fill(STREET_ADDRESS + ", " + ZIP_CODE)
        page.locator("id=address-suggestion-list_0").get_by_role("button").click()

        address_submit_btn = page.get_by_role("button").filter(has_text="Save Address")
        expect(address_submit_btn).to_be_enabled()
        logger.info("Saving address...")
        address_submit_btn.click()

        logger.info("Waiting for page to update with address info...")
        page.wait_for_load_state("networkidle")
        logger.info("Page refresh done!")

        # go directly to strawberries page (now that location is set)
        #logger.info("Browsing to " + STRAWBERRIES_2LBS_URL + "...")
        #page.goto(STRAWBERRIES_2LBS_URL)

        logger.info("Browsing to " + WATERMELON_SEEDLESS_WHOLE_URL + "...")
        page.goto(WATERMELON_SEEDLESS_WHOLE_URL)

        # this selects the first grid div in the item details to exclude the
        # "you may also like" product carosel underneath. All these divs are
        # not labeled with human readable attributes...
        content = page.locator("id=item_details").locator("div").nth(1)

        # scrape data
        item_name = content.locator("h1").inner_text()
        logger.info("Obtained item name: '" + item_name + "'")

        item_num = content.locator("div:text('Item:')").inner_text()
        item_num = item_num.replace("Item: ", "")
        logger.info("Obtained item number: " + item_num)

        item_price = content.locator("span:not(.screen-reader-only)").filter(has_text="Current price").inner_text()

        try:
            item_price_extract = re.search(r"Current price:\s+\$(?P<price>[0-9]+\.[0-9]{2})", item_price)
            item_price = float(item_price_extract.group("price"))
        except IndexError:
            logger.info("Could not extract item price. Item Price not formatted as expected! -> '" + str(item_price) + "'")

        logger.info("Obtained item price: " + str(item_price))

        # selecting random gibberish class, but it seems to be the easiest way for now...
        if content.locator("div.e-pftdsf").count() > 0:
            item_status = content.locator("div.e-pftdsf").inner_text()
            logger.info("Obtained item stock status: " + item_status)
        else:
            logger.info("Item stock information not available")

        browser.close()
