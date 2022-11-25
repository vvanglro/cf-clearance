# -*- coding: utf-8 -*-
import asyncio
import logging

from playwright.async_api import async_playwright

from cf_clearance import async_cf_retry, async_stealth
from tests.test_common import (
    test_add_ua_cookie_cf_success,
    test_not_pass_cf_challenge_request,
)


async def test_cf_challenge():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            proxy={"server": "socks5://localhost:7890"},
            args=[
                "--disable-gpu",
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--no-first-run",
                "--no-service-autorun",
                "--no-default-browser-check",
                "--password-store=basic",
                "--start-maximized",
            ],
        )
        content = await browser.new_context(no_viewport=True)
        page = await content.new_page()
        await async_stealth(page, pure=True)
        await page.goto("https://nowsecure.nl")
        res = await async_cf_retry(page)
        ua = None
        cf_clearance_value = None
        if res:
            cookies = await page.context.cookies()
            for cookie in cookies:
                if cookie.get("name") == "cf_clearance":
                    cf_clearance_value = cookie.get("value")
            ua = await page.evaluate("() => {return navigator.userAgent}")
        else:
            logging.info("cf challenge fail")
        await browser.close()
        return ua, cf_clearance_value


async def main():
    logging.basicConfig(level=logging.INFO)
    test_not_pass_cf_challenge_request()
    ua, cf_clearance_value = await test_cf_challenge()
    test_add_ua_cookie_cf_success(ua, cf_clearance_value)


asyncio.get_event_loop().run_until_complete(main())
