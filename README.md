# tunet-usereg
[usereg.tsinghua.edu.cn](https://usereg.tsinghua.edu.cn) 的 Python 接口，可查询在线状态、远程下线、连接其它 IP、修改联网数

## usage

兼容 Python 2 和 Python 3，建议使用 Python 3，以便显示中文字符

```python
from pprint import pprint
from six.moves import http_cookiejar
from usereg import usereg

jar = http_cookiejar.MozillaCookieJar()  # 创建 cookie
agent = usereg(jar)
agent.login('username', 'password')      # 登录
pprint(agent.user_info())                # 打印用户信息
pprint(agent.online_user_ipv4())         # 打印在线列表
```

避免每次都要重新登录？需要保存 cookie，参考 [test.py](test.py)。

## api

- login `<username: str> <password: str>`

  登录失败抛出异常，登录成功返回 None

- logout

  登出。无论原来是否在线都会返回 None

- checklogin

  已登录返回 {'error': 0}，未登录返回 {'error': 1}
  
  *注：以下 API 只能在已登录状态下调用，否则抛出异常*

- user_info

  返回用户信息，即一个字典

- online_user_ipv4

  返回在线列表，即字典的列表

- ip_login `<ip: str>`

  远程登录其它 IP

- drops `<ip: str>`

  远程下线指定 IP。IP 必须在在线列表里，否则抛出异常

- modify_online_num `<num: int>`

  修改联网数。联网数只能是 1、2 或 3

- import_online_user

  返回准入在线列表，即字典的列表

- drops_import `<ip: str>`

  准入下线。IP 必须在准入在线列表里，否则抛出异常

## todo
- [x] 远程下线
- [ ] 准入代认证
- [x] 准入在线
- [x] 准入下线
- [ ] 上网明细
- [ ] 准入上网明细
