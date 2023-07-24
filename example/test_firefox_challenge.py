import requests
from playwright.async_api import async_playwright

from cf_clearance import async_cf_retry


async def test_cf_challenge(url: str):
    # not use cf_clearance, cf challenge is fail
    res = requests.get("https://nowsecure.nl")
    assert "<title>Just a moment...</title>" in res.text
    # get cf_clearance
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(url)
        success, cf = await async_cf_retry(page)
        if cf:
            if success:
                cookies = await page.context.cookies()
                for cookie in cookies:
                    if cookie.get("name") == "cf_clearance":
                        cf_clearance_value = cookie.get("value")
                print(cf_clearance_value)
                ua = await page.evaluate("() => {return navigator.userAgent}")
                assert cf_clearance_value
            else:
                raise
        else:
            print("No cloudflare challenges encountered")
        await browser.close()
    # use cf_clearance, must be same IP and UA
    headers = {"user-agent": ua}
    cookies = {"cf_clearance": cf_clearance_value}
    res = requests.get("https://nowsecure.nl", headers=headers, cookies=cookies)
    assert "<title>Just a moment...</title>" not in res.text


if __name__ == "__main__":
    import asyncio

    asyncio.run(test_cf_challenge("https://nowsecure.nl"))
