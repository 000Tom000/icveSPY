import requests

from utils.baseIO import get_auth, get_cookies, save_auth, save_cookies, save_me, get_me


class SP:
    def __init__(self):
        super().__init__()
        self.load()

    # 加载所有
    def load(self):
        self.session = requests.Session()
        self.session.cookies.update(get_cookies())
        self.authorization = get_auth()
        self.me = get_me()

    # 保存所有
    def save(self):
        save_auth(self.authorization)
        save_cookies(self.session.cookies.get_dict())
        save_me(self.me)
