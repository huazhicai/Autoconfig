from random import Random


def phonenum(numlen=11):
    num = ''
    chars = '1234567890'
    length = len(chars) - 1
    rd = Random()
    for i in range(numlen):
        num += chars[rd.randint(0, length)]
    return num


def email(numlen=9):
    email = ''
    chars = '1234567890'
    length = len(chars) - 1
    rd = Random()
    for i in range(numlen):
        email += chars[rd.randint(0, length)]
    return email + '@qq.com'

# 适用于新版本


# 配置文件
PASSWORD = '123456'
PHONE = phonenum()
EMAIL = email()


ADMIN = 'admin'
ADMIN_PASSWORD = 'sdftd11'
Plusmoney = '50000.0'


# 可能需要修改
# BASE_URL = 'http://console.listenrobot.com/'
BASE_URL = 'http://192.168.1.184/'
PREFIX = '188888221'
AIM_SN = '123456'


# 必须修改每次
USERNAME = 'seven'
INC_NAME = 'seven'
AI_NUM = '2'
start = 2
end = 3







