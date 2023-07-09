import asyncio
from typing import Dict, List, Literal, Optional

from fastapi import FastAPI
from playwright.async_api import async_playwright
from pydantic import BaseModel, Field
from pyvirtualdisplay import Display
from typing_extensions import TypedDict

from cf_clearance import async_cf_retry, async_stealth

app = FastAPI()


class ProxySetting(BaseModel):
    server: str = Field(...)
    username: str = Field(
        "",
        description="Optional username to use if HTTP proxy requires authentication.",
    )
    password: str = Field(
        "",
        description="Optional password to use if HTTP proxy requires authentication.",
    )


class SetCookieParam(TypedDict, total=False):
    name: str
    value: str
    url: Optional[str]
    domain: Optional[str]
    path: Optional[str]
    expires: Optional[float]
    httpOnly: Optional[bool]
    secure: Optional[bool]
    sameSite: Optional[Literal["Lax", "None", "Strict"]]


class ChallengeRequest(BaseModel):
    proxy: ProxySetting = Field(None)
    timeout: int = Field(10)
    url: str = Field(...)
    pure: bool = Field(False)
    cookies: List[SetCookieParam] = Field(None)
    headers: Dict[str, str] = Field(None)

    class Config:
        schema_extra = {
            "example": {
                "proxy": {"server": "socks5://localhost:7890"},
                "timeout": 20,
                "url": "https://nowsecure.nl",
                "pure": False,
                "cookies": [
                    {
                        "url": "https://www.example.com",
                        "name": "example-cookie",
                        "value": "example-value",
                    }
                ],
                "headers": {"example-ua": "example-ua-value"},
            },
        }


class ChallengeResponse(BaseModel):
    success: bool = Field(True)
    msg: str = Field(None)
    user_agent: str = Field(None)
    cookies: dict = Field(None)
    headers: dict = Field(None)
    content: str = Field(None)


async def pw_challenge(data: ChallengeRequest):
    launch_data = {
        "headless": False,
        "proxy": {
            "server": data.proxy.server,
            "username": data.proxy.username,
            "password": data.proxy.password,
        }
        if data.proxy
        else None,
        "args": [
            "--disable-gpu",
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--no-first-run",
            "--no-service-autorun",
            "--no-default-browser-check",
            "--password-store=basic",
        ],
    }
    # Create a new context for each request:
    # https://github.com/microsoft/playwright/issues/17736#issuecomment-1263667429
    # https://github.com/microsoft/playwright/issues/6319
    with Display():
        async with async_playwright() as p:
            browser = await p.chromium.launch(**launch_data)
            ctx = await browser.new_context()
            if data.cookies:
                await ctx.add_cookies(data.cookies)
            if data.headers:
                await ctx.set_extra_http_headers(data.headers)
            page = await ctx.new_page()
            await async_stealth(page, pure=data.pure)
            resp = await page.goto(data.url)
            success = await async_cf_retry(page)
            if not success:
                await browser.close()
                return {"success": success, "msg": "cf challenge fail"}
            user_agent = await page.evaluate("() => navigator.userAgent")
            cookies = {
                cookie["name"]: cookie["value"]
                for cookie in await page.context.cookies()
            }
            content = await page.content()
            await browser.close()
    return {
        "success": success,
        "user_agent": user_agent,
        "cookies": cookies,
        "msg": "cf challenge success",
        "content": content,
        "headers": resp.headers,
    }


@app.post("/challenge", response_model=ChallengeResponse)
async def cf_challenge(data: ChallengeRequest):
    try:
        return await asyncio.wait_for(pw_challenge(data), timeout=data.timeout)
    except asyncio.TimeoutError:
        return {"success": False, "msg": "challenge timeout"}
    except Exception as e:
        return {"success": False, "msg": str(e)}
