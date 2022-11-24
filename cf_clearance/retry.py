# -*- coding: utf-8 -*-
import asyncio
import time

from playwright.async_api import Error
from playwright.async_api import Page as AsyncPage
from playwright.sync_api import Page as SyncPage

from cf_clearance.errors import RecaptchaChallengeException


async def async_cf_retry(page: AsyncPage, tries=10) -> bool:
    while tries != 0:
        try:
            success = (False if await page.query_selector('#challenge-form') else True)
        except Error:
            success = False
        if success:
            break
        else:
            tries -= 1
            await page.wait_for_timeout(1000)
    return success


def sync_cf_retry(page: SyncPage, tries=10) -> bool:
    while tries != 0:
        try:
            success = (False if page.query_selector('#challenge-form') else True)
        except Error:
            success = False
        if success:
            break
        else:
            tries -= 1
            page.wait_for_timeout(1000)
    return success
