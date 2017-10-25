from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from register.config import *
from time import sleep

browser = webdriver.Chrome()
browser.maximize_window()
wait = WebDriverWait(browser, 60)


def register():
    try:
        browser.get('{}auth/register'.format(BASE_URL))
        # 电子邮箱
        input1 = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#email'))
        )
        input1.send_keys(EMAIL)
        # 用户名
        input2 = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#username'))
        )
        input2.send_keys(USERNAME)
        # 输入秘密
        input3 = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#password'))
        )
        input3.send_keys(PASSWORD)
        # 确认秘密
        input4 = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#password2'))
        )
        input4.send_keys(PASSWORD)
        # 企业名称
        input4 = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#inc_name'))
        )
        input4.send_keys(INC_NAME)
        # 联系电话
        input5 = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#phone'))
        )
        input5.send_keys(PHONE)
        # 注册
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#reg'))
        )
        submit.click()

        print('注册成功')
        return True
    except TimeoutException:
        print('注册失败')
        register()


def admin_login():
    try:
        browser.get('{}auth/login?next=%2F'.format(BASE_URL))
        # 管理员账号
        input1 = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#email'))
        )
        input1.send_keys(ADMIN)
        # 管理员密码
        input2 = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#password'))
        )
        input2.send_keys(ADMIN_PASSWORD)
        # 登录
        submit = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#login_form > div:nth-child(6) > input'))
        )
        submit.click()
    except TimeoutException:
        print('登录失败')
        admin_login()


def edit_user():
    try:
        browser.get('{0}admin/user/?search={1}'.format(BASE_URL, USERNAME))
        # 编辑
        edit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div > table > tbody > tr > td.list-buttons-column > a:nth-child(1) > span'))
        )
        edit.click()
        # 审核
        submit1 = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#active'))
        )
        submit1.click()
        # 用户ai数据
        input2 = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#ai_num'))
        )
        input2.clear()
        input2.send_keys(AI_NUM)
        # Aim Sn
        input3 = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#aim_sn'))
        )
        input3.clear()
        input3.send_keys(AIM_SN)
        # 邮件确认
        submit3 = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#confirmed'))
        )
        submit3.click()
        # 保存
        submit4 = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.container > form > div:nth-child(38) > div > input.btn.btn-primary'))
        )
        submit4.click()

        # ai组配置
        submit5 = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div > table > tbody > tr > td.list-buttons-column > a:nth-child(3) > span'))
        )
        submit5.click()
        # 用户ai组数据
        input4 = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#ai_num'))
        )
        input4.clear()
        input4.send_keys(AI_NUM)
        # 保存
        submit5 = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.container > form > div:nth-child(16) > div > input.btn.btn-primary'))
        )
        submit5.click()
        print('认证通过')
    except TimeoutException:
        print('编辑资料失败')
        edit_user()


def add_money():
    try:
        browser.get('{0}admin/user/?search={1}'.format(BASE_URL, USERNAME))
        # 充值虚拟货币
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div > table > tbody > tr > td.list-buttons-column > a:nth-child(4) > span'))
        )
        submit.click()
        # 充值金额
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#money'))
        )
        input.clear()
        input.send_keys(Plusmoney)
        # 保存
        submit2 = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.container > form > div:nth-child(12) > div > input.btn.btn-primary'))
        )
        submit2.click()
        print('充值成功{}'.format(Plusmoney))
    except TimeoutException:
        print('充值失败')
        add_money()


def create_mobile(number):
    phone = PREFIX + number
    try:
        browser.get('{}admin/mphonenum/new/?url=%2Fadmin%2Fmphonenum%2F'.format(BASE_URL))
        # 移动主叫账号
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#phone'))
        )
        input.send_keys(phone)
        # 输入用户
        submit1 = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#s2id_mowner > a'))
        )
        submit1.click()
        input2 = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#s2id_autogen1_search'))
        )
        input2.send_keys(USERNAME)
        input2.send_keys(Keys.ENTER)
        # 保存
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.container > form > div:nth-child(9) > div > input.btn.btn-primary'))
        )
        submit.click()
        print('移动主叫创建成功{}'.format(phone))
    except TimeoutException:
        print('创建移动主叫失败')
        create_mobile(number)


def main():
    # 注册账号
    register()
    # 认证
    admin_login()
    edit_user()
    add_money()
    # 分配号码
    for i in range(start, end+1):
        if i < 10:
            i = '0' + str(i)
            create_mobile(number=str(i))
        else:
            create_mobile(number=str(i))
    print('Successfully')
    # 必须关，因为你懂得
    browser.quit()


if __name__ == '__main__':
    main()



