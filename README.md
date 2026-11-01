# 智慧职教(执教云) 自动化管理

+ 实现自动化管理自己的账号，包括自动签到、自动刷课 ······

## 版本 v1.0

### 新增功能

+ 用户持久化登录
+ 自动刷课

### 主要功能

+ 用户持久化登录
+ 自动刷课

## 项目结构

|       结构        | 文件类别 |  定义  |      作用      |  改动推荐   |
|:---------------:|:----:|:----:|:------------:|:-------:|
|      apis       |  包   |  接口  |  只负责发送网络请求   |   不推荐   |   
|    services     |  包   |  业务  | 直接调用api的类方法  |   一般    |
|     models      |  包   | 模板类  |   以对象管理变量    |   不推荐   |
|      utils      |  包   |  工具  |  给程序提供辅助工具   |   不推荐   |
|     caches      | 文件夹  |  缓存  |     存缓存      | **不可能** |
|      logs       | 文件夹  |  日志  |     存日志      | **不可能** |
|     main.py     |  文件  | 程序入口 |    梦开始的地方    |   推荐    |
|    config.py    |  文件  | 配置文件 |    负责配置路径    | **不可能** |
| requirement.txt |  文件  |  依赖  | 必须在运行程序前安装依赖 | **不可能** |

## 使用者须知

+ 使用者在pull下这个项目的第一步应该是根据 **requirements.txt** 文件下载对应的依赖，在项目文件夹下打开终端(terminal)
  ，运行下方的命令

```bash

pip install -r requirements.txt
```

+ 上述命令下载依赖缓慢，可以运行下方的命令

```bash

pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

+ 约定 **sp** 作为一个爬虫子，是整个爬虫操作中最重要的一个对象

```python
from models.sper import SP

sp = SP()  # 一个爬虫子
print(sp)  # 打印sp对象
```

+ 如果使用者想调用 **services包** 中某个写好的业务，导入具体的 **service类** 以实现，同时还要传入 **sp** 爬虫子对象

```python
from models.sper import SP
from services.user import UserService

sp = SP()  # 一个爬虫子
userservice = UserService(sp)  # user相关的api
userservice.login_progress()  # 调用扫码登录业务
```

+ 如果使用者想调用 **apis包** 中某个写好的 **api**，导入具体的 **api类** 以实现，同时还要传入 **sp** 爬虫子对象

```python
from models.sper import SP
from apis.userapi import UserApi

sp = SP()  # 一个爬虫子
userapi = UserApi(sp)  # user相关的api
userapi.mev2()  # 获取当前用户信息
```

## 作者

| ![IMG_2773.JPG](author/wechat.JPG) | ![IMG_2773.JPG](author/wechat.JPG) |
|------------------------------------|------------------------------------|

## 声明

+ 该项目仅用于参考与学习，欢迎大家与作者交流
+ 但若该项目被用于其他用途，一经发现必定追究其责任

## License

Copyright © 2026 Tom.

This project is licensed under the [MIT License](LICENSE).
