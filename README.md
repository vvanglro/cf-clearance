# cf-clearance

[![OSCS Status](https://www.oscs1024.com/platform/badge/vvanglro/cf_clearance.svg?size=small)](https://www.oscs1024.com/project/vvanglro/cf_clearance?ref=badge_small)
[![Package version](https://img.shields.io/pypi/v/cf_clearance?color=%2334D058&label=pypi%20package)](https://pypi.python.org/pypi/cf_clearance)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/cf_clearance.svg?color=%2334D058)](https://pypi.python.org/pypi/cf_clearance)
[![Docker Image versions](https://img.shields.io/docker/v/vvanglro/cf-clearance?color=%2334D058&label=docker%20version)](https://hub.docker.com/r/vvanglro/cf-clearance)


Purpose To make a cloudflare v2 challenge pass successfully, Can be use cf_clearance bypassed by cloudflare, However, with
the cf_clearance, make sure you use the same IP and UA as when you got it.

## Project Pass Challenge Status
[![Every day cron challenge](https://github.com/vvanglro/cf-clearance/actions/workflows/every_day_cron_challenge.yml/badge.svg)](https://github.com/vvanglro/cf-clearance/actions/workflows/every_day_cron_challenge.yml)

## Warning

Please use interface mode, You must add headless=False.
If you use it on linux or docker, use XVFB.

Challenge are not always successful. Please try more and handle exceptions.


## Docker Usage

Recommended to install using Docker container on Ubuntu server.
DockerHub => https://hub.docker.com/r/vvanglro/cf-clearance

```shell
docker run -d --restart always --network host --name cf-clearance vvanglro/cf-clearance:latest \
--host 0.0.0.0 --port 8000 --workers 1
```

```shell
curl http://localhost:8000/challenge -H "Content-Type:application/json" -X POST \
-d '{"proxy": {"server": "socks5://localhost:7890"}, "timeout":20, "url": "https://nowsecure.nl"}'
```

```python
import requests

proxy = "socks5://localhost:7890"
resp = requests.post("http://localhost:8000/challenge",
                     json={"proxy": {"server": proxy}, "timeout": 20,
                           "url": "https://nowsecure.nl"})
data = resp.json()
# In some cases, the cloudflare challenge will not be triggered, so when cf in the return parameter is true, it means that the challenge has been encountered.
if data.get("success") and data.get("cf"):
    ua = data.get("user_agent")
    cf_clearance_value = data.get("cookies").get("cf_clearance")
    # use cf_clearance, must be same IP and UA
    headers = {"user-agent": ua}
    cookies = {"cf_clearance": cf_clearance_value}
    res = requests.get('https://nowsecure.nl', proxies={
        "all": proxy
    }, headers=headers, cookies=cookies)
    if '<title>Just a moment...</title>' not in res.text:
        print("cf challenge success")
```

## Install

```
pip install cf-clearance
```

## Usage

Please make sure it is the latest package.

```
pip install --upgrade cf-clearance
```
or
```shell
pip install git+https://github.com/vvanglro/cf-clearance.git@main
```

### sync

```python
from playwright.sync_api import sync_playwright
from cf_clearance import sync_cf_retry, sync_stealth
import requests

# not use cf_clearance, cf challenge is fail
proxies = {
    "all": "socks5://localhost:7890"
}
res = requests.get('https://nowsecure.nl', proxies=proxies)
if '<title>Just a moment...</title>' in res.text:
    print("cf challenge fail")
# get cf_clearance
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, proxy={"server": "socks5://localhost:7890"})
    page = browser.new_page()
    sync_stealth(page, pure=True)
    page.goto('https://nowsecure.nl')
    res, cf = sync_cf_retry(page)
    if cf:
        if res:
            cookies = page.context.cookies()
            for cookie in cookies:
                if cookie.get('name') == 'cf_clearance':
                    cf_clearance_value = cookie.get('value')
                    print(cf_clearance_value)
            ua = page.evaluate('() => {return navigator.userAgent}')
            print(ua)
        else:
            print("cf challenge fail")
    else:
        print("No cloudflare challenges encountered")
    browser.close()
# use cf_clearance, must be same IP and UA
headers = {"user-agent": ua}
cookies = {"cf_clearance": cf_clearance_value}
res = requests.get('https://nowsecure.nl', proxies=proxies, headers=headers, cookies=cookies)
if '<title>Just a moment...</title>' not in res.text:
    print("cf challenge success")
```

### async

```python
import asyncio
from playwright.async_api import async_playwright
from cf_clearance import async_cf_retry, async_stealth
import requests


async def main():
    # not use cf_clearance, cf challenge is fail
    proxies = {
        "all": "socks5://localhost:7890"
    }
    res = requests.get('https://nowsecure.nl', proxies=proxies)
    if '<title>Just a moment...</title>' in res.text:
        print("cf challenge fail")
    # get cf_clearance
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, proxy={"server": "socks5://localhost:7890"})
        page = await browser.new_page()
        await async_stealth(page, pure=True)
        await page.goto('https://nowsecure.nl')
        res, cf = await async_cf_retry(page)
        if cf:
            if res:
                cookies = await page.context.cookies()
                for cookie in cookies:
                    if cookie.get('name') == 'cf_clearance':
                        cf_clearance_value = cookie.get('value')
                        print(cf_clearance_value)
                ua = await page.evaluate('() => {return navigator.userAgent}')
                print(ua)
            else:
                print("cf challenge fail")
        else:
            print("No cloudflare challenges encountered")
        await browser.close()
    # use cf_clearance, must be same IP and UA
    headers = {"user-agent": ua}
    cookies = {"cf_clearance": cf_clearance_value}
    res = requests.get('https://nowsecure.nl', proxies=proxies, headers=headers, cookies=cookies)
    if '<title>Just a moment...</title>' not in res.text:
        print("cf challenge success")


asyncio.get_event_loop().run_until_complete(main())
```
