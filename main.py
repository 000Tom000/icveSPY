import json
import math
import time

from apis.course import COURSEAPI
from apis.study import STUDYAPI, ppt_study, video_study
from apis.user import USERAPI
from sper import SP
from utils.baseIO import log


# 自动刷课
# 课程名字包括 course_name_contains
def auto_study_course(course_name_contains: str):
    global sp, userapi, courseapi, studyapi
    # 所有课程
    log(["自动刷课", "info"], "正在获取 最新课程列表 ...")
    courses = courseapi.courses()
    log(["自动刷课", "success"], "成功获取到 最新课程列表 ")
    log(["自动刷课", "data"], courses)
    # 找出目标课程
    course = None
    for cour in courses:
        if cour["courseName"].find(course_name_contains) != -1:
            course = cour
            log(["自动刷课", "success"], f"成功找到 课程名 含有 {course_name_contains} 的课程")
            log(["自动刷课", "data"], course)
            break

    if not course:
        log(["自动刷课", "error"], f"未从 最新课程列表 中找到 课程名 含有 {course_name_contains} 的目标课程")
        log(["自动刷课", "info"], "程序over...")
        exit(0)
    # 要学习的内容
    log(["自动刷课", "info"], "开始拉取 所有学习内容的折叠项 ...")
    studies = studyapi.studies(course["courseId"], course["classId"])
    log(["自动刷课", "success"], f"拉取到 {len(studies)}个 折叠项")
    log(["自动刷课", "info"], f"开始展开 所有折叠项")
    targets = list()
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
                for st_child in st["children"]:
                    if st_child["speed"] != 100:
                        targets.append(st_child)
            else:
                targets.append(st)
        time.sleep(0.21)
    # 要学习的课件(具体)
    log(["自动刷课", "success"], f"成功展开出 {len(targets)}个 学习目标课件")
    for target in targets:
        # print(course)
        # print(target)
        url = json.loads(target["fileUrl"])["url"]
        res = studyapi.status(url)
        if target["fileType"] == "ppt" or target["fileType"] == "txt" or target["fileType"] == "doc":
            end = res["args"]["page_count"]
            start = math.floor(target["speed"] / 100 * end)
            ppt_study(course["classId"], target["courseId"], target["id"], start, end, target["name"], studyapi)
        elif target["fileType"] == "video":
            duration = res["args"]["duration"]
            a = duration.split(":")
            hour = int(a[0])
            minute = int(a[1])
            second = int(a[2].split(".")[0])
            end = hour * 60 * 60 + minute * 60 + second
            start = math.floor(target["speed"] / 100 * end)
            video_study(course["classId"], target["courseId"], target["id"], start, end, target["name"], studyapi)
        elif target["fileType"] == "img":
            ppt_study(course["classId"], target["courseId"], target["id"], 0, 1, target["name"], studyapi)


if __name__ == '__main__':
    sp = SP()
    userapi = USERAPI(sp)
    sp.me = userapi.mev2()
    courseapi = COURSEAPI(sp)
    studyapi = STUDYAPI(sp)
    auto_study_course("软件测试")
    # auto_study_course("大模型部署")
    # auto_study_course("linux")
    # auto_study_course("Web")
