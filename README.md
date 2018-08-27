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

需要保存 cookie 以免每次都要登录？参考 [test.py](test.py)。

## api

- login `<username: str> <password: str>`

  登录失败抛出异常，登录成功返回 None

- checklogin

  已登录返回 {'error': 0}，未登录返回 {'error': 1}

- user_info

  返回用户信息，即一个字典

- online_user_ipv4

  返回在线列表，即字典的列表

- ip_login `<ip: str>`

  远程登录其它 IP

- modify_online_num `<num: int>`

  修改联网数。联网数只能是 1、2 或 3

## todo
- [ ] 远程下线
- [ ] 准入代认证
- [ ] 准入在线
- [ ] 上网明细
