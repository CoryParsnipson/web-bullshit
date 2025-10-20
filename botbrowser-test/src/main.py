import argparse
import logging
import os
import pdb
from playwright.sync_api import Page, Playwright, sync_playwright
from playwright_stealth import Stealth

import diagnostics

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format = "[%(levelname)s] %(message)s")

parser = argparse.ArgumentParser(
    prog="Playwright Botbrowser Test",
)
parser.add_argument("-b", "--bot-profile")
parser.add_argument("-d", "--remote-debugging-port")

if __name__ == "__main__":
    args = parser.parse_args()

    with Stealth().use_sync(sync_playwright()) as p:
        logger.info("Starting playwright botbrowser test!")

        browser_executable_path = None
        if "BOTBROWSER_EXEC_PATH" in os.environ:
            browser_executable_path = os.environ["BOTBROWSER_EXEC_PATH"]

        browser_args = [
            "--no-sandbox",
            "--window-size=1920,1080"

        ]

        if args.bot_profile:
            browser_args.append(f"--bot-profile={args.bot_profile}")

        if args.remote_debugging_port:
            browser_args.append(f"--remote_debugging_port={args.remote_debugging_port}")

        logger.info(f"Browser executable path: {browser_executable_path}")
        logger.info(f"Browser args: {browser_args}")

        browser = p.chromium.launch(
            headless = False,
            channel = "chrome",
            chromium_sandbox = False,
            executable_path = browser_executable_path,
            args = browser_args,
        )

        breakpoint()

        logger.info("Loading new tab...")
        page = browser.new_page()

        diagnostics.run_stealth_diagnostic(page)

        breakpoint()
        browser.close()
