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
            # if teach["title"].find(datetime.now().strftime("%Y-%m-%d")) != -1:
            if teach["title"].find("2026-10-27") != -1:
                log(["获取课堂", "success"], f"获取到名为 {teach['title']} 的课堂")
                return teach
        log(["获取课堂", "error"], f"获取失败！")
        return None

    # 获取签到活动
    def checkin_activity(self, classId: str, courseId: str, teachId: str, courseInfoId: str) -> dict | None:
        activities = self.courseapi.teach_activities(classId, courseId, teachId, courseInfoId)
        for activity in activities:
            if activity["title"].find("签到") != -1:
                log(["获取签到活动", "success"], f"获取到名为 {activity['title']} 的签到活动")
                return activity
        log(["获取签到活动", "error"], f"获取失败！")
        return None

    # 签到
    def checkin(self, classId: str, courseId: str, teachId: str, courseInfoId: str):
        activity = self.checkin_activity(classId, courseId, teachId, courseInfoId)
        activityId = activity["activityId"]
        log(["checkservice", "checkin"], activity)
        # 待实现
