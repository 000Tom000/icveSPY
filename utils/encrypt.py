import json
import hashlib
import base64
from urllib.parse import quote

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


def encrypt_data(data: dict, authorization: str):
    # MD5(e)，取前16位十六进制字符
    key = hashlib.md5(authorization.encode("utf-8")).hexdigest()[:16]

    # JSON序列化
    plaintext = json.dumps(
        data,
        ensure_ascii=False,
        separators=(",", ":")
    ).encode("utf-8")

    # AES ECB + PKCS7
    cipher = AES.new(key.encode("utf-8"), AES.MODE_ECB)
    encrypted = cipher.encrypt(pad(plaintext, AES.block_size))

    # Base64
    res = base64.b64encode(encrypted).decode("utf-8")
    res = quote(res, safe="")
    return res


if __name__ == '__main__':
    data = {
        "actualNum": 1,
        "courseInfoId": "cnvlafgvb4jadaiivxxrgw",
        "classId": "94899627-3396-47B6-91B8-4BC971D515F4",
        "lastNum": 1,
        "sourceId": "eyiaarywuznjxlxvfs0e3g",
        "studyTime": 5,
        "totalNum": 2
    }
    authorization = "eyJhbGciOiJIUzUxMiJ9.eyJ1c2VyX2lkIjoiNzhkZmZkYWNkNzUyMDUzMTRmY2FlMTA2OTkzMGEwZTUiLCJ1c2VyX2tleSI6IjI3NzdkYmIzLWYzNzAtNDcwMy1hMGU1LTM1NDMyMTc1Y2JkZSIsInVzZXJuYW1lIjoibmprajIyMDY1NDAxMTAifQ.ZMk8HLqqqvnivTzEkceKVgFDupARNmnNE08C2KKrwHxU35zBJtYtETAFtgTCVoLrvphrchtKAiRn9DotfF7MDQ"
    print(encrypt_data(data, authorization))
    print(
        "r8TdBuwMZE2YsyNys4Kq4sGe6DLLqYTTNYFx+2KTDIVSkR3/XDySm3OzkVG/ucTFrVWVqXL7qYWiyAwcowjrj2C3SfC/zAE0B5hPsqoqkWTO9VIuRDBfuUTnQn+DXRB22vTzXhfirTFCgTTZZ7EdmYLbIg2UonWzNI8HTyUJK8TUnhCn9E5LB3xdrZiQfvk6CEXOwYBRzb622ybEfvigUz5V3aoiIzsIT+n3ui9CUmxt0FmDQZQ1Yq+AwBtBFOb/")
