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
wait = WebDriverWait(browser, 80)


def login():
    try:
        browser.get('http://{}/'.format(BASE_IP))
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


# 配置呼出路由(outbound route)
def outbound_route(id, num):
    try:
        # https://192.168.11.180/config.php?display=routing&extdisplay=9
        browser.get('https://{0}/config.php?display=routing&extdisplay={1}'.format(BASE_IP, id))

        # # Route Name
        # input1 = wait.until(
        #         EC.presence_of_element_located((By.CSS_SELECTOR,
        #                                         '#routeEdit > table > tbody > tr:nth-child(2) > td:nth-child(2) > input[type="text"]'))
        # )
        # input1.clear()
        # input1.send_keys(DISPLAY + num)
        #
        # # Route CID
        # input2 = wait.until(
        #         EC.presence_of_element_located((By.CSS_SELECTOR,
        #                                         '#routeEdit > table > tbody > tr:nth-child(3) > td:nth-child(2) > input[type="text"]:nth-child(1)'))
        # )
        # input2.clear()
        # input2.send_keys(PREFIX + num)

        # Dial route
        input3 = wait.until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="pattern_prefix_0"]'))
        )
        input3.clear()

        # Dial route
        input4 = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#match_cid_0'))
        )
        input4.clear()
        input4.send_keys(PREFIX + num)
        #
        # # 选择中继器
        # sel = Select(browser.find_element_by_id('trunkpri0'))  # 实例化Select
        # sel.select_by_visible_text(TRUNK_NAME)  # 选择中继器

        # 提交更改#routeEdit > table > tbody > tr:nth-child(24) > td > h6 > input:nth-child(1)
        submit2 = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '#routeEdit > table > tbody > tr:nth-child(24) > td > h6 > input:nth-child(1)'))
        )
        submit2.click()
        print('配置呼出路由成功{}'.format(num))
    except TimeoutException:
        print('配置呼出路由失败')
        outbound_route(id, num)


def main():
    login()
    # 配置分机和呼出路由
    for i in range(1, 33):
        if i < 10:
            j = '0' + str(i)
            # (id, number)
            outbound_route(i+1, j)
        else:
            outbound_route(i+1, str(i))
    # apply config
    submit3 = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#button_reload'))
    )
    submit3.click()
    browser.close()

if __name__ == '__main__':
    main()
