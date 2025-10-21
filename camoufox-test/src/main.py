from camoufox.sync_api import Camoufox
import logging
import pdb

import diagnostics

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format = "[%(levelname)s] %(message)s")


if __name__ == "__main__":
    logging.info("Hello world!")
    breakpoint()

    with Camoufox() as browser:
        page = browser.new_page()
        diagnostics.run_stealth_diagnostic(page)

        breakpoint()
