import inspect
import logging
import os
from patchright.sync_api import Page, Playwright
import subprocess

from .config import *

logger = logging.getLogger(__name__)


def make_browser(playwright: Playwright, launch_config = {}, browser_config = {}):
    """
    Make a playwright browser instance

    :param playwright: playwright instance
    :param launch_config: dictionary with playwright launch config parameters
    :param browser_config: dictionary with playwright browser context parameters

    :returns: tuple with browser and context
    """
    tag = __name__ + "." + inspect.stack()[0][0].f_code.co_name

    if not isinstance(playwright, Playwright):
        raise ValueError(
            f"({tag}) invalid playwright parameter. Expecting type playwright.sync_api.Playwright, "
            f"received {type(playwright)} instead"
        )

    if "BROWSER" in os.environ and os.environ["BROWSER"] == "chromium":
        browser = playwright.chromium.launch_persistent_context(**launch_config)
    else:
        browser = playwright.firefox.launch(**launch_config)

    logger.info("Creating new browser instance...")
    #context = browser.new_context(**browser_config)
    context = None

    return (browser, context)


def should_pause_at_beginning():
    if pause_at_beginning() == None:
        if environment() == "dev" and in_docker():
            return True
        else:
            return False
    elif pause_at_beginning() == False:
        return False
    else:
        return True


def pause_page(page: Page):
    """
    Wraps playwright function, to close debug window afterwards
    """
    tag = __name__ + "." + inspect.stack()[0][0].f_code.co_name

    if not isinstance(page, Page):
        raise ValueError(
            f"({tag}) invalid page parameter. Expecting type playwright.sync_api.Page, "
            f"received {type(page)} instead"
        )

    logger.info(f"({tag}) Pausing playwright...")
    page.pause()

    if in_docker():
        # need to automatically close debug window bc in docker we don't have
        # a window manager that we can use manually
        subprocess.run("xdotool search --name playwright | xargs xdotool windowclose", shell=True)
