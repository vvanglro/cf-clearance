# -*- coding: utf-8 -*-
import asyncio

from playwright.async_api import async_playwright

from cf_clearance import async_retry, stealth_async


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, proxy={"server": "socks5://localhost:7890"}, args=[
            "--disable-gpu",
            '--no-sandbox',
            '--disable-dev-shm-usage',
            '--no-first-run',
            '--no-service-autorun',
            '--no-default-browser-check',
            '--password-store=basic',
            '--start-maximized',
        ])
        content = await browser.new_context(no_viewport=True)
        page = await content.new_page()
        await stealth_async(page)
        await page.goto('https://nowsecure.nl')
        res = await async_retry(page)
        if res:
            cppkies = await page.context.cookies()
            for cookie in cppkies:
                if cookie.get('name') == 'cf_clearance':
                    print(cookie.get('value'))
            ua = await page.evaluate('() => {return navigator.userAgent}')
            print(ua)
        else:
            print("获取失败")
        await browser.close()


asyncio.get_event_loop().run_until_complete(main())
