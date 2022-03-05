# -*- coding: utf-8 -*-
import asyncio
import functools
import time
import gevent.hub

import gevent

from playwright.async_api import Page as AsyncPage
from playwright.sync_api import Page as SyncPage
from playwright.async_api import expect as async_expect
from playwright.sync_api import expect as sync_expect


async def async_cf_retry(page: AsyncPage, tries=5) -> bool:
    page_assertions = async_expect(page)
    success = False
    while tries != 0:
        try:
            disabled_title_list = ['Please Wait... | Cloudflare', 'Just a moment...', 'www.', 'about:black']
            await asyncio.gather(
                *[asyncio.create_task(page_assertions.not_to_have_title(disabled_title, timeout=5000)) for
                  disabled_title in
                  disabled_title_list])
        except AssertionError:
            tries -= 1
            await asyncio.sleep(0.1)
        else:
            success = True
            break
    return success


def sync_cf_retry(page: SyncPage, tries=5) -> bool:
    page_assertions = sync_expect(page)
    gevent.hub.Hub.NOT_ERROR = (AssertionError,)
    success = False
    while tries != 0:
        try:
            disabled_title_list = ['Please Wait... | Cloudflare', 'Just a moment...', 'www.', 'about:black']
            jobs = [gevent.spawn(functools.partial(page_assertions.not_to_have_title, disabled_title), timeout=5000) for
                    disabled_title in
                    disabled_title_list]
            gevent.joinall(jobs, raise_error=True)

        except AssertionError:
            tries -= 1
            time.sleep(1)
        else:
            success = True
            break
    return success
