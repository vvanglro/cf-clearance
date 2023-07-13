from playwright.async_api import async_playwright

from cf_clearance import async_cf_retry, async_stealth


async def test_cf_challenge(url: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
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
        context = await browser.new_context()
        page = await context.new_page()
        await async_stealth(page, pure=True)
        await page.goto(url)
        res, cf = await async_cf_retry(page)
        if cf:
            if res:
                cookies = await page.context.cookies()
                for cookie in cookies:
                    if cookie.get("name") == "cf_clearance":
                        cf_clearance_value = cookie.get("value")
                assert cf_clearance_value
            else:
                raise
        else:
            print("No cloudflare challenges encountered")
        await browser.close()


if __name__ == "__main__":
    import asyncio

    asyncio.run(test_cf_challenge("https://nowsecure.nl"))
