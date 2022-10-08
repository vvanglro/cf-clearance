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
        try:
            title = await page.title()
        except Error:
            tries -= 1
            await asyncio.sleep(1)
        else:
            if title == 'Please Wait... | Cloudflare':
                raise RecaptchaChallengeException("Encountered recaptcha. Check whether your proxy is an elite proxy.")
            elif title == 'Just a moment...':
                tries -= 1
                await asyncio.sleep(2)
            elif "www." in title:
                await page.reload()
                tries -= 1
                await asyncio.sleep(3)
            else:
                success = True
                break
    return success


def sync_cf_retry(page: SyncPage, tries=10) -> bool:
    success = False
    while tries != 0:
        try:
            title = page.title()
        except Error:
            tries -= 1
            time.sleep(1)
        else:
            if title == 'Please Wait... | Cloudflare':
                raise RecaptchaChallengeException("Encountered recaptcha. Check whether your proxy is an elite proxy.")
            elif title == 'Just a moment...':
                tries -= 1
                time.sleep(2)
            elif "www." in title:
                page.reload()
                tries -= 1
                time.sleep(3)
            else:
                success = True
                break
    return success
