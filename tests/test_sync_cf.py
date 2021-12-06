# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright

from cf_clearance import sync_retry, stealth_sync
from tests.test_common import test_not_pass_cf_challenge_request, test_add_ua_cookie_cf_success


def test_cf_challenge():
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
            cookies = page.context.cookies()
            for cookie in cookies:
                if cookie.get('name') == 'cf_clearance':
                    cf_clearance_value = cookie.get('value')
                    print(cf_clearance_value)
            ua = page.evaluate('() => {return navigator.userAgent}')
            print(ua)
            return ua, cf_clearance_value
        else:
            print("cf challenge fail")
        browser.close()


def main():
    test_not_pass_cf_challenge_request()
    ua, cf_clearance_value = test_cf_challenge()
    test_add_ua_cookie_cf_success(ua, cf_clearance_value)


main()
