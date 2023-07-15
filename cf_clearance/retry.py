# -*- coding: utf-8 -*-
import logging
from typing import Tuple

from playwright.async_api import Error
from playwright.async_api import Page as AsyncPage
from playwright.sync_api import Page as SyncPage


async def async_cf_retry(page: AsyncPage, tries: int = 10) -> Tuple[bool, bool]:
    success = False
    cf = True
    user_tries = tries
    while tries > 0:
        await page.wait_for_timeout(1500)
        try:
            success = False if await page.query_selector("#challenge-form") else True
            if success:
                break
            for target_frame in page.main_frame.child_frames:
                if "challenge" in target_frame.url and "turnstile" in target_frame.url:
                    try:
                        click = await target_frame.query_selector(
                            "#challenge-stage > div > label > input[type=checkbox]"
                        )
                    except Error:
                        # frame is refreshed, so playwright._impl._api_types.Error: Target closed
                        logging.debug("Playwright Error:", exc_info=True)
                    else:
                        if click:
                            await click.click()
        except Error:
            logging.debug("Playwright Error:", exc_info=True)
            success = False
        tries -= 1
    if tries == user_tries:
        cf = False
    return success, cf


def sync_cf_retry(page: SyncPage, tries: int = 10) -> Tuple[bool, bool]:
    success = False
    cf = True
    user_tries = tries
    while tries > 0:
        page.wait_for_timeout(1500)
        try:
            success = False if page.query_selector("#challenge-form") else True
            if success:
                break
            for target_frame in page.main_frame.child_frames:
                if "challenge" in target_frame.url and "turnstile" in target_frame.url:
                    try:
                        click = target_frame.query_selector(
                            "#challenge-stage > div > label > input[type=checkbox]"
                        )
                    except Error:
                        # frame is refreshed, so playwright._impl._api_types.Error: Target closed
                        logging.debug("Playwright Error:", exc_info=True)
                    else:
                        if click:
                            click.click()
        except Error:
            logging.debug("Playwright Error:", exc_info=True)
            success = False
        tries -= 1
    if tries == user_tries:
        cf = False
    return success, cf
