
# -*- coding: UTF-8 -*-
import time
import os
from selenium import webdriver
from PIL import Image
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys  # 需要引入keys包
from selenium.webdriver.support.ui import Select
import sys
import requests
import pickle
import json
from requests import exceptions
import time,urllib2,difflib
import pngquant
from fateadm_api import FateadmApi
from datetime import datetime

reload(sys)  # reload 才能调用 setdefaultencoding 方法
sys.setdefaultencoding('utf-8')  # 设置 'utf-8'

DOWNLOAD_CSV = '/Users/mac04/Downloads'
MESSAGE = 'http://192.168.204.2/getcode.php'
ACCOUNT = 'https://cpanel.yayawan.com/?act=game.pack_tool_api&key=wxj9dlpe&action=get_access&lib=baidu'

BD_LOGIN_1 = "http://shantou.baidu.com/#/"
BD_LOGIN_2 = "http://shantou.baidu.com/pa/pna.html#/report/index~type=styles"
API_UPLOAD_CSV = "https://cpanel.yayawan.com/"

pd_id = "112729"
pd_key = "HsfKii2YwtjeyMNlmqMaQQ9Le1XHMzYn"
app_id = "312729"
app_key = "05+HjIfGKIRkuuFhqaoQR21SDx3qSa6c"
# 具体类型可以查看官方网站的价格页选择具体的类型，不清楚类型的，可以咨询客服
pred_type = "30400"
# 初始化api接口
api = FateadmApi(app_id, app_key, pd_id, pd_key)


class BD(object):
    def __init__(self):
        self.headers = {
            'Connection': 'close',
        }
        self.base_params = {
        }

    def csv_upload(self,data):
        params = {
            'act':'game.pack_tool_api',
            'key':'wxj9dlpe',
            'action':'save_report',
            'str':data
        }
        try:
            r = requests.post(API_UPLOAD_CSV, headers=self.headers, data=params)
            print r.text
        except exceptions as e:
            print e
    def message(self):
        while(True):
            r = requests.get(MESSAGE)
            if not r.content:
                time.sleep(2)
            else:
                break
        return r.content
    def account(self):
        try:
            r = requests.get(ACCOUNT)
            return r.json()['data']
        except Exception as e:
            return ''

bd = BD()


# 获取csv
def file_csv():
    for root, folders, files in os.walk(DOWNLOAD_CSV):
        for fname in files:
            if fname.endswith('.csv'):
                fullname = os.path.join(root, fname)
                print fullname
                data = open(fullname, 'rb').read()
                os.remove(fullname)
                return data

def ff_dama(image_data):
    rep = api.Predict(pred_type,image_data)
    return rep

def verifyCodeImg(imageurl):
    headers = {
        "User-Agent": driver.execute_script("return navigator.userAgent;")
    }
    s = requests.session()
    s.headers.update(headers)
    for cookie in driver.get_cookies():
        c = {cookie['name']: cookie['value']}
        s.cookies.update(c)
    r = s.get(imageurl, allow_redirects=True)
    with open('tkcode.png', 'wb') as img:
        img.write(r.content)
    image = open('tkcode.png', 'rb').read()
    return image


def download_excel():
    driver.get(BD_LOGIN_2)
    time.sleep(15)
    driver.find_element_by_xpath('//*[@id="ctrl-e-range-text"]').click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="ctrl-e-range-shortcut-item0"]').click()
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="ctrl-e-esui8785963"]').click()
    time.sleep(8)
    # 下载
    driver.find_element_by_xpath('//*[@id="ctrl-e-downloadReport"]').click()
    print 'down_load_ing...0'
    time.sleep(10)
    down_laod_error()
    time.sleep(1)
    # 上传
    bd.csv_upload(file_csv())
    time.sleep(5)

    # 下方
    driver.find_element_by_xpath('//*[@id="ctrl-e-position"]/div[2]').click()
    time.sleep(5)
    driver.find_element_by_xpath('//*[@id="ctrl-e-downloadReport"]').click()
    time.sleep(5)
    down_laod_error()
    bd.csv_upload(file_csv())
    time.sleep(5)
    print '上传成功'

# 下载报错
def down_laod_error():
    time.sleep(5)
    while(True):
        print 'down_load_ing...1'
        time.sleep(1)
        try:
            print 'down_load_ing...2'
            errortext = driver.find_element_by_xpath('//*[@id="ctrl-default-dialog-alert8785971-body"]/div[2]').text
            print errortext
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="ctrl-default-dialog-alert8785971-dialog-alert-ok"]').click()
            time.sleep(2)
            # 重新下载
            driver.find_element_by_xpath('//*[@id="ctrl-e-downloadReport"]').click()
            time.sleep(10)
            print '重新下载'
            break
        except:
            print 'down_load_ing...3'
            break
            pass

def login(name,pwd):
    driver.get(BD_LOGIN_1)
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="entered_login"]').clear()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="entered_login"]').send_keys(name)
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="entered_password"]').send_keys(pwd)
    time.sleep(1)
    verify_codeimg()

    # 点击登录
    driver.find_element_by_xpath('/html/body/div[2]/div[2]/form/div[4]/input').click()
    time.sleep(5)

    while (True):
        time.sleep(1)
        try:
            errortext = driver.find_element_by_xpath('//*[@id="codeError"]')
            res1 = u"验证码错误" in errortext.text
            if res1:
                print errortext.text
                # 刷新页面
                # driver.navigate().refresh();
                # 刷新验证码
                driver.find_element_by_xpath('//*[@id="refreshVerifyCode"]').click()
                # 输入密码
                driver.find_element_by_xpath('//*[@id="entered_password"]').send_keys(pwd)
                verify_codeimg()
                # 登录
                driver.find_element_by_xpath('/html/body/div[2]/div[2]/form/div[4]/input').click()

            else:
                break
        except:
            print '验证码识别成功'
            message_send()
            break

def verify_codeimg():

    imageurl = driver.find_element_by_id('verifyCode').get_attribute('src')
    # 获取截图
    driver.get_screenshot_as_file('CrawlResult/screenshot.png')
    # 获取指定元素位置
    element = driver.find_element_by_id('verifyCode')
    left = int(element.location['x'])
    top = int(element.location['y'])
    right = int(element.location['x'] + element.size['width'])
    bottom = int(element.location['y'] + element.size['height'])
    # 通过Image处理图像
    im = Image.open('CrawlResult/screenshot.png')
    im = im.crop((left, top, right, bottom))
    im.save('CrawlResult/code.png')
    image = open('CrawlResult/code.png', 'rb').read()

    res = ff_dama(image)
    code = res.pred_rsp.value
    driver.find_element_by_xpath('//*[@id="entered_imagecode"]').click()
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="entered_imagecode"]').send_keys(code)
    time.sleep(4)

def message_send():

    requests.get(MESSAGE)
    while(True):
        try:
            driver.find_element_by_xpath('/html/body/div[2]/h2').text
            # 手机号码
            driver.find_element_by_xpath('//*[@id="uc-sec-mobile"]').send_keys(u'13128282957')
            time.sleep(3)
            # 获取验证码
            driver.find_element_by_xpath('//*[@id="uc-sec-get-code-btn"]').click()
            time.sleep(3)
            # 验证码
            message_code = bd.message()
            print message_code
            driver.find_element_by_xpath('//*[@id="uc-sec-code"]').send_keys(message_code)
            time.sleep(3)
            # 确定
            driver.find_element_by_xpath('//*[@id="uc-sec-confirm-btn"]').click()
            time.sleep(1)
            print '短信获取成功'
            break
        except:
            print '登录成功'
            break


if __name__ == '__main__':

    while(True):

        if int(datetime.now().strftime("%H")) != 17:
            time.sleep(2)
            continue

        account = bd.account()
        print account
        if not account:
            break
        for i in range(len(account)):
            print u'------' + str(i) + u'------'
            driver = webdriver.Chrome('/Users/mac04/Downloads/chromedriver')
            driver.set_window_size(1200, 800)
            name = account[i]['u']
            pwd = account[i]['p']
            print u"用户名: " + name + " " + u"密码: " + pwd
            try:
                login(name, pwd)
            except Exception as e:
                print e
                driver.quit()
                continue
            try:
                download_excel()
            except:
                driver.quit()
                continue
            driver.quit()
            time.sleep(10)

