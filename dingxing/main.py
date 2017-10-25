# 三汇网关自动配置脚本
# author: seven

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from dingxing.config import *

browser = webdriver.PhantomJS()
# browser.maximize_window()
wait = WebDriverWait(browser, 15)


def login():
    try:
        browser.get('http://admin:admin@{}/'.format(BASE_IP))
        browser.get('http://192.168.1.104/Frame.htm')
        print(browser.page_source)
        # 呼叫配置
        button1 = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="BoldHref4"]'))
        )
        print(button1)
        button1.click()
        # IP->Tel路由
        button2 = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#HerfMenu251'))
        )
        print(button2)
        button2.click()
    except TimeoutException:
        login()


def port_config():
    # 添加
    button1 = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '#Add'))
    )
    button1.click()
    s1 = Select(browser.find_element_by_id('BindDynamic'))
    s1.select_by_visible_text("0")
    input = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#RouteDesc'))
    )
    input.clear()
    input.send_keys('0')
    s2 = Select(browser.find_element_by_id('RouteSrc'))
    s2.select_by_visible_text("任意")
    s2 = Select(browser.find_element_by_id('RouteDest'))
    s2.select_by_value("0")
    # 高级路由规则
    button2 = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '#RouteEnable'))
    )
    button2.click()
    # 主叫号码前缀
    input = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#RouteSrcPrefix'))
    )
    input.clear()
    input.send_keys('1888888')
    # 保存
    button3 = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '#Ok'))
    )
    button3.click()


def net_config():
    try:
        browser.get('http://{}/navigation.php'.format(BASE_IP))
        # 高级设置
        button1 = wait.until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/dl/dt[4]'))
        )
        button1.click()
        # 网络设置
        button2 = wait.until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/dl/dd[4]/ul/li[1]/a'))
        )
        button2.click()
        # IP地址<input type="text" style="ime-mode:disabled;width:130px" id="IpAddr" name="IpAddr" onkeypress="inputlimit_IP(this.value,event)" class="text" value="192.168.1.100">
        input = wait.until(
                EC.presence_of_element_located((By.ID, 'IpAddr'))
        )
        input.clear()
        input.send_keys(IP)
        # 网关<input type="text" style="ime-mode:disabled;width:130px" id="Gateway" name="Gateway" onkeypress="inputlimit_IP(this.value,event)" class="text" value="192.168.1.1">
        input = wait.until(
                EC.presence_of_element_located((By.ID, 'Gateway'))
        )
        input.clear()
        input.send_keys(GATEWAY)
        # 点击保存
        submit = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '#ok'))
        )
        submit.click()
        # 弹出框确定
        a1 = browser.switch_to.alert
        sleep(1)
        a1.accept()
    except TimeoutException:
        net_config()


def main():
    login()
    port_config()


if __name__ == '__main__':
    main()
