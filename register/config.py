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


# 配置文件
PASSWORD = '123456'
PHONE = phonenum()
EMAIL = email()

ADMIN = 'admin'
ADMIN_PASSWORD = 'sdfsdfls1'
Plusmoney = '50000.0'

# 需要修改
BASE_URL = 'http://console.lsfhxc.com/'

PREFIX = '188880341'
AIM_SN = '2c4d5446f883'

# 必须修改每次
USERNAME = 'hzls_wangpaiyun211'
INC_NAME = '王牌云财税'
AI_NUM = '2'
start = 26
end = 27
