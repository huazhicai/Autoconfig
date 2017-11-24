# 鼎鑫通网关自动配置脚本
# author: seven

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from dingxing.config import *

browser = webdriver.Chrome()
browser.maximize_window()
wait = WebDriverWait(browser, 60)


# 登录网关
def login():
    try:
        browser.get('http://admin:admin@{}/Frame.htm'.format(BASE_IP))
        # browser.get('http://192.168.1.104/Frame.htm')
    except TimeoutException:
        login()


# 添加ip->Tell路由
def port_config(number):
    try:
        browser.get('http://{}/RouteIP2PSTNAddNew.htm'.format(BASE_IP))

        # 实例化Select
        se1 = Select(browser.find_element_by_id('RouteIndex'))
        # 选择编号
        se1.select_by_visible_text(number)
        # # 名称
        # # CSS  #RouteDesc
        input1 = browser.find_element_by_id('RouteDesc')
        input1.clear()
        input1.send_keys(number)

        # 呼叫来源
        se2 = Select(browser.find_element_by_id('RouteSrc'))
        se2.select_by_value("255")

        # 呼叫送达
        se3 = Select(browser.find_element_by_id('RouteDest'))
        se3.select_by_visible_text('port-{}'.format(number))

        # 高级路由规则
        submit1 = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '#RouteEnable'))
        )
        submit1.click()

        # 主叫号码前缀
        input2 = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#RouteSrcPrefix'))
        )
        input2.clear()
        if int(number) < 10:
            input2.send_keys(PREFIX + '0' + number)
        else:
            input2.send_keys(PREFIX + number)

        # 保存
        submit2 = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '#Ok'))
        )
        submit2.click()
        print('配置成功{}'.format(number))
        # 添加
        submit3 = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '#Add'))
        )
        submit3.click()
    except TimeoutException:
        print('配置失败{}'.format(number))


# 修改网络配置的IP和GATEEAY
def net_config():
    try:
        browser.get('http://{}/LocalNetwork.htm'.format(BASE_IP))
        # IP 地址
        input1 = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#WanIP'))
        )
        input1.clear()
        input1.send_keys(IP)

        # 默认网关
        input2 = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#GateWay'))
        )
        input2.clear()
        input2.send_keys(GATEWAY)

        # 保存
        submit = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '#ok'))
        )
        submit.click()
        print(IP, GATEWAY)

    except TimeoutException:
        net_config()


# 重启设备使配置生效
def restart():
    browser.get('http://{}/Restart.htm'.format(BASE_IP))
    browser.find_element_by_id('reboot').click()
    # 弹出框确定
    a1 = browser.switch_to.alert
    sleep(1)
    a1.accept()


def main():
    login()
    # 分配号码
    for num in range(start, end + 1):
        port_config(str(num))
    # 修改IP路由
    net_config()
    sleep(0.5)
    restart()
    # browser.close()


if __name__ == '__main__':
    main()
