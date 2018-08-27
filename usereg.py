# -*- coding: UTF-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import hashlib

from bs4 import BeautifulSoup
from six.moves import http_cookiejar, urllib
from six.moves.urllib.request import build_opener, HTTPCookieProcessor


class usereg:
    BASEURL = 'https://usereg.tsinghua.edu.cn/'

    def __init__(self, jar):
        self._opener = build_opener(HTTPCookieProcessor(jar))

    def _open(self, fullurl, data=None):
        if data is None:
            return self._opener.open(fullurl)
        return self._opener.open(fullurl, urllib.parse.urlencode(data).encode())

    def login(self, username, password):
        request = self._open(usereg.BASEURL + 'do.php', dict(
                action='login',
                user_login_name=username.encode(),
                user_password=hashlib.md5(password.encode()).hexdigest(),
            )
        )
        assert 200 == request.code
        content = request.read().decode('gb2312', 'ignore')
        assert 'ok' == content, 'password incorrect'

    def logout(self):
        request = self._open(usereg.BASEURL + 'do.php', dict(
                action='logout',
            )
        )
        assert 200 == request.code
        content = request.read().decode('gb2312', 'ignore')
        print(content)
        assert 'ok' == content

    def checklogin(self):
        request = self._open(usereg.BASEURL + 'main.php')
        assert 200 == request.code
        return dict(
            error=0 if request.url.endswith('main.php') else 1,
        )

    def user_info(self):
        request = self._open(usereg.BASEURL + 'user_info.php')
        assert 200 == request.code
        content = request.read().decode('gb2312')
        soup = BeautifulSoup(content, 'html.parser')
        tds = [
            td.get_text().replace('\xa0', ' ').strip()
            if td.find('input') is None else td.find('input').get('value')
            for td in soup.find_all('td')
        ]
        return {
            k: tds[tds.index(k) + 1]
            for k in '用户名 用户组 姓名 部门 证件号 邮件地址 固定电话 '
            '移动电话 住址 当前计费组 结算日期 使用时长(IPV4) '
            '使用流量(IPV4) 使用时长(IPV6) 使用流量(IPV6) 帐户余额 '
            '可用余额 用户状态'.split()
        }

    def _online_user(self, portal):
        request = self._open(usereg.BASEURL + portal)
        assert 200 == request.code
        content = request.read().decode('gb2312')
        soup = BeautifulSoup(content, 'html.parser')
        trs = [
            [
                td.get_text().replace('\xa0', ' ').strip()
                if td.find('input') is None else td.find('input').get('value')
                for td in tr.find_all('td')
            ] for tr in soup.find_all('tr', {'align': 'center'})
        ]
        trs[0][0] = 'id'
        return [
            dict(zip(trs[0], td)) for td in trs[1:]
        ]

    def _drops(self, protal, ip):
        ls = self._online_user(protal)
        ls = [o for o in ls if o.get('IP') == ip]
        assert 1 <= len(ls), 'IP not in online list'
        request = self._open(usereg.BASEURL + protal, dict(
                action='drops',
                user_ip=ls[0].get('id', ''),
            )
        )
        assert 200 == request.code
        content = request.read().decode('gb2312')
        assert '下线请求已发送' in content, content

    def online_user_ipv4(self):
        return self._online_user('online_user_ipv4.php')

    def ip_login(self, ip):
        request = self._open(usereg.BASEURL + 'ip_login.php', dict(
                n='100',
                is_pad='1',
                type='10',
                action='do_login',
                user_ip=ip,
                drop='0',
            )
        )
        assert 200 == request.code
        content = request.read().decode('gb2312')
        assert '上线请求已发送' in content, content

    def drops(self, ip):
        return self._drops('online_user_ipv4.php', ip)

    def modify_online_num(self, num):
        request = self._open(usereg.BASEURL + 'modify_online_num.php', dict(
                action='mod',
                user_max_online_num='{:d}'.format(num),
            )
        )
        assert 200 == request.code
        content = request.read().decode('gb2312')
        assert '联网数已修改' in content, content

    def import_online_user(self):
        return self._online_user('import_online_user.php')

    def drops_import(self, ip):
        return self._drops('import_online_user.php', ip)
