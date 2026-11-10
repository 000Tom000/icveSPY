import pathlib

ROOT = pathlib.Path(__file__).parent.resolve()
# 缓存
CACHES_DIR = ROOT / "caches"
AUTH_FILE = CACHES_DIR / "authorization"
COOKIES_FILE = CACHES_DIR / "cookies.json"
ME_FILE = CACHES_DIR / "me.json"

# 日志
LOGS_DIR = ROOT / "logs"
INFO_LOG_FILE = LOGS_DIR / "info.log"
SUCC_LOG_FILE = LOGS_DIR / "success.log"
ERROR_LOG_FILE = LOGS_DIR / "error.log"
DEBUG_LOG_FILE = LOGS_DIR / "debug.log"
