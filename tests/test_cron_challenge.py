from playwright.async_api import async_playwright

from cf_clearance import async_cf_retry, async_stealth


async def test_cf_challenge(url: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await async_stealth(page, pure=True)
        await page.goto(url)
        res = await async_cf_retry(page)
        if res:
            cookies = await page.context.cookies()
            for cookie in cookies:
                if cookie.get("name") == "cf_clearance":
                    cf_clearance_value = cookie.get("value")
        assert cf_clearance_value
        await browser.close()


if __name__ == "__main__":
    import asyncio

    asyncio.run(test_cf_challenge("https://nowsecure.nl"))
