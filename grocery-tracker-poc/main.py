from datetime import datetime
import logging
from playwright.sync_api import expect, sync_playwright

from parsers import costco_sameday

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

if __name__ == "__main__":
    with sync_playwright() as p:
        # TODO: remove headless setting
        browser = p.firefox.launch(headless = False)

        logger.info("Creating new browser instance...")
        context = browser.new_context(viewport = {'width': 1920, 'height': 1080})

        logger.info("Loading new tab...")
        page = context.new_page()

        # hardcoded for now
        costco_loc = {
            "street": "Rengstorff Avenue",
            "zip": "94041"
        }

        # get to the website
        costco_sameday.navigate_to_storefront(page)
        costco_sameday.set_location(page, costco_loc["street"], costco_loc["zip"])

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
                "location": costco_loc["street"] + ", " + costco_loc["zip"]
            }

            logger.info(f"Extracted information for \"{product['name']}\" from {PRODUCT_URLS['costco'][0]}...")
            logger.info(f"{product}")

        logger.info("Taking screenshot...")
        page.screenshot(path="test-screenshot.no-git.png")

        browser.close()
