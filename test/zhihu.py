import requests
from bs4 import BeautifulSoup
import os, time
import re
# import http.cookiejar as cookielib

# 构造 Request headers
agent = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36'
headers = {
    "Host": "www.zhihu.com",
    "Referer": "https://www.zhihu.com/",
    'User-Agent': agent
}


# 构造用于网络请求的session
session = requests.Session()
# session.cookies = cookielib.LWPCookieJar(filename='zhihucookie')
# try:
#     session.cookies.load(ignore_discard=True)
# except:
#     print('cookie 文件未能加载')