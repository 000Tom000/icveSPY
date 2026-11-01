import json
import math
import time

from apis.courseapi import CourseApi
from apis.userapi import UserApi
from models.sper import SP
from utils.baseIO import log, show_kv
from utils.encrypt import encrypt_data


class StudyApi:
    def __init__(self, sp):
        super().__init__()
        self.sp = sp

    # 课程学习内容列表
    def studies(self, courseId: str, courseInfoId: str, classId: str, parentId: str = "0", level: int = 1) -> list:
        headers = {
            "authorization": self.sp.authorization,
        }
        params = {
            "courseId": courseId,
            "courseInfoId": courseInfoId,
            "parentId": parentId,
            "level": level,
            "classId": classId,
        }
        res = self.sp.session.get("https://zjy2.icve.com.cn/prod-api/spoc/courseDesign/study/record", headers=headers,
                                  params=params)
        res = res.json()
        for i in range(len(res)):
            res[i]["lv"] = level
        return res

    # ppt数据
    def source(self, sourceId: str, classId: str) -> dict:
        headers = {
            "authorization": self.sp.authorization,
        }
        params = {
            "id": sourceId,
            "classId": classId
        }
        res = self.sp.session.get("https://zjy2.icve.com.cn/prod-api/spoc/courseDesign/getStudyCellInfo",
                                  headers=headers, params=params)
        # log(["studyapi", "source"], res.json()["data"])
        show_kv(res.json()["data"])
        res = res.json()["data"]["studentStudyRecord"]
        return res

    # 状态
    def status(self, url: str):
        headers = {
            "authorization": self.sp.authorization,
        }
        params = {
            "product_id": "86f10208b7aa4d04b36c9600827a8272",
            "user_id": self.sp.me["id"],
            # "user_id": "78dffdacd75205314fcae1069930a0e5"
        }
        res = self.sp.session.post(f"https://urc.icve.com.cn/stage-api/{url}/status", headers=headers, params=params)
        res = res.json()
        # log(["studyapi", "video_status"], res)
        return res

    def aitoken(self, courseId):
        headers = {
            "authorization": self.sp.authorization,
            "content-type": "application/json;charset=utf-8",
        }
        ps = {
            "module": "课件学习",
            "child": {
                "id1": courseId,
                "name1": "软件测试（在线开放）",
                "type1": 2
            },
            "user_type": 1
        }
        data = {
            "params": json.dumps(ps),
            "product_id": "86f10208b7aa4d04b36c9600827a8272",
            "user_id": self.sp.me["id"]
        }
        res = self.sp.session.post("https://urc.icve.com.cn/stage-api/getOssSecret", headers=headers,
                                   data=json.dumps(data))
        res = res.json()["data"]["signature"]
        show_kv(res)
        log(["studyapi", "aitoken"], res)

    # 向服务器记录学习
    def study(self, source_data: dict):
        headers = {
            "content-type": "application/json;charset=utf-8",
            "authorization": self.sp.authorization,
        }
        data = {
            "param": encrypt_data(source_data, self.sp.authorization.split()[-1])
        }
        data = json.dumps(data).replace(" ", "")
        res = self.sp.session.post("https://zjy2.icve.com.cn/prod-api/spoc/studyRecord", headers=headers, data=data)
        res = res.json()
        return res["code"] == 200


if __name__ == '__main__':
    sp = SP()
    studyapi = StudyApi(sp)
    res = studyapi.status("doc/g@28DDD60FCBF74EED4251737BDF7DC060.mp4")
    print(res)
    pass
