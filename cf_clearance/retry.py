# -*- coding: utf-8 -*-
import asyncio
import time

from playwright.async_api import Error
from playwright.async_api import Page as AsyncPage
from playwright.sync_api import Page as SyncPage


async def async_retry(page: AsyncPage) -> bool:
    num = 0
    while 1:
        try:
            title = await page.title()
        except Error:
            await asyncio.sleep(1)
            continue
        else:
            if "Just a moment" in title:
                num += 1
                await asyncio.sleep(2)
            elif "www." in title:
                await page.reload()
                num += 2
                await asyncio.sleep(3)
            else:
                break
            if num >= 10:
                break
    if num < 10:
        return True
    return False


def sync_retry(page: SyncPage) -> bool:
    num = 0
    while 1:
        try:
            title = page.title()
        except Error:
            time.sleep(1)
            continue
        else:
            if "Just a moment" in title:
                num += 1
                time.sleep(2)
            elif "www." in title:
                page.reload()
                num += 2
                time.sleep(3)
            else:
                break
            if num >= 10:
                break
    if num < 10:
        return True
    return False
