#!/bin/python

import asyncio
import inspect
import zendriver as zd
import logging
import pdb
import re

FINGERPRINT_SCAN_URL = "https://fingerprint-scan.com/"
COVER_YOUR_TRACKS_URL = "https://coveryourtracks.eff.org/"

ENTROPY_WARNING_THRESHOLD = 1000

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format = "[%(levelname)s] %(message)s")

# there seems to be an issue in the nodriver code right now where running
# query_selector, or select, or wait_for will not respect timeout and throw
# a ProtocolException if the element does not exist, and the wrapper functions
# do not catch this error.
async def wait_for(page, selector = "", text = "", timeout = 10):
    """
    Custom wait_for that wraps nodrivers to fix issue
    """
    loop = asyncio.get_running_loop()
    start_time = loop.time()

    try:
        item = await page.wait_for(selector, text, timeout)
    except zd.core.connection.ProtocolException:
        item = None

    while not item:
        try:
            item = await page.wait_for(selector, text, timeout)
        except zd.core.connection.ProtocolException:
            pass

        if loop.time() - start_time > timeout:
            return item
        await asyncio.sleep(0.5)
    return item


async def run_diagnostics(browser: zd.Browser, quiet = True):
    """
    Run all diagnostic tests in a row.
    """
    tag = __name__ + "." + inspect.stack()[0][0].f_code.co_name

    logger.info(f"({tag}) Running diagnostics...")

    score = await get_fingerprint_score(browser, quiet)
    logger.info(f"({tag}) fingerprint Score => {score}")

    entropy = await check_entropy(browser, quiet)
    if entropy == 1.0:
        logger.info(f"({tag}) entropy => unique fingerprint detected...")
    else:
        logger.info(f"({tag}) entropy => {entropy}")

    logger.info(f"({tag}) Test complete.")


async def get_fingerprint_score(browser: zd.Browser, quiet = False):
    """
    Returns the fingerprint score as an integer between 0 and 100
    """
    tag = __name__ + "." + inspect.stack()[0][0].f_code.co_name

    page = await browser.get(FINGERPRINT_SCAN_URL)

    # print out some generic bot test results and fingerprint id
    if not quiet:
        await wait_for(page, "#fingerprintHash", timeout = 30)
        fingerprint_hash_element = await page.select("#fingerprintHash")

        fingerprint_hash_text = fingerprint_hash_element.text_all

        fingerprint_match = re.match(r"Fingerprint ID:\s+(?P<fingerprint>.*)$", fingerprint_hash_text)
        if "fingerprint" in fingerprint_match.groupdict():
            fingerprint_hash = fingerprint_match.groupdict()["fingerprint"]
        else:
            fingerprint_hash = "not found"

        logger.info(f"({tag}) fingerprint hash: {fingerprint_hash}")

        info_table = await page.find("table#fingerprintTable")
        rows = await info_table.query_selector_all("tr")

        found_header = False
        for row in rows:
            if not found_header:
                header = re.search(r"Generic Bot Tests", row.text_all)
                if header:
                    found_header = True

                continue

            end_header = await row.query_selector(".group-separator")
            if found_header and end_header:
                break

            # if we are down here, we are seeing a row we are interested in
            name = await row.query_selector(".property-name")
            result = await row.query_selector(".property-value")

            logger.info(f"({tag}) {name.text_all} - {result.text_all}")

    score_element = await page.select("#fingerprintScore")
    score_match = re.match(r"Bot Risk Score:\s+(?P<score>[0-9]+)", score_element.text_all)
    score = int(score_match.groupdict()["score"]) if "score" in score_match.groupdict() else None

    if not quiet:
        logger.info(f"({tag}) fingerprint score: {score if score != None else 'inconclusive'}")

    return score


async def check_entropy(browser: zd.Browser, quiet = False):
    """
    Get browser fingerprinting stats.
    """
    tag = __name__ + "." + inspect.stack()[0][0].f_code.co_name

    page = await browser.get(COVER_YOUR_TRACKS_URL)

    test_button = await page.select("a#kcarterlink", timeout = 30)

    logger.info(f"({tag}) starting browser test...")

    # click through to start the test
    await test_button.click()

    # wait for results to become available
    await wait_for(page, "#fp_status > span", timeout = 30)
    await wait_for(page, "#ad_status > span", timeout = 30)
    await wait_for(page, "#tracker_status > span", timeout = 30)

    # get assessment summary
    assessment = await page.query_selector("#fp_status > span")
    logger.info(f"({tag}) Assessment => {assessment.text_all}")

    adblock_status = await page.query_selector("#ad_status")
    logger.info(f"({tag}) Blocking tracking ads? => {adblock_status.text_all}")

    tracker_block_status = await page.query_selector("#tracker_status")
    logger.info(f"({tag}) Blocking invisible trackers? => {tracker_block_status.text_all}")

    # check entropy values
    results_table = await page.query_selector("div.detailed-results")
    detailed_results = await results_table.query_selector_all(".results-table")

    for row in detailed_results:
        header = await row.query_selector("h4")

        description = await row.query_selector(".default")
        description = description.text_all
        if len(description) >= 100:
            description = description[0:97] + "..."

        entropy = await row.query_selector(".detailed:last-child > em")
        entropy = float(entropy.text_all)

        if not quiet:
            if entropy >= ENTROPY_WARNING_THRESHOLD:
                entropy_msg = str(entropy) + "**"
            else:
                entropy_msg = str(entropy)

            logger.info(f"({tag}) {header.text_all} ({entropy_msg}) => {description}")

        if quiet and entropy >= ENTROPY_WARNING_THRESHOLD:
            logger.warning(f"({tag}) LOW ENTROPY DETECTED FOR {header.text_all}! ({entropy}) => {description}")

    overall_entropy = await page.select("div.entropy")
    results = re.search(r"one in (?P<uniqueness>[0-9]*?(\.[0-9]+)?) browsers", overall_entropy.text_all)
    if results and "uniqueness" in results.groupdict():
        entropy = float(results.groupdict()["uniqueness"])
    else:
        entropy = 1.0

    if not quiet:
        logger.info(f"({tag}) entropy => {entropy}")

    return entropy


async def main():
    browser = await zd.start(
        headless = False,
        sandbox = False,
        user_data_dir = "chrome_data",
        browser_args = [ "--start-maximized", "--window-size=1920,1080" ],
    )

    await run_diagnostics(browser)
    breakpoint()
    await browser.stop()


if __name__ == "__main__":
    asyncio.run(main())
