# -*- coding: utf-8 -*-
from playwright.async_api import Error
from playwright.async_api import Page as AsyncPage
from playwright.sync_api import Page as SyncPage


async def async_cf_retry(page: AsyncPage, tries: int = 10) -> bool:
    success = False
    while tries != 0:
        await page.wait_for_timeout(1500)
        try:
            success = False if await page.query_selector("#challenge-form") else True
            click_button = await page.query_selector("#challenge-stage > div > input")
            if click_button:
                await click_button.click()
            iframe = await page.query_selector(
                "xpath=//div[@class='hcaptcha-box']/iframe"
            )
            if iframe:
                switch_iframe = await iframe.content_frame()
                iframe_button = await switch_iframe.query_selector(
                    "xpath=//*[@id='cf-stage']//label/span"
                )
                if iframe_button:
                    await iframe_button.click()
        except Error:
            success = False
        if success:
            break
        tries -= 1
    return success


def sync_cf_retry(page: SyncPage, tries: int = 10) -> bool:
    success = False
    while tries != 0:
        page.wait_for_timeout(1500)
        try:
            success = False if page.query_selector("#challenge-form") else True
            click_button = page.query_selector("#challenge-stage > div > input")
            if click_button:
                click_button.click()
            iframe = page.query_selector("xpath=//div[@class='hcaptcha-box']/iframe")
            if iframe:
                iframe_button = iframe.content_frame().query_selector(
                    "xpath=//*[@id='cf-stage']//label/span"
                )
                if iframe_button:
                    iframe_button.click()
        except Error:
            success = False
        if success:
            break
        tries -= 1

    return success
