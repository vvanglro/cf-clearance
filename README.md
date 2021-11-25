# cf_clearance
Reference from [playwright_stealth](https://github.com/AtuboDad/playwright_stealth) and [undetected-chromedriver](https://github.com/ultrafunkamsterdam/undetected-chromedriver)

Purpose To make a cloudflare challenge pass successfully, Can be use cf_clearance bypassed by cloudflare, However, with the cf_clearance, make sure you use the same IP and UA as when you got it.

## Warning
Please use interface mode, You must add headless=False.  
If you use it on linux, use XVFB.

## Install

```
$ pip install cf_clearance
```

## Usage
### sync
```python
from playwright.sync_api import sync_playwright
from cf_clearance import sync_retry, stealth_sync

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
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
        print("fail")
    browser.close()
```
### async
```python
import asyncio
from playwright.async_api import async_playwright
from cf_clearance import async_retry, stealth_async

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
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
            print("fail")
        await browser.close()


asyncio.get_event_loop().run_until_complete(main())
```