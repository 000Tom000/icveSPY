from utils.baseIO import log
from datetime import datetime
from models.sper import SP


class COURSEAPI():
    def __init__(self, sp: SP):
        super().__init__()
        self.sp = sp

    # 全部最近加入的课程
    def courses(self) -> list:
        headers = {
            "authorization": self.sp.authorization
        }
        params = {
            "pageNum": 1,
            "pageSize": 15,
            "currentTerm": 1
        }
        res = self.sp.session.get("https://zjy2.icve.com.cn/prod-api/spoc/courseInfoStudent/myCourseListNew",
                                  headers=headers, params=params)
        res = res.json()["rows"]
        return res
        # log(["courseapi", "courses"], res)
        # for course in res:
        #     log(["courseapi", "courses"], course)

    # 课程的全部的课堂
    def course_teaches(self, classId: str, courseId: str):
        headers = {
            "authorization": self.sp.authorization
        }
        params = {
            "pageNum": 1,
            "pageSize": 15,
            "classId": classId,
            "courseId": courseId,
            "courseInfoId": courseId,
            "isCriteria": 1
        }
        res = self.sp.session.get("https://zjy2.icve.com.cn/prod-api/spoc/courseFaceTeachInfo/student/listByDates",
                                  headers=headers, params=params)
        res = res.json()["rows"]
        return res

    # 课堂的活动
    # type=1 -> 课前
    # type=2 -> 课中[签到一般在这儿]
    # type=3 -> 课后
    def teach_activities(self, classId: str, courseId: str, teachId: str, type: int = 2) -> list:
        headers = {
            "authorization": self.sp.authorization
        }
        params = {
            "classId": classId,
            "courseId": courseId,
            "id": teachId,
            "teachId": teachId,
            "courseInfoId": courseId,
            "requireType": type
        }
        res = self.sp.session.get("https://zjy2.icve.com.cn/prod-api/spoc/courseFaceTeachInfo/v2/student/info",
                                  headers=headers, params=params)
        res = res.json()["data"]
        return res


# 选出课程名包含 course_name 的课程(第一个)
def select_course(courses: list, course_name: str) -> dict:
    for course in courses:
        if course["courseName"].find(course_name) != -1:
            return course
    return dict()


# 选出今日的课程的课堂(第一个)
def select_teach(teaches: list) -> dict:
    for teach in teaches:
        if teach["title"].find(datetime.now().strftime("%Y-%m-%d")) != -1:
            # if teach["title"].find("2026-10-27") != -1:
            return teach
    return dict()


def select_checkin_activity(classId: str, courseId: str) -> dict:
    pass


if __name__ == '__main__':
    sp = SP()
    courseapi = COURSEAPI(sp)
    # course = select_course("Web")
    # 获取所有课程
    courses = courseapi.courses()
    course = select_course(courses, "linux")
    # 获取课程的所有课堂
    teaches = courseapi.course_teaches(course["classId"], course["courseId"])
    teach = select_teach(teaches)
    # 获取课堂的所有活动(type决定课前、课中、课后，具体看函数的注释)
    activities = courseapi.teach_activities(course["classId"], course["courseId"], teach["id"])
    for activity in activities:
        if activity["title"].find("签到") != -1:
            # 执行签到
            log(["courseapi", "main_demo"], activity)
            activityId = activity["activityId"]
            # 未完成
            # 等待上课调试
            break

    # show_kv(activities[0])
