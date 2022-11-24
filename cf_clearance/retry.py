# -*- coding: utf-8 -*-
from playwright.async_api import Error
from playwright.async_api import Page as AsyncPage
from playwright.sync_api import Page as SyncPage


async def async_cf_retry(page: AsyncPage, tries: int = 10) -> bool:
    success = False
    while tries != 0:
        try:
            success = (False if await page.query_selector('#challenge-form') else True)
        except Error:
            success = False
        if success:
            break
        else:
            tries -= 1
            await page.wait_for_timeout(1500)
    return success


def sync_cf_retry(page: SyncPage, tries: int = 10) -> bool:
    success = False
    while tries != 0:
        try:
            success = (False if page.query_selector('#challenge-form') else True)
        except Error:
            success = False
        if success:
            break
        else:
            tries -= 1
            page.wait_for_timeout(1500)
    return success
