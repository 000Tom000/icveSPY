from datetime import datetime

from apis.courseapi import CourseApi
from models.sper import SP
from utils.baseIO import log


class CourseService:
    def __init__(self, sp: SP):
        super().__init__()
        self.sp = sp
        self.courseapi = CourseApi(self.sp)

    # 获取课程(本学期的课程)(课程名包含course_name_contains)(第一个)
    def course(self, course_name_contains: str) -> dict | None:
        courses = self.courseapi.courses()
        for course in courses:
            if course["courseName"].find(course_name_contains) != -1:
                log(["获取课程", "success"], f"获取到名为 {course['courseName']} 的课程")
                return course
        log(["获取课程", "error"], f"获取失败！")
        return None

    # 获取今日课堂(第一个)
    def teach(self, classId: str, courseId: str, courseInfoId: str) -> dict | None:
        teaches = self.courseapi.teaches(classId, courseId, courseInfoId)
        for teach in teaches:
            if teach["title"].find(datetime.now().strftime("%Y-%m-%d")) != -1:
                # if teach["title"].find("2026-10-26") != -1:
                log(["获取课堂", "success"], f"获取到名为 {teach['title']} 的课堂")
                return teach
        log(["获取课堂", "error"], f"获取失败！")
        return None

    # ["activityTypeId"]==2 -> 签到
    # ["activityTypeId"]==3 -> 提问
    # ["activityTypeId"]==3&&["asktype"]==1 -> 提问,随机选人回答(摇一摇)
    # ["activityTypeId"]==3&&["asktype"]==3 -> 提问,抢答
    # ["activityTypeId"]==4 -> 讨论
    # 获取签到活动
    def checkin_activity(self, classId: str, courseId: str, teachId: str, courseInfoId: str) -> dict | None:
        activities = self.courseapi.teach_activities(classId, courseId, teachId, courseInfoId)
        for activity in activities:
            if activity["activityTypeId"] == 2:
                log(["获取签到活动", "success"], f"获取到名为 {activity['title']} 的签到活动")
                return activity
        log(["获取签到活动", "error"], f"获取失败！")
        return None

    # 获取抢答活动
    def quick_activity(self, classId: str, courseId: str, teachId: str, courseInfoId: str) -> dict | None:
        activities = self.courseapi.teach_activities(classId, courseId, teachId, courseInfoId)
        for activity in activities:
            if activity["activityTypeId"] == 3 and activity["askType"] == 3:
                log(["获取抢答活动", "success"], f"获取到名为 {activity['title']} 的抢答活动")
                return activity
        log(["获取抢答活动", "error"], f"获取失败！")
        return None

    # 获取讨论活动
    def talk_activity(self, classId: str, courseId: str, teachId: str, courseInfoId: str) -> dict | None:
        activities = self.courseapi.teach_activities(classId, courseId, teachId, courseInfoId)
        for activity in activities:
            if activity["activityTypeId"] == 4:
                log(["获取讨论活动", "success"], f"获取到名为 {activity['title']} 的讨论活动")
                return activity
        log(["获取讨论活动", "error"], f"获取失败！")
        return None

    # 签到
    def checkin(self, classId: str, courseId: str, teachId: str, courseInfoId: str) -> int:
        activity = self.checkin_activity(classId, courseId, teachId, courseInfoId)
        if not activity:
            log(["签到", "error"], "老师还没发起签到")
            return -4
        if activity["state"] == "2":
            log(["签到", "error"], "签到已经结束了")
            return -3
        if activity["participationTime"]:
            log(["签到", "error"], "已经签过到了")
            return -2
        activityId = activity["activityId"]
        # log(["签到"], activity)
        ck = self.courseapi.checkin(classId, courseId, courseInfoId, activityId, teachId)
        return ck - 1
        # if ck:
        #     # log(["签到", "success"], "签到成功!")
        #     return 0
        # else:
        #     return -1

    # 抢答
    def quick_answer(self, classId: str, courseId: str, teachId: str, courseInfoId: str):
        activity = self.quick_activity(classId, courseId, teachId, courseInfoId)
        activityId = activity["activityId"]
        # log(["抢答"], activity)
        if not activity:
            log(["抢答", "error"], "老师还没发起抢答")
            return -4
        if activity["state"] == "2":
            log(["抢答", "error"], "抢答已经结束了")
            return -3
        if activity["participationTime"]:
            log(["抢答", "error"], "已经抢答过了")
            return -2
        qks = self.courseapi.quick_ans(classId, courseId, courseInfoId, activityId, teachId)
        return qks - 1
