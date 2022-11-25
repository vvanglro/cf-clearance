import logging

import requests


def test_not_pass_cf_challenge_request():
    proxies = {"all": "socks5://localhost:7890"}
    res = requests.get("https://nowsecure.nl", proxies=proxies)
    if "<title>Just a moment...</title>" in res.text:
        logging.info("not use clearance cf challenge fail")


def test_add_ua_cookie_cf_success(ua, cf_clearance):
    proxies = {"all": "socks5://localhost:7890"}
    headers = {"user-agent": ua}
    cookies = {"cf_clearance": cf_clearance}

    res = requests.get(
        "https://nowsecure.nl", proxies=proxies, headers=headers, cookies=cookies
    )
    if "<title>Just a moment...</title>" not in res.text:
        logging.info("use clearance cf challenge success")
