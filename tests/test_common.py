import requests


def test_not_pass_cf_challenge_request():
    proxies = {
        "all": "socks5://localhost:7890"
    }
    res = requests.get('https://nowsecure.nl', proxies=proxies)
    if '<title>Please Wait... | Cloudflare</title>' in res.text:
        print("cf challenge fail")


def test_add_ua_cookie_cf_success(ua, cf_clearance):
    proxies = {
        "all": "socks5://localhost:7890"
    }
    headers = {
        "user-agent": ua
    }
    cookies = {
        "cf_clearance": cf_clearance
    }

    res = requests.get('https://nowsecure.nl', proxies=proxies, headers=headers, cookies=cookies)
    if '<title>Please Wait... | Cloudflare</title>' not in res.text:
        print("cf challenge success")
