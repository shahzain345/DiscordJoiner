import random
import httpx
import json
from colorama import Fore,Style
with open('config.json') as fp:
    config = json.load(fp)
captchaApi = config["captchaApi"]
class Joiner:
    def __init__(self, capKey, inv, token):
        self.capKey = capKey
        self.inv = inv
        with open("proxies.txt") as fp:
            proxies = fp.read().splitlines()
        self.client = httpx.Client(cookies={"locale": "en-US"}, headers={
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US",
            "origin": "https://discord.com",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": 'same-origin',
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9003 Chrome/91.0.4472.164 Electron/13.4.0 Safari/537.36",
            "x-context-properties": "eyJsb2NhdGlvbiI6IkpvaW4gR3VpbGQiLCJsb2NhdGlvbl9ndWlsZF9pZCI6IjkxNTU4NTgwMDYxMDExOTcxMSIsImxvY2F0aW9uX2NoYW5uZWxfaWQiOiI5MzQ3MDcwNDI3MDExNTIyODciLCJsb2NhdGlvbl9jaGFubmVsX3R5cGUiOjB9",
            "x-debug-options": "bugReporterEnabled",
            "x-discord-locale": "en-US",
            "x-super-properties": 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MDAzIiwib3NfdmVyc2lvbiI6IjEwLjAuMjIwMDAiLCJvc19hcmNoIjoieDY0Iiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiY2xpZW50X2J1aWxkX251bWJlciI6MTE0NDA3LCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ=='
        }, proxies=f"http://{random.choice(proxies)}")
        self.client.headers["authorization"] = token
        self.client.headers["x-fingerprint"] = self.client.get("https://discord.com/api/v9/experiments", timeout=30).json()["fingerprint"]
    def joinServer(self):
        res = self.client.post(f'https://discord.com/api/v9/invites/{self.inv}', json={"captcha_key": self.getCap()})
        if res.status_code == 200:
            print(f"{Fore.GREEN}{Style.BRIGHT}[>] Joined server {self.client.headers['authorization']} {Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}{Style.BRIGHT}[>] Failed to join server {self.client.headers['authorization']} {Style.RESET_ALL}")
    def getCap(self):
        solvedCaptcha = None
        captchaKey = self.capKey
        taskId = ""
        taskId = httpx.post(f"https://api.{captchaApi}/createTask", json={"clientKey": captchaKey, "task": {"type": "HCaptchaTaskProxyless", "websiteURL": "https://discord.com/",
                               "websiteKey": "4c672d35-0701-42b2-88c3-78380b0db560", "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0"}}, timeout=30).json()
        if taskId.get("errorId") > 0:
                print(f"{Fore.RED}{Style.BRIGHT}[-] createTask - {taskId.get('errorDescription')}!{Style.RESET_ALL}")
                return None

        taskId = taskId.get("taskId")
            
        while not solvedCaptcha:
                    captchaData = httpx.post(f"https://api.{captchaApi}/getTaskResult", json={"clientKey": captchaKey, "taskId": taskId}, timeout=30).json()
                    if captchaData.get("status") == "ready":
                        solvedCaptcha = captchaData.get("solution").get("gRecaptchaResponse")
                        print(f"{Fore.GREEN}{Style.BRIGHT}[>] Got Captcha {solvedCaptcha[0:60]}{Style.RESET_ALL}")
                        return solvedCaptcha