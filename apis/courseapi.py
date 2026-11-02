from utils.baseIO import log
from datetime import datetime
from models.sper import SP


class CourseApi():
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
    def teaches(self, classId: str, courseId: str, courseInfoId: str):
        headers = {
            "authorization": self.sp.authorization
        }
        params = {
            "pageNum": 1,
            "pageSize": 100,
            "classId": classId,
            "courseId": courseId,
            "courseInfoId": courseInfoId,
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
    def teach_activities(self, classId: str, courseId: str, teachId: str, courseInfoId: str, type: int = 2) -> list:
        headers = {
            "authorization": self.sp.authorization
        }
        params = {
            "classId": classId,
            "courseId": courseId,
            "id": teachId,
            "requireType": type,
            "teachId": teachId,
            "courseInfoId": courseInfoId
        }
        res = self.sp.session.get("https://zjy2.icve.com.cn/prod-api/spoc/courseFaceTeachInfo/v2/student/info",
                                  headers=headers, params=params)
        res = res.json()["data"]
        return res

    # 签到
    def checkin(self, classId: str, courseId: str, courseInfoId: str, signId: str, teachId: str) -> bool:
        headers = {
            "authorization": self.sp.authorization,
            "content-type": "application/json;charset=utf-8",
        }
        data = {
            "classId": classId,
            "courseId": courseId,
            "courseInfoId": courseInfoId,
            "signId": signId,
            "signResultType": 1,
            "teachId": teachId
        }
        res = self.sp.session.post("https://zjy2.icve.com.cn/prod-api/spoc/courseFaceTeachSignStudent", headers=headers,
                                   data=data)
        res = res.json()
        if res["code"] == 200:
            log(["签到", "success"], "签到成功！")
            return True
        else:
            log(["签到", "error"], res["msg"])
            return False

    # 抢答
    def quick_ans(self, classId: str, courseId: str, courseInfoId: str, questionId: str, teachId: str):
        headers = {
            "authorization": self.sp.authorization,
            "content-type": "application/json;charset=utf-8",
        }
        data = {
            "classId": classId,
            "courseId": courseId,
            "courseInfoId": courseInfoId,
            "questionId": questionId,
            "teachId": teachId
        }
        res = self.sp.session.post(
            "https://zjy2.icve.com.cn/prod-api/spoc/courseFaceTeachQuestionStudent/preemptiveAnswer", headers=headers,
            json=data)
        res = res.json()
        if res["code"] == 200:
            log(["抢答", "success"], "抢答成功！")
            return True
        else:
            log(["抢答", "error"], res["msg"])
            return False


if __name__ == '__main__':
    courseApi = CourseApi(SP())
    res = courseApi.teach_activities("9F2C7963-806B-428C-8ABC-72081F9805A1", "waxhaqwvkqhfatywj9bepg",
                                     "44956957-A1E1-497A-8130-9B7AD8D3975B")
    print(res)
