import time
from apis.userapi import UserApi
from models.sper import SP
from utils.baseIO import log


class UserService:
    def __init__(self, sp: SP):
        super().__init__()
        self.sp = sp
        self.userapi = UserApi(self.sp)

    # 个人信息
    def me(self):
        self.userapi.mev2()
        res = self.userapi.routers()
        if self.sp.me and res["code"] == 200:
            self.sp.save()
            log(["账号登录状态"],
                f"{self.sp.user} 已登录 | {self.sp.me["schoolName"]} | {self.sp.me["displayName"]} | {self.sp.me["mobile"]}")
            return True
        else:
            log(["账号登录状态"], f"{self.sp.user} 未登录")
            return False

    # 扫码登录
    def login_progress(self):
        sceneId, qrUrl = self.userapi.login_qrcode()
        while True:
            status, expireTime, token = self.userapi.login_qrcode_status(sceneId)
            status_str = "status : " + str(status)
            if status == 0:
                status_str = "未扫码"
                log(["扫码登录"], f"{status_str} | 剩余过期时间 {expireTime} s")
            elif status == 1:
                status_str = "已扫码待确认"
                log(["扫码登录"], f"{status_str} | 剩余过期时间 {expireTime} s")
            elif status == 2:
                status_str = "已登录"
                log(["success", "扫码登录"], f"{status_str} | 剩余过期时间 {expireTime} s")
            else:
                log(["扫码登录"], f"{status_str} | 剩余过期时间 {expireTime} s")
            if status == 2:
                # userapi.login(token)
                self.userapi.loginv2(token)
                self.userapi.mev2()
                self.sp.save()
                return
            time.sleep(1.23)
