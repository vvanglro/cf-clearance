import asyncio

from fastapi import FastAPI
from playwright.async_api import async_playwright
from pydantic import BaseModel, Field

from cf_clearance import async_cf_retry, async_stealth
from cf_clearance.errors import RecaptchaChallengeException

from pyvirtualdisplay import Display

app = FastAPI()


class ProxySetting(BaseModel):
    server: str = Field(...)
    username: str = Field("", description="Optional username to use if HTTP proxy requires authentication.")
    password: str = Field("", description="Optional password to use if HTTP proxy requires authentication.")


class ChallengeRequest(BaseModel):
    proxy: ProxySetting = Field(...)
    timeout: int = Field(10)
    url: str = Field(...)

    class Config:
        schema_extra = {
            'example': {
                "proxy": {
                    "server": "socks5://localhost:7890"
                },
                "timeout": 20,
                "url": "https://nowsecure.nl"
            },
        }


class ChallengeResponse(BaseModel):
    success: bool = Field(True)
    msg: str = Field(None)
    user_agent: str = Field(None)
    cf_clearance_value: str = Field(None)


async def pw_challenge(data: ChallengeRequest):
    # Create a new context for each request:
    # https://github.com/microsoft/playwright/issues/17736#issuecomment-1263667429
    # https://github.com/microsoft/playwright/issues/6319
    proxy_setting = data.proxy
    with Display():
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False, proxy={"server": proxy_setting.server,
                                                                     "username": proxy_setting.username,
                                                                     "password": proxy_setting.password}, args=[
                "--disable-gpu",
                '--no-sandbox',
                '--disable-dev-shm-usage',
                '--no-first-run',
                '--no-service-autorun',
                '--no-default-browser-check',
                '--password-store=basic',
                '--start-maximized',
            ])
            page = await browser.new_page()
            await async_stealth(page, pure=True)
            await page.goto(data.url)
            success = await async_cf_retry(page)
            cf_clearance_value = None
            if not success:
                await browser.close()
                return {"success": success, "user_agent": None, "cf_clearance_value": None, "msg": "cf challenge fail"}
            cookies = await page.context.cookies()
            for cookie in cookies:
                if cookie.get('name') == 'cf_clearance':
                    cf_clearance_value = cookie.get('value')
            ua = await page.evaluate('() => {return navigator.userAgent}')
            await browser.close()
            return {"success": success, "user_agent": ua, "cf_clearance_value": cf_clearance_value}


@app.post("/challenge", response_model=ChallengeResponse)
async def cf_challenge(data: ChallengeRequest):
    try:
        res = await asyncio.wait_for(pw_challenge(data), timeout=data.timeout)
    except asyncio.TimeoutError:
        return {"success": False, "msg": "challenge timeout"}
    except RecaptchaChallengeException as e:
        return {"success": False, "msg": str(e)}
    except Exception as e:
        return {"success": False, "msg": str(e)}
    else:
        return res
