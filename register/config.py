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
# ADMIN_PASSWORD = 'sdfsdfls1'
ADMIN_PASSWORD = 'sdftd11'
Plusmoney = '320000.0'

# 可能需要修改
# BASE_URL = 'http://console.lsfhxc.com/'
# 191服务器
# PREFIX = '188880342'
# AIM_SN = '2c4d5446f883'

# # 190服务器
# PREFIX = '188333300'
# AIM_SN = '123456'


# 必须修改每次
USERNAME = 'hengyun'
INC_NAME = 'hengyun'
AI_NUM = '32'
start = 1
end = 4

# 装机测试
BASE_URL = 'http://27.184.59.195:666/'
PREFIX = '188888802'
AIM_SN = '001e67fecc65'


# # 可能需要修改(西安)
# BASE_URL = 'http://xian.synvn.com:666/'
# PREFIX = '188888802'
# AIM_SN = 'a4bf0119ef8f'



#
# # 可能需要修改(sjz)
# BASE_URL = 'http://xian.synvn.com:666/'
# PREFIX = '188888802'
# AIM_SN = 'a4bf0119ef8f'