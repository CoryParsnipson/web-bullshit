import inspect
import logging
from patchright.sync_api import expect, Page
import re
import time

from .common import pause_page

logger = logging.getLogger(__name__)

SCRAPFLY_JA3_URL = "https://scrapfly.io/web-scraping-tools/ja3-fingerprint"
JA3ZONE_URL = "https://ja3.zone/check"
FINGERPRINT_SCAN_URL = "https://fingerprint-scan.com/"
COVER_YOUR_TRACKS_URL = "https://coveryourtracks.eff.org/"
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


def check_scrapfly_ja3(page: Page):
    """
    Check if this passes the JA3 TLS handshake.
    """
    tag = __name__ + "." + inspect.stack()[0][0].f_code.co_name

    if not isinstance(page, Page):
        raise ValueError(
            f"({tag}) invalid page parameter. Expecting type playwright.sync_api.Page, "
            f"received {type(page)} instead"
        )

    logger.info(f"({tag}) checking JA3 fingerprint from Scrapfly...")
    page.goto(SCRAPFLY_JA3_URL)
    pause_page(page)


def check_ja3zone_ja3(page: Page):
    """
    Check if this passes the JA3 TLS handshake.
    """
    tag = __name__ + "." + inspect.stack()[0][0].f_code.co_name

    if not isinstance(page, Page):
        raise ValueError(
            f"({tag}) invalid page parameter. Expecting type playwright.sync_api.Page, "
            f"received {type(page)} instead"
        )

    logger.info(f"({tag}) checking JA3 fingerprint from JA3 zone...")
    page.goto(JA3ZONE_URL)
    pause_page(page)


def check_fingerprint_score(page: Page):
    """
    Go to fingerprint score calculator tool.
    """
    tag = __name__ + "." + inspect.stack()[0][0].f_code.co_name

    if not isinstance(page, Page):
        raise ValueError(
            f"({tag}) invalid page parameter. Expecting type playwright.sync_api.Page, "
            f"received {type(page)} instead"
        )

    logger.info(f"({tag}) trying fingerprint score...")
    page.goto(FINGERPRINT_SCAN_URL)

    risk_score = None
    if page.locator("id=fingerprintScore").count() == 0:
        logger.info(f"({tag}) finger print score inconclusive...")
    else:
        risk_score = page.locator("id=fingerprintScore").inner_text()
        match = re.search(r"Bot Risk Score: (?P<score_numer>[0-9]+)\/(?P<score_denom>[0-9]+)", risk_score)
        risk_score = float(match.group["score_numer"]) / float(match.group["score_denom"]) * 100

        logger.info(f"({tag}) Fingerprint score obtained (higher is more risk): {risk_score}")

    pause_page(page)
    return risk_score


def check_entropy(page: Page):
    """
    Go to diagnostic tool for browser fingerprinting uniqueness score.
    """
    tag = __name__ + "." + inspect.stack()[0][0].f_code.co_name

    if not isinstance(page, Page):
        raise ValueError(
            f"({tag}) invalid page parameter. Expecting type playwright.sync_api.Page, "
            f"received {type(page)} instead"
        )

    logger.info(f"({tag}) going to Cover Your Tracks fingerprint diagnostic.")
    page.goto(COVER_YOUR_TRACKS_URL)

    page.get_by_role("link", name="Test Your Browser").click()

    # wait for ajax request to update page
    expect(page.locator("id=fp_status")).to_be_visible(timeout=60000)
    expect(page.locator("id=fp_status")).not_to_be_empty(timeout=30000)

    logger.info(f"({tag}) *** RESULTS ***")

    for result in page.locator(".results-table").filter(has=page.locator("h4")).all():
        header = result.locator("h4").inner_text()
        item_name = result.locator("div.default").inner_text()
        uniqueness = result.locator("div").filter(has_text="browsers have this value").inner_text()

        if len(item_name) > 100:
            item_name = item_name[0:97] + "..."

        match = re.search(r"value: (?P<odds>[0-9]+(\.[0-9]+)?)", uniqueness)
        if "odds" in match.groupdict():
            uniqueness = float(match.groupdict()["odds"])

        logger.info(f"({tag}) === {header} ({uniqueness})")
        logger.info(f"({tag})   {item_name}")

    logger.info(f"({tag}) *** OVERALL ASSESSMENT ***")

    status = page.locator("id=fp_status").inner_text()
    logger.info(f"({tag}) {status}")

    overall_uniqueness = page.locator("div.entropy").locator("p").nth(0).inner_text().replace("\r\n", "")
    logger.info(f"({tag}) {overall_uniqueness}")

    match = re.search(r"one in (?P<uniqueness>[0-9]*?(\.[0-9]+)?) browsers", overall_uniqueness)
    return float(match.groupdict()["uniqueness"]) if "uniqueness" in match.groupdict() else 1.0


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
    print_webdriver_status(page)

    logger.warning(f"({tag}) Page load may get stuck. You may need to Ctrl+C out of this...")
    page.goto(SANNYSOFT_URL, timeout = 0)
    pause_page(page)


def check_scrapethissite_forms(page: Page):
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
