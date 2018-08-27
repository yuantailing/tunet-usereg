import getpass
import os

from pprint import pprint
from six.moves import http_cookiejar, input
from usereg import usereg

if __name__ == '__main__':
    jar = http_cookiejar.MozillaCookieJar('cookie.txt')
    if jar.filename and os.path.isfile(jar.filename):
        jar.load(ignore_discard=True, ignore_expires=True)

    agent = usereg(jar)
    if agent.checklogin()['error']:
        username = input('Username: ')
        password = getpass.getpass()
        agent.login(username, password)
    pprint(agent.user_info())
    pprint(agent.online_user_ipv4())

    if jar.filename:
        jar.save(ignore_discard=True, ignore_expires=True)
