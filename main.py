import json, math, time
import threading
from datetime import datetime

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
def auto_study_course(course_name_contains: str, sp: SP = None):
    if sp is None:
        sp = SP()
    courseservice = CourseService(sp)
    studyservice = StudyService(sp)

    # 课程
    course = courseservice.course(course_name_contains)
    if not course:
        return
    # 要学习的资源
    targets = studyservice.sources(course["courseId"], course["courseInfoId"], course["classId"])
    for target in targets:
        # print(course)
        # print(target)
        studyservice.study(target, course["classId"])


# 自动签到
def ensure_checkin(course_name_contains: str, sp: SP = None):
    if sp is None:
        sp = SP()
    courseservice = CourseService(sp)
    # 课程
    course = courseservice.course(course_name_contains)
    # 今日课堂
    teach = None
    while not teach:
        teach = courseservice.teach(course["classId"], course["courseId"], course["courseInfoId"])
        time.sleep(4.321)
    # 签到
    ck = -4
    while ck != 0 and ck != -2 and ck != -3:
        ck = courseservice.checkin(course["classId"], course["courseId"], teach["id"], course["courseInfoId"])
        time.sleep(4.321)


# 自动抢答
def ensure_quick_answer(course_name_contains: str, sp: SP = None):
    if sp is None:
        sp = SP()
    courseservice = CourseService(sp)
    # 课程
    course = courseservice.course(course_name_contains)
    # 今日课堂
    teach = None
    while not teach:
        teach = courseservice.teach(course["classId"], course["courseId"], course["courseInfoId"])
        time.sleep(4.321)
    # 抢答
    qka = -4
    while qka != 0 and qka != -2 and qka != -3:
        qka = courseservice.quick_answer(course["courseId"], course["courseId"], teach["id"], course["courseInfoId"])
        time.sleep(4.321)


# 定时启动
# time模板 "%Y-%m-%d %H:%M:%S"
# 例子 "2026-11-02 11:02:00" 意为等待到 "2026-11-02 11:02:00"
def wait_until(startTime: str):
    now = int(datetime.now().timestamp())
    st = int(datetime.strptime(startTime, "%Y-%m-%d %H:%M:%S").timestamp())
    if now >= st:
        log(["定时", "error"], f"{startTime} 已过，直接执行后续的程序")
    else:
        log(["定时", "info"], f"将于 {startTime} 继续执行后续的程序，剩余 {st - now} s")
        time.sleep(st - now)


if __name__ == '__main__':
    # 软件测试课的签到执行流程
    def auto_checkin_rjcs():
        wait_until("2026-11-02 10:15:00")
        ensure_checkin("软件测试")


    # 软件测试课的抢答执行流程
    def auto_quick_answer_rjcs():
        wait_until("2026-11-02 11:05:00")
        ensure_checkin("软件测试")


    # AI课的签到执行流程
    def auto_checkin_ai():
        wait_until("2026-11-02 13:20:00")
        ensure_checkin("AI")


    # 多线程检测多项活动
    checkin_rjcs_thread = threading.Thread(target=auto_checkin_rjcs)
    quick_answer_rjcs_thread = threading.Thread(target=auto_quick_answer_rjcs)
    checkin_ai_thread = threading.Thread(target=auto_checkin_ai)

    ensure_login()  # 确保用户登录
    # checkin_rjcs_thread.start()  # 软件测试课的签到执行流程 启动
    # quick_answer_rjcs_thread.start()  # 软件测试课的抢答执行流程 启动
    checkin_ai_thread.start()  # AI课的签到执行流程 启动
