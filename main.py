import json, math, time

from apis.courseapi import CourseApi
from apis.studyapi import StudyApi
from apis.userapi import UserApi
from services.course import CourseService
from services.study import StudyService
from services.user import UserService
from models.sper import SP
from utils.baseIO import log


# 保证用户处于登录状态
def ensure_login(sp: SP = None):
    if sp is None:
        sp = SP()
    userservice = UserService(sp)
    userservice.me()
    while not sp.me:
        userservice.login_progress()


# 自动刷课（一个课程）
# 课程名字包括 course_name_contains
def auto_study_course(course_name_contains: str, sp: SP = None):
    if sp is None:
        sp = SP()
    courseservice = CourseService(sp)
    studyservice = StudyService(sp)

    # 课程
    course = courseservice.course(course_name_contains)
    if not course:
        return
    # 要学习的内容
    targets = studyservice.sources(course["courseId"], course["courseInfoId"], course["classId"])
    # 要学习的课件(具体)
    for target in targets:
        # print(course)
        # print(target)
        studyservice.study(target, course["classId"])


# 自动签到
def auto_checkin(course_name_contains: str, sp: SP = None):
    if sp is None:
        sp = SP()
    courseservice = CourseService(sp)
    # 课程
    course = courseservice.course(course_name_contains)
    # 今日课堂
    teach = courseservice.teach(course["classId"], course["courseId"], course["courseInfoId"])
    # 签到
    courseservice.checkin(course["classId"], course["courseId"], teach["id"], course["courseInfoId"])


if __name__ == '__main__':
    sp = SP()
    ensure_login(sp)
    # auto_checkin("linux")

    auto_study_course("软件测试")
    # auto_study_course("AI")
    # auto_study_course("linux")
    # auto_study_course("Web")
