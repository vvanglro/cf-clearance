# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright

from cf_clearance import sync_retry, stealth_sync


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, proxy={"server": "socks5://localhost:7890"}, args=[
            "--disable-gpu",
            '--no-sandbox',
            '--disable-dev-shm-usage',
            '--no-first-run',
            '--no-service-autorun',
            '--no-default-browser-check',
            '--password-store=basic',
            '--start-maximized',
        ])
        content = browser.new_context(no_viewport=True)
        page = content.new_page()
        stealth_sync(page)
        page.goto('https://nowsecure.nl')
        res = sync_retry(page)
        if res:
            cppkies = page.context.cookies()
            for cookie in cppkies:
                if cookie.get('name') == 'cf_clearance':
                    print(cookie.get('value'))
            ua = page.evaluate('() => {return navigator.userAgent}')
            print(ua)
        else:
            print("获取失败")
        browser.close()


main()
