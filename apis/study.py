import json
import math
import time

from apis.course import COURSEAPI, select_course
from apis.user import USERAPI
from sper import SP
from utils.baseIO import log, show_kv
from utils.encrypt import encrypt_data


class STUDYAPI:
    def __init__(self, sp):
        super().__init__()
        self.sp = sp

    # 课程学习内容列表
    def studies(self, courseId: str, classId: str, parentId: str = "0", level: int = 1) -> list:
        headers = {
            "authorization": self.sp.authorization,
        }
        params = {
            "courseId": courseId,
            "courseInfoId": courseId,
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
            # "user_id": self.sp.me["id"],
            "user_id": "78dffdacd75205314fcae1069930a0e5"
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


# ppt学习
def ppt_study(classId: str, courseId: str, sourceId: str, start: int, end: int, name: str, studyapi: STUDYAPI):
    data = {
        "actualNum": 0,
        "classId": classId,
        "courseInfoId": courseId,
        "lastNum": 0,
        "sourceId": sourceId,
        "studyTime": 5,
        "totalNum": end
    }
    for lastNum in range(start, end + 1):
        data["actualNum"] = lastNum
        data["lastNum"] = lastNum
        success = studyapi.study(data)
        if success:
            log(["studyapi", "ppt_study"], f"{name} | 课件 | {lastNum} / {end} | 学习成功 √")
        else:
            log(["studyapi", "ppt_study"], f"{name} | 课件 | {lastNum} / {end} | 学习失败 X")
        time.sleep(0.34)


# 视频学习
def video_study(classId: str, courseId: str, sourceId: str, start: int, end: int, name: str,
                studyapi: STUDYAPI):
    data = {
        "actualNum": 0,
        "classId": classId,
        "courseInfoId": courseId,
        "lastNum": 0,
        "sourceId": sourceId,
        "studyTime": 5,
        "totalNum": end
    }
    step = 10
    for lastNum in range(start, (end // step + 1) * step + 1, step):
        if lastNum > end:
            lastNum = end
        data["actualNum"] = lastNum
        data["lastNum"] = lastNum
        success = studyapi.study(data)
        if success:
            log(["studyapi", "video_study"], f"{name} | 视频 | {lastNum} / {end} | 学习成功 √")
        else:
            log(["studyapi", "video_study"], f"{name} | 视频 | {lastNum} / {end} | 学习失败 X")
        time.sleep(0.34)


if __name__ == '__main__':
    sp = SP()
    userapi = USERAPI(sp)
    sp.me = userapi.mev2()
    courseapi = COURSEAPI(sp)
    studyapi = STUDYAPI(sp)
    # course = select_course("Web")
    # 获取所有课程
    courses = courseapi.courses()
    # course = select_course(courses, "软件测试")
    # course = select_course(courses, "Web")
    course = select_course(courses, "linux")
    # course = select_course(courses, "大模型部署")
    studies = studyapi.studies(course["courseId"], course["classId"])

    targets = list()
    # show_kv(studies[0])
    while len(studies):
        study = studies.pop(0)
        sts = studyapi.studies(course["courseId"], course["classId"], study["id"], int(study["lv"]) + 1)
        for st in sts:
            if st["speed"] == 100:
                time.sleep(0.21)
                continue
            if st["fileType"] == "子节点":
                studies.append(st)
            elif st["fileType"] == "文件夹":
                targets.extend(st["children"])
            else:
                targets.append(st)
        time.sleep(0.21)

    for target in targets:
        # print(course)
        # print(target)
        url = json.loads(target["fileUrl"])["url"]
        res = studyapi.status(url)
        if target["fileType"] == "ppt" or target["fileType"] == "txt":
            end = res["args"]["page_count"]
            start = math.floor(target["speed"] / 100 * end)
            ppt_study(course["classId"], target["courseId"], target["id"], start, end, target["name"])
        elif target["fileType"] == "video":
            duration = res["args"]["duration"]
            a = duration.split(":")
            hour = int(a[0])
            minute = int(a[1])
            second = int(a[2].split(".")[0])
            end = hour * 60 * 60 + minute * 60 + second
            start = math.floor(target["speed"] / 100 * end)
            video_study(course["classId"], target["courseId"], target["id"], start, end, target["name"])
