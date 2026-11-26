import requests
from utils.baseIO import get_auth, get_cookies, save_auth, save_cookies, save_me, get_me


class SP:
    def __init__(self, user: str = None, tasks: list = []):
        super().__init__()
        self.user = user
        self.tasks = tasks
        self.load()

    # 加载所有
    def load(self):
        self.session = requests.Session()
        if self.user:
            self.authorization = get_auth(self.user)
            self.session.cookies.update(get_cookies(self.user))
            self.me = get_me(self.user)

    # 保存所有
    def save(self):
        if self.user:
            save_auth(self.authorization, self.user)
            save_cookies(self.session.cookies.get_dict(), self.user)
            save_me(self.me, self.user)
