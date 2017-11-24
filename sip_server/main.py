from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from sip_server.config import *
from time import sleep

browser = webdriver.Chrome()
# browser.set_window_size(1400, 900)
browser.maximize_window()
wait = WebDriverWait(browser, 90)


def login():
    try:
        browser.get('https://{}'.format(BASE_IP))
        # 用户名
        input1 = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#input_user'))
        )
        input1.send_keys(USERNAME)
        # 输入秘密
        input2 = wait.until(
                EC.presence_of_element_located(
                        (By.CSS_SELECTOR, 'body > div > div.login-form > div > form > div:nth-child(2) > div > input'))
        )
        input2.send_keys(PASSWORD)
        # 点击登录
        submit = wait.until(
                EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, 'body > div > div.login-form > div > form > div:nth-child(3) > button'))
        )
        submit.click()
        print('登录成功')
    except TimeoutException:
        print('登录失败')
        login()


# 配置add sip trunk
def trunk_config():
    try:
        browser.get('https://{}/config.php?display=trunks&tech=SIP'.format(BASE_IP))
        # trunk name
        input1 = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR,
                                                '#page_body > form > table > tbody > tr:nth-child(2) > td:nth-child(2) > input[type="text"]'))
        )
        input1.clear()
        input1.send_keys(TRUNK_NAME)

        # Trunk name
        input2 = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR,
                                                '#page_body > form > table > tbody > tr:nth-child(17) > td:nth-child(2) > input[type="text"]'))
        )
        input2.clear()
        input2.send_keys(TRUNK_NAME)

        # peer detail
        input3 = wait.until(
                EC.presence_of_element_located(
                        (By.CSS_SELECTOR, '#page_body > form > table > tbody > tr:nth-child(19) > td > textarea'))
        )
        input3.clear()
        input3.send_keys(HOST_PORT)

        # 提交更改
        submit = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="page_body"]/form/table/tbody/tr[26]/td/h6/input[1]'))
        )
        submit.click()
        a1 = browser.switch_to.alert
        sleep(1)
        a1.accept()
        print('配置trunk成功')
    except TimeoutException:
        print('配置中继器失败')
        trunk_config()


# 配置分机号
def add_extension(number):
    try:
        browser.get('https://{}/index.php?menu=pbxadmin'.format(BASE_IP))
        # 点击进入配置界面
        submit = wait.until(
                EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, '#page_body > form > table > tbody > tr:nth-child(5) > td > h6 > input'))
        )
        submit.click()

        # User extension
        input1 = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#extension'))
        )
        input1.clear()
        input1.send_keys(PREFIX + number)

        # Display name
        input2 = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#name'))
        )
        input2.clear()
        input2.send_keys(DISPLAY + number)

        # Secret
        input3 = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#devinfo_secret'))
        )
        input3.clear()
        input3.send_keys(SECRET)

        # 提交更改
        submit2 = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="page_body"]/form/table/tbody/tr[98]/td/h6/input'))
        )
        submit2.click()
        print('配置分机号成功{}'.format(number))
    except TimeoutException:
        print('配置分机失败')
        add_extension(number)


# 配置呼出路由(outbound route)
def outbound_route(num):
    try:
        browser.get('https://{}/config.php?display=routing&extdisplay=1'.format(BASE_IP))

        # 复制路由摸板
        submit1 = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR,
                                            '#routeEdit > table > tbody > tr:nth-child(24) > td > h6 > input:nth-child(2)'))
        )
        submit1.click()

        # Route Name
        input1 = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR,
                                                '#routeEdit > table > tbody > tr:nth-child(2) > td:nth-child(2) > input[type="text"]'))
        )
        input1.clear()
        input1.send_keys(DISPLAY + num)

        # Route CID
        input2 = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR,
                                                '#routeEdit > table > tbody > tr:nth-child(3) > td:nth-child(2) > input[type="text"]:nth-child(1)'))
        )
        input2.clear()
        input2.send_keys(PREFIX + num)

        # Dial route
        # 清空中间的9
        input3 = wait.until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="pattern_prefix_0"]'))
        )
        input3.clear()

        # # 填前面
        # input4 = wait.until(
        #         EC.presence_of_element_located((By.XPATH, '//*[@id="pattern_prefix_0"]'))
        # )
        # 填后面
        input4 = wait.until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="match_cid_0"]'))
        )
        input4.clear()
        input4.send_keys(PREFIX + num)


        # 选择中继器
        sel = Select(browser.find_element_by_id('trunkpri0'))  # 实例化Select
        sel.select_by_visible_text(TRUNK_NAME)  # 选择中继器

        # 提交更改
        submit2 = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="routeEdit"]/table/tbody/tr[24]/td/h6/input[1]'))
        )
        submit2.click()
        print('配置呼出路由成功{}'.format(num))
    except TimeoutException:
        print('配置呼出路由失败')
        outbound_route(num)


def featurecode():
    try:
        browser.get('https://{}/?menu=pbxconfig&type=setup&display=featurecodeadmin'.format(BASE_IP))
        # 实例化
        sel = Select(browser.find_element_by_name('ena#blacklist#blacklist_add'))  # 实例化Select
        sel.select_by_visible_text('Disabled')

        se2 = Select(browser.find_element_by_name('ena#blacklist#blacklist_last'))
        se2.select_by_value('0')

        se3 = Select(browser.find_element_by_name('ena#blacklist#blacklist_remove'))  # 实例化Select
        se3.select_by_visible_text('Disabled')

        se4 = Select(browser.find_element_by_name('ena#callforward#cfon'))
        se4.select_by_value('0')

        se5 = Select(browser.find_element_by_name('ena#callforward#cfoff'))  # 实例化Select
        se5.select_by_visible_text('Disabled')

        se6 = Select(browser.find_element_by_name('ena#callforward#cfpon'))
        se6.select_by_value('0')

        se7 = Select(browser.find_element_by_name('ena#callforward#cfoff_any'))  # 实例化Select
        se7.select_by_visible_text('Disabled')

        se8 = Select(browser.find_element_by_name('ena#callforward#cfbon'))
        se8.select_by_value('0')

        se9 = Select(browser.find_element_by_name('ena#callforward#cfboff'))  # 实例化Select
        se9.select_by_visible_text('Disabled')

        se10 = Select(browser.find_element_by_name('ena#callforward#cfbpon'))
        se10.select_by_value('0')

        se11 = Select(browser.find_element_by_name('ena#callforward#cfboff_any'))  # 实例化Select
        se11.select_by_visible_text('Disabled')

        se12 = Select(browser.find_element_by_name('ena#callforward#cfuon'))
        se12.select_by_value('0')

        se13 = Select(browser.find_element_by_name('ena#callforward#cfupon'))  # 实例化Select
        se13.select_by_visible_text('Disabled')

        se14 = Select(browser.find_element_by_name('ena#callforward#cf_toggle'))
        se14.select_by_value('0')

        se15 = Select(browser.find_element_by_name('ena#callwaiting#cwon'))  # 实例化Select
        se15.select_by_visible_text('Disabled')

        se16 = Select(browser.find_element_by_name('ena#callwaiting#cwoff'))
        se16.select_by_value('0')

        se17 = Select(browser.find_element_by_name('ena#timeconditions#toggle-mode-all'))  # 实例化Select
        se17.select_by_visible_text('Disabled')

        se18 = Select(browser.find_element_by_name('ena#voicemail#dialvoicemail'))
        se18.select_by_value('0')

        se19 = Select(browser.find_element_by_name('ena#voicemail#directdialvoicemail'))  # 实例化Select
        se19.select_by_visible_text('Disabled')

        se20 = Select(browser.find_element_by_name('ena#voicemail#myvoicemail'))
        se20.select_by_value('0')

        # 保存
        browser.find_element_by_css_selector('#page_body > form > table > tbody > tr:nth-child(81) > td > h6 > input').click()
    except:
        pass


def main():
    login()
    trunk_config()  # 添加中继
    # 配置分机和呼出路由
    for i in range(start, end+1):
        if i < 10:
            i = '0' + str(i)
            add_extension(i)
            outbound_route(i)
        else:
            add_extension(str(i))
            outbound_route(str(i))
    featurecode()
    # apply config #button_reload
    submit3 = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#button_reload'))
    )
    submit3.click()
    browser.close()


if __name__ == '__main__':
    main()

