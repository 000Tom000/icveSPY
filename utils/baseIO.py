import os, json, pathlib
from config import AUTH_FILE, COOKIES_FILE, ME_FILE, INFO_LOG_FILE, SUCC_LOG_FILE, ERROR_LOG_FILE, DEBUG_LOG_FILE
from datetime import datetime


# 保存authorization
def save_auth(authorization: str | dict, user: str = None) -> None:
    if user:
        if os.path.isfile(AUTH_FILE):
            with open(AUTH_FILE, "r", encoding="utf-8") as file:
                auths = json.load(file)
        else:
            auths = dict()
        auths[user] = authorization
        authorization = auths
    with open(AUTH_FILE, "w", encoding="utf-8") as file:
        json.dump(authorization, file, indent=4, ensure_ascii=False)


# 获取authorization
def get_auth(user: str = None) -> str | dict:
    if pathlib.Path(AUTH_FILE).exists():
        with open(AUTH_FILE, "r", encoding="utf-8") as file:
            if user:
                return json.load(file).get(user, str())
            else:
                return json.load(file)
    else:
        return str()


# 保存cookies
def save_cookies(cookies: dict, user: str = None) -> None:
    if user:
        if os.path.isfile(COOKIES_FILE):
            with open(COOKIES_FILE, "r", encoding="utf-8") as file:
                cks = json.load(file)
        else:
            cks = dict()
        cks[user] = cookies
        cookies = cks
    with open(COOKIES_FILE, "w", encoding="utf-8") as file:
        json.dump(cookies, file, ensure_ascii=False, indent=4)


# 装载cookies
def get_cookies(user: str = None) -> dict:
    if pathlib.Path(COOKIES_FILE).exists():
        with open(COOKIES_FILE, "r", encoding="utf-8") as file:
            if user:
                return json.load(file).get(user, dict())
            else:
                return json.load(file)
    else:
        return dict()


# 保存me
def save_me(me: dict, user: str = None) -> None:
    if user:
        if os.path.isfile(ME_FILE):
            with open(ME_FILE, "r", encoding="utf-8") as file:
                users = json.load(file)
        else:
            users = dict()
        users[user] = me
        me = users
    with open(ME_FILE, "w", encoding="utf-8") as file:
        json.dump(me, file, ensure_ascii=False, indent=4)


# 获取me
def get_me(user: str = None) -> dict:
    if pathlib.Path(ME_FILE).exists():
        with open(ME_FILE, "r", encoding="utf-8") as file:
            if user:
                return json.load(file).get(user, dict())
            else:
                return json.load(file)
    else:
        return dict()


# 打印dict
def show_kv(data: dict):
    for k, v in data.items():
        print(f"{k} : {v}")


# 打log
def log(sign: list | str, text: str) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    if type(sign) == str:
        sign = [sign]
    api_sign = sign.pop(0)
    if api_sign == "info":
        file_path = INFO_LOG_FILE
    elif api_sign == "success":
        file_path = SUCC_LOG_FILE
    elif api_sign == "error":
        file_path = ERROR_LOG_FILE
    elif api_sign == "debug" or api_sign == "data":
        file_path = DEBUG_LOG_FILE
    else:
        sign.insert(0, api_sign)
        file_path = INFO_LOG_FILE
    hint_text = f"{timestamp}\t\t{'->'.join(sign)}\t\t{text}"
    with open(file_path, "a+", encoding="utf-8") as file:
        file.write(f"{hint_text}\n")
    print(hint_text)
