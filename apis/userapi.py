import time

from models.sper import SP
from utils.common import show_qrcode
from utils.baseIO import log


class UserApi:
    def __init__(self, sp: SP):
        super().__init__()
        self.sp = sp

    # 获取登录的二维码
    def login_qrcode(self):
        res = self.sp.session.get("https://sso.icve.com.cn/prod-api/v2/user/generateQrCode")
        res = res.json()["data"]
        sceneId = res["sceneId"]
        qrUrl = res["qrUrl"]
        show_qrcode(qrUrl)
        return (sceneId, qrUrl)

    # 获取登录二维码的操作状态
    def login_qrcode_status(self, sceneId: str) -> tuple:
        res = self.sp.session.get(f"https://sso.icve.com.cn/prod-api/v2/user/status/{sceneId}")
        res = res.json()["data"]
        return (res["status"], res["expireTime"], res.get("token", None))

    # 登录
    def login(self, token):
        params = {
            "token": token
        }
        res = self.sp.session.post("https://www.icve.com.cn/prod-api/uc/passLogin", params=params)
        res = res.json()
        self.sp.session.cookies.update({
            "Token": res["data"],
        })
        self.sp.authorization = f"Bearer {res["data"]}"

    # 登录v2
    def loginv2(self, token):
        params = {
            "token": token
        }
        self.sp.session.cookies.update({
            "token": token
        })
        res = self.sp.session.get("https://zjy2.icve.com.cn/prod-api/auth/passLogin", params=params)
        # log(["userapi", "loginv2"], res.json())
        res = res.json()["data"]
        self.sp.session.cookies.update({
            "Token": res["access_token"],
        })
        self.sp.authorization = f"Bearer {res["access_token"]}"

    # 获取用户信息
    def me(self) -> dict | None:
        headers = {
            "authorization": self.sp.authorization,
        }
        res = self.sp.session.get("https://www.icve.com.cn/prod-api/getInfo", headers=headers).json()
        if res["code"] == 401:
            log(["userapi", "me"], "未登录")
            # print("userapi : me : 未登录")
            return None
        else:
            user = res["data"]["user"]
            log(["userapi", "me"], f"已登录 | {user["schoolName"]} | {user["nickName"]} | {user["phonenumber"]}")
            # print(f'userapi : me : 已登录 | {user["schoolName"]} | {user["nickName"]} | {user["phonenumber"]}')
            return user

    # 获取用户信息
    def mev2(self) -> dict | None:
        params = {
            "token": self.sp.session.cookies.get_dict().get("token", ""),
        }
        headers = {
            "authorization": self.sp.authorization,
        }
        res = self.sp.session.post("https://sso.icve.com.cn/prod-api/user/userInfo", headers=headers,
                                   params=params).json()
        self.sp.me = res["data"]

    # 退登
    def logout(self):
        headers = {
            "authorization": self.sp.authorization,
        }
        params = {
            "token": self.sp.session.cookies.get("token")
        }
        res = self.sp.session.delete("https://zjy2.icve.com.cn/prod-api/auth/logout", headers=headers, params=params)
        log(["userapi", "logout"], res.json())

# 登录过程
## 判定了用户未登录就可以调用该函数
# def login_progress(sp: SP, userapi: USERAPI):
#     sceneId, qrUrl = userapi.login_qrcode()
#     while True:
#         # print(userapi.login_qrcode_status(sceneId))
#         status, expireTime, token = userapi.login_qrcode_status(sceneId)
#         # print(status, expireTime)
#         status_str = "status : " + str(status)
#         if status == 0:
#             status_str = "未扫码"
#         elif status == 1:
#             status_str = "已扫码待确认"
#         elif status == 2:
#             status_str = "已登录"
#         print(f"{status_str} | 剩余过期时间 {expireTime} s")
#         if status == 2:
#             # userapi.login(token)
#             userapi.loginv2(token)
#             sp.me = userapi.mev2()
#             sp.save()
#             return
#         time.sleep(1.23)


# if __name__ == '__main__':
#     # 一个爬虫子
#     sp = SP()
#     userapi = USERAPI(sp)
#     # sp.me = userapi.me()
#     sp.me = userapi.mev2()
#     while not sp.me:
#         login_progress(sp, userapi)
