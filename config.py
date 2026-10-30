import pathlib

ROOT = pathlib.Path(__file__).parent.resolve()
APIS_DIR = ROOT / "apis"
CACHES_DIR = ROOT / "caches"
AUTH_FILE = CACHES_DIR / "authorization"
COOKIES_FILE = CACHES_DIR / "cookies.json"
ME_FILE = CACHES_DIR / "me.json"