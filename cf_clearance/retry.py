# -*- coding: utf-8 -*-
import asyncio
import time

from playwright.async_api import Error
from playwright.async_api import Page as AsyncPage
from playwright.sync_api import Page as SyncPage

from cf_clearance.errors import RecaptchaChallengeException


async def async_cf_retry(page: AsyncPage, tries=10) -> bool:
    success = False
    while tries != 0:
        if await page.query_selector('#challenge-form'):
            tries -= 1
            await page.wait_for_timeout(1000)
        else:
            success = True
            break
    return success


def sync_cf_retry(page: SyncPage, tries=10) -> bool:
    success = False
    while tries != 0:
        if page.query_selector('#challenge-form'):
            tries -= 1
            page.wait_for_timeout(1000)
        else:
            success = True
            break
    return success
