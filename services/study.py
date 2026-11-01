import collections
import json
import math
import time

from apis.studyapi import StudyApi
from models.sper import SP
from utils.baseIO import log


class StudyService:
    def __init__(self, sp: SP):
        super().__init__()
        self.sp = sp
        self.studyapi = StudyApi(self.sp)

    # 学习内容
    def sources(self, courseId: str, courseInfoId: str, classId: str):
        log(["获取学习内容", "info"], "正在获取学习资源，该过程可能耗时较长，请耐心等待 ...")
        studies = self.studyapi.studies(courseId, courseInfoId, classId)
        studies = collections.deque(studies)
        targets = list()
        while studies:
            study = studies.popleft()
            sts = self.studyapi.studies(courseId, courseInfoId, classId, study["id"], int(study["lv"]) + 1)
            for st in sts:
                if st["speed"] == 100:
                    time.sleep(0.21)
                    continue
                if st["fileType"] == "子节点":
                    studies.append(st)
                elif st["fileType"] == "文件夹":
                    for st_child in st["children"]:
                        if st_child["speed"] != 100:
                            targets.append(st_child)
                else:
                    targets.append(st)
            time.sleep(0.21)
        log(["获取学习内容", "info"], f"获取到 {len(targets)} 个学习资源")
        return targets

    # ppt学习
    def ppt_study(self, classId: str, courseInfoId, sourceId: str, start: int, end: int, name: str):
        data = {
            "actualNum": 0,
            "classId": classId,
            "courseInfoId": courseInfoId,
            "lastNum": 0,
            "sourceId": sourceId,
            "studyTime": 5,
            "totalNum": end
        }
        for lastNum in range(start, end + 1):
            data["actualNum"] = lastNum
            data["lastNum"] = lastNum
            success = self.studyapi.study(data)
            if success:
                log(["学习", "success"], f"{name} | 课件 | {lastNum} / {end} | 学习成功 √")
            else:
                log(["学习", "error"], f"{name} | 课件 | {lastNum} / {end} | 学习失败 X")
            time.sleep(0.34)

    # 视频学习
    def video_study(self, classId: str, courseInfoId: str, sourceId: str, start: int, end: int,
                    name: str):
        data = {
            "actualNum": 0,
            "classId": classId,
            "courseInfoId": courseInfoId,
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
            success = self.studyapi.study(data)
            if success:
                log(["学习", "success"], f"{name} | 视频 | {lastNum} / {end} | 学习成功 √")
            else:
                log(["学习", "error"], f"{name} | 视频 | {lastNum} / {end} | 学习失败 X")
            time.sleep(0.34)

    # 学习
    def study(self, target: dict, classId: str):
        url = json.loads(target["fileUrl"])["url"]
        res = self.studyapi.status(url)
        if res.get("code", 200) == 500:
            log(["学习", "error"], res["msg"])
            return
        if res.get("status", 2) < 0:
            log(["学习", "error"], "该课件有问题，请手动学习")
            return
        if target["fileType"] == "ppt" or target["fileType"] == "txt" or target["fileType"] == "doc":
            end = res["args"]["page_count"]
            start = math.floor(target["speed"] / 100 * end)
            self.ppt_study(classId, target["courseInfoId"], target["id"], start, end, target["name"])
        elif target["fileType"] == "video":
            duration = res["args"]["duration"]
            a = duration.split(":")
            hour = int(a[0])
            minute = int(a[1])
            second = int(a[2].split(".")[0])
            end = hour * 60 * 60 + minute * 60 + second
            start = math.floor(target["speed"] / 100 * end)
            self.video_study(classId, target["courseInfoId"], target["id"], start, end, target["name"])
        elif target["fileType"] == "img":
            self.ppt_study(classId, target["courseInfoId"], target["id"], 0, 1, target["name"])


if __name__ == '__main__':
    pass
