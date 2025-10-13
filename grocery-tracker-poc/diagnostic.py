import inspect
import logging
from playwright.sync_api import Page
import time

logger = logging.getLogger(__name__)

SANNYSOFT_URL = "https://bot.sannysoft.com/"
SCRAPETHISSITE_URL = "https://www.scrapethissite.com"
SCRAPETHISSITE_FORM_SANDBOX_URL = SCRAPETHISSITE_URL + "/pages/forms/"


def print_webdriver_status(page: Page):
    """
    Check the webdriver property on this page's navigator object

    :param page: playwright page object
    """
    tag = __name__ + "." + inspect.stack()[0][0].f_code.co_name

    webdriver_status = page.evaluate("navigator.webdriver")
    logger.info(f"({tag}) webdriver status -> navigator.webdriver == {'True' if webdriver_status else 'False'}")


def goto_sannysoft(page: Page):
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
    print_webdriver_status(page)

    logger.warning(f"({tag}) Page load may get stuck. You may need to Ctrl+C out of this...")
    page.goto(SANNYSOFT_URL, timeout = 0)
    page.pause()


def goto_scrapethissite_forms(page: Page):
    """
    Go to the scrape this site hockey sandbox.

    :param page: playwright page object
    """
    tag = __name__ + "." + inspect.stack()[0][0].f_code.co_name

    if not isinstance(page, Page):
        raise ValueError(
            f"({tag}) invalid page parameter. Expecting type playwright.sync_api.Page, "
            f"received {type(page)} instead"
        )

    logger.info(f"({tag}) ...")
    page.goto(SCRAPETHISSITE_FORM_SANDBOX_URL)

    print_webdriver_status(page)
