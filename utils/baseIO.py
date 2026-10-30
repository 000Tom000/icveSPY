import json
import pathlib

import requests

from config import AUTH_FILE, COOKIES_FILE, ME_FILE
from datetime import datetime


# # 保存 authorization 和 cookies
# def save():
#     global authorization, session
#     save_auth()
#     save_cookies()
#
#
# # 加载 authorization 和 cookies
# def load():
#     global authorization, session
#     get_auth()
#     get_cookies()


# 保存authorization
def save_auth(authorization: str) -> None:
    with open(AUTH_FILE, "w") as file:
        file.write(authorization)


# 获取authorization
def get_auth() -> str:
    if pathlib.Path(AUTH_FILE).exists():
        with open(AUTH_FILE, "r") as file:
            return file.read()
    else:
        return str()


# 保存cookies
def save_cookies(cookies: dict) -> None:
    with open(COOKIES_FILE, "w", encoding="utf-8") as file:
        json.dump(cookies, file, ensure_ascii=False, indent=4)


# 装载cookies
def get_cookies() -> dict:
    if pathlib.Path(COOKIES_FILE).exists():
        with open(COOKIES_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    else:
        return dict()


# 保存me
def save_me(me: dict) -> None:
    with open(ME_FILE, "w", encoding="utf-8") as file:
        json.dump(me, file, ensure_ascii=False, indent=4)


# 获取me
def get_me() -> dict:
    with open(ME_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


# 打印dict
def show_kv(data: dict):
    for k, v in data.items():
        print(f"{k} : {v}")


# 打log
def log(sign: list | str, text: str) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    if type(sign) == str:
        sign = [sign]
    print(f"{timestamp}\t\t{'->'.join(sign)}\t\t{text}")
