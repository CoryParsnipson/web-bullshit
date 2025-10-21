from camoufox.sync_api import Camoufox
import logging
import pdb

import diagnostics

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format = "[%(levelname)s] %(message)s")


if __name__ == "__main__":
    logging.info("Hello world!")

    with Camoufox() as browser:
        page = browser.new_page()

        logging.info(f"Created new browser page...")
        logging.info(f"UserAgent = {page.evaluate('navigator.userAgent')}")
        logging.info(f"Screen offset = {page.evaluate('window.screenX')}, {page.evaluate('window.screenY')}")
        logging.info(f"Screen size = {page.evaluate('window.outerWidth')}, {page.evaluate('window.outerHeight')}")

        breakpoint()

        diagnostics.run_stealth_diagnostic(page)

        breakpoint()
