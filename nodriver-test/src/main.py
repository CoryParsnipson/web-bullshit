#!/bin/python

import asyncio
import nodriver as uc
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format = "[%(levelname)s] %(message)s")

async def main():
    browser = await uc.start(
        headless = False,
        sandbox = False,
        user_data_dir = "chrome_data",
        browser_args = [ "--start-maximized", "--window-size=1920,1080" ],
    )
    page = await browser.get("https://www.nowsecure.nl")

    await asyncio.sleep(300)


if __name__ == "__main__":
    uc.loop().run_until_complete(main())
