from joiner import Joiner
import pyfiglet
import json
import os
from colorama import Fore, Style
with open('tokens.txt') as fp:
    tokens = fp.read().splitlines()
with open('config.json') as fp:
    config = json.load(fp)
os.system("cls")
os.system("title Discord Joiner By Shahzain")
print(pyfiglet.figlet_format("Discord Joiner"))
print(f"{Style.BRIGHT}By Shahzain{Style.RESET_ALL}")
with open("proxies.txt") as fp:
    if len(fp.read().splitlines()) == 0:
        print(
            f"{Style.BRIGHT}{Fore.RED}[?] Input some proxies before restarting{Style.RESET_ALL}")
        input("[?] Press Enter To Exit: ")
        exit()

if len(tokens) == 0:
    print(
        f"{Style.BRIGHT}{Fore.RED}[?] Input some tokens before restarting{Style.RESET_ALL}")
    input("[?] Press Enter To Exit: ")
    exit()

inv = str(
    input(f"{Style.BRIGHT}{Fore.GREEN}[>] Enter The Invite: \n>> {Style.RESET_ALL}"))
for token in tokens:
    joiner = Joiner(config["capKey"], inv, token)
    joiner.joinServer()
