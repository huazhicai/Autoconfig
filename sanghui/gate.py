# 三汇网关自动配置脚本
# author: Seven

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from sanghui.config import *

browser = webdriver.Chrome()
browser.maximize_window()
wait = WebDriverWait(browser, 90)


# 登录网关
def login():
    try:
        # 账号名密码登录网关
        browser.get('http://admin:admin@{}/'.format(BASE_IP))
    except TimeoutException:
        print('登录失败')
        login()


# 填写端口配置, 	IP->Tel路由 添加
def port_config(id, number):
    try:
        browser.get('http://{0}/6-1-1portmodify.php?id={1}'.format(BASE_IP, id))
        wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#BindDynamic'))
        )
        # 选择静态绑定
        s1 = Select(browser.find_element_by_id('BindDynamic'))
        s1.select_by_value("0")
        # 绑定号码
        input = wait.until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="BindNum"]'))
        )
        input.clear()
        input.send_keys(number)
        # 保存修改
        submit = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '#ok'))
        )
        submit.click()
        # 弹出框确定
        a1 = browser.switch_to.alert
        sleep(1)
        a1.accept()
        print('端口配置完成{}'.format(number))
    except TimeoutException:
        port_config(id, number)


# 修改网络配置的ip和网关
def net_config():
    try:
        # http://192.168.1.100/4-1netset.php
        browser.get('http://{}/4-1netset.php'.format(BASE_IP))
        # IP地址
        input1 = wait.until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="IpAddr"]'))
        )
        input1.clear()
        input1.send_keys(IP)
        # 网关
        input2 = wait.until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="Gateway"]'))
        )
        input2.clear()
        input2.send_keys(GATEWAY)
        # DNS
        input3 = wait.until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="Firstdns"]'))
        )
        input3.clear()
        input3.send_keys(DNS)
        # 点击保存
        submit = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '#ok'))
        )
        submit.click()
        # 弹出框确定
        a1 = browser.switch_to.alert
        sleep(1)
        a1.accept()
        print('网络配置成功ip:{},gateway{}'.format(IP, GATEWAY))
    except TimeoutException:
        print('网络配置失败')


# 注册网关
def register():
    try:
        browser.get('http://admin:admin@{}/'.format(IP))
        browser.get('http://{}/9-10snmp.php'.format(IP))
        # 勾选启用
        input1 = wait.until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="CheckboxGroup_snmp"]'))
        )
        input1.click()
        # 集中管理服务器地址
        input2 = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#snmp_ip'))
        )
        input2.clear()
        input2.send_keys(SERVER_URL)
        # 公司名
        input3 = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#area'))
        )
        input3.clear()
        input3.send_keys(COMPANY)
        # 授权码
        input4 = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#authorCode'))
        )
        input4.clear()
        input4.send_keys(TOKEN)
        # 网关描述
        input5 = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#description'))
        )
        input5.clear()
        input5.send_keys(DESCRIBE)
        # 保存
        click = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#save'))
        )
        click.click()
        a1 = browser.switch_to.alert
        sleep(1)
        a1.accept()
        print('注册成功')
    except:
        print("注册失败")


def main():
    login()
    # i为id号，非号码后尾数， id从0到31 range(32)
    for i in range(32):
        id = str(i)
        # i<9不用动
        if i < 9:
            number = PREFIX + '0' + str(i + 1)
            port_config(id, number)
        else:
            number = PREFIX + str(i + 1)
            port_config(id, number)
    # 网络配置
    net_config()
    register()
    browser.quit()


if __name__ == '__main__':
    main()
