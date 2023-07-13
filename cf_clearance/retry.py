# -*- coding: utf-8 -*-
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
            simple_challenge = await page.query_selector(
                "#challenge-stage > div > input[type='button']"
            )
            if simple_challenge:
                await simple_challenge.click()
            for target_frame in page.main_frame.child_frames:
                if "challenge" in target_frame.url and "turnstile" in target_frame.url:
                    click = await target_frame.query_selector(
                        "xpath=//input[@type='checkbox']"
                    )
                    if click:
                        await click.click()
        except Error:
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
            simple_challenge = page.query_selector(
                "#challenge-stage > div > input[type='button']"
            )
            if simple_challenge:
                simple_challenge.click()
            for target_frame in page.main_frame.child_frames:
                if "challenge" in target_frame.url and "turnstile" in target_frame.url:
                    click = target_frame.query_selector(
                        "xpath=//input[@type='checkbox']"
                    )
                    if click:
                        click.click()
        except Error:
            success = False
        tries -= 1
    if tries == user_tries:
        cf = False
    return success, cf
