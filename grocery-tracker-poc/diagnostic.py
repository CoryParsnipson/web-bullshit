import inspect
import logging
from playwright.sync_api import Page

logger = logging.getLogger(__name__)


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

    webdriver_status = page.evaluate("navigator.webdriver")
    logger.info(f"({tag}) webdriver status -> navigator.webdriver == {'True' if webdriver_status else 'False'}")

    logger.warning(f"({tag}) Page load may get stuck. You may need to Ctrl+C out of this...")
    page.goto("https://bot.sannysoft.com/", timeout = 0)
    page.pause()
