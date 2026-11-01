import pathlib

ROOT = pathlib.Path(__file__).parent.resolve()
APIS_DIR = ROOT / "apis"
CACHES_DIR = ROOT / "caches"
LOGS_DIR = ROOT / "logs"
# 缓存文件
AUTH_FILE = CACHES_DIR / "authorization"
COOKIES_FILE = CACHES_DIR / "cookies.json"
ME_FILE = CACHES_DIR / "me.json"
STUDIES_FILE = CACHES_DIR / "studies.json"
# 日志文件
STUDY_LOG_FILE = LOGS_DIR / "study.log"
USER_LOG_FILE = LOGS_DIR / "user.log"
MAIN_LOG_FILE = LOGS_DIR / "main.log"
