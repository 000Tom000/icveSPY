import time, threading
from datetime import datetime
from services.courseservice import CourseService
from services.studyservice import StudyService
from services.userservice import UserService
from models.sper import SP
from utils.baseIO import log


# 保证用户处于登录状态
def ensure_login(sp: SP):
    userservice = UserService(sp)
    # ck = userservice.me()
    # while not sp.me:
    #     userservice.login_progress()
    while not userservice.me():
        userservice.login_progress()


# 自动刷课（一个课程）
def auto_study_course(sp: SP, course_name_contains: str):
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
def ensure_checkin(sp: SP, course_name_contains: str):
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
def ensure_quick_answer(sp: SP, course_name_contains: str):
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
# time模板 "%Y-%m-%d %H:%M:%S" 或者 传入整型数值(单位为秒的时间戳)
# 例子 "2026-11-02 11:02:00" 意为 等待到2026-11-02 11:02:00
def wait_until(startTime: str | int):
    now = int(datetime.now().timestamp())
    if type(startTime) == str:
        st = int(datetime.strptime(startTime, "%Y-%m-%d %H:%M:%S").timestamp())
    else:
        st = startTime
    if now >= st:
        log(["定时"], f"{startTime} 已过，直接执行后续的程序")
    else:
        log(["定时"], f"将于 {startTime} 继续执行后续的程序，剩余 {st - now} s")
        time.sleep(st - now)


######################################################################
################################ demo ################################
######################################################################
# 自动刷课
def demo_for_auto_study_course():
    sp = SP(user="Tom")
    ensure_login(sp)
    auto_study_course(sp, "linux")
    # auto_study_course(sp, "软件测试")


# 自动签到
def demo_for_auto_checkin():
    def auto_checkin(sp, start_time: str, course_name_contains: str):
        wait_until(start_time)
        ensure_checkin(sp, course_name_contains)

    def auto_quick_answer(sp, start_time: str, course_name_contains: str):
        wait_until(start_time)
        ensure_quick_answer(sp, course_name_contains)

    sps = list()
    sps.append(SP(user="Tom"))
    # sps.append(SP(user="zs"))

    for sp in sps:
        ensure_login(sp)
        # 多线程定时任务
        # threading.Thread(target=auto_checkin, args=(sp, "2026-11-24 13:25:00", "linux",)).start()
        # threading.Thread(target=auto_checkin, args=(sp, "2026-11-23 10:15:00", "软件测试",)).start()
        # threading.Thread(target=auto_quick_answer, args=(sp, "2026-11-23 10:20:00", "软件测试",)).start()
        # threading.Thread(target=auto_checkin, args=(sp, "2026-11-23 13:25:00", "AI",)).start()
        threading.Thread(target=auto_checkin, args=(sp, "2026-11-25 8:15:00", "Web",)).start()
        # test


if __name__ == '__main__':
    demo_for_auto_checkin()
    # demo_for_auto_study_course()
