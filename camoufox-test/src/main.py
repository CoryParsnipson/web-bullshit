from camoufox.sync_api import Camoufox
import logging
import pdb

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format = "[%(levelname)s] %(message)s")


if __name__ == "__main__":
    logging.info("Hello world!")
    breakpoint()

    with Camoufox() as browser:
        page = browser.new_page()
        page.goto("https://www.browserscan.net/bot-detection")

        breakpoint()
