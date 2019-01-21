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
from selenium.webdriver.common.keys import Keys  #需要引入keys包
from selenium.webdriver.support.ui import Select
import xlrd
import xlwt
from xlutils.copy import copy
from xlwt import Style
import pyautogui
import pyperclip
import sys
import requests
from hashlib import md5
import pickle
import json



reload(sys)                      # reload 才能调用 setdefaultencoding 方法
sys.setdefaultencoding('utf-8')  # 设置 'utf-8'
xlrd.Book.encoding = "utf8"


BASEPATH = os.path.abspath(os.curdir)
# /Users/lz/PycharmProjects/untitled1
# /Users/lz/PycharmProjects/untitled1/qc1121jjcjb001.apk

APL_INFO_URL = 'https://cpanel.yayawan.com/?act=game.pack_tool_api&action=get_baidu_task&key=wxj9dlpe'
BAIDUURL_LOGIN = 'http://app.baidu.com/'
baidu_username = '18680442415'
baidu_password = 'BDapp1988'
rk_username = 'mwlbear'
rk_password = '@qq19028'

driver = webdriver.Chrome('/Users/lz/Downloads/chromedriver')
imagePath = '/Users/lz/Desktop/1.png'


#
class APK(object):
    def __init__(self):
        self.base_params = {
            'action': 'update_task_status',
            'key':'wxj9dlpe',
        }
    def apk_info(self):
        r = requests.get(APL_INFO_URL)
        return r.json()['data']

    def apk_report_error(self, ename, status,error):
        params = {
            'ename':ename,
            'status':status,
            'tag':error,
        }
        params.update(self.base_params)
        r = requests.post('https://cpanel.yayawan.com/?act=game.pack_tool_api',data=params)
        return r.json()

apk = APK()
# 若快识别验证码
class RClient(object):
    def __init__(self,username,password,soft_id,soft_key):
        self.username = username
        self.password = password
        self.soft_id = soft_id
        self.soft_key = soft_key

        self.base_params = {
            'username':self.username,
            'password':self.password,
            'softid':self.soft_id,
            'softkey':self.soft_key,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'Expect': '100-continue',
            'User-Agent': 'ben',
        }
    def rk_create(self, im, im_type, timeout=60):
        """
        im: 图片字节
        im_type: 题目类型
        """
        params = {
            'typeid': im_type,
            'timeout': timeout,
        }
        params.update(self.base_params)
        files = {'image': ('a.jpg', im)}
        r = requests.post('http://api.ruokuai.com/create.json', data=params, files=files, headers=self.headers)
        return r.json()

    def rk_report_error(self, im_id):
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://api.ruokuai.com/reporterror.json', data=params, headers=self.headers)
        return r.json()

rc = RClient(rk_username, rk_password, '121093', 'c746b4d86af24b27b18bd3c0a92a6a79')

def verifyCodeImg(imageurl,type):

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
    rs = rc.rk_create(image, type)
    return rs

def dowmload_image(url):
    local_filename = url.split('/')[-1]
    # NOTE the stream=True parameter
    r = requests.get(url, allow_redirects=True)
    with open(local_filename, 'wb') as img:
        img.write(r.content)
    return local_filename

def download_file(url):
    local_filename = url.split('/')[-1]
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                #f.flush() commented by recommendation from J.F.Sebastian
    return local_filename

def login():
    print '开始登陆'
    driver.get(BAIDUURL_LOGIN)
    # driver.maximize_window()
    time.sleep(8)
    driver.find_element_by_xpath('//*[@id="j-inheaderNew"]/div/ul[2]/li[2]/a').click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="TANGRAM__PSP_10__userName"]').click()
    driver.find_element_by_xpath('//*[@id="TANGRAM__PSP_10__userName"]').send_keys(baidu_username)
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="TANGRAM__PSP_10__password"]').click()
    driver.find_element_by_xpath('//*[@id="TANGRAM__PSP_10__password"]').send_keys(baidu_password)
    # 登录
    driver.find_element_by_xpath('//*[@id="TANGRAM__PSP_10__submit"]').click()
    time.sleep(3)
    ecode = None
    time.sleep(8)
    try:
        ecode = driver.find_element_by_xpath('//*[@id="TANGRAM__PSP_10__verifyCode"]')
    except:
        print ecode
        print '登录不用验证码'
    if ecode:
        print '123456'
        # print imageurl
        while (True):
            time.sleep(2)
            imageurl = driver.find_element_by_xpath('//*[@id="TANGRAM__PSP_10__verifyCodeImg"]').get_attribute('src')
            print imageurl
            driver.find_element_by_xpath('//*[@id="TANGRAM__PSP_10__verifyCode"]').clear()
            rs = verifyCodeImg(imageurl,5000)
            print rs['Result']
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="TANGRAM__PSP_10__verifyCode"]').click()
            driver.find_element_by_xpath('//*[@id="TANGRAM__PSP_10__verifyCode"]').send_keys(rs['Result'])
            time.sleep(5)
            driver.find_element_by_xpath('//*[@id="TANGRAM__PSP_10__submit"]').click()
            time.sleep(5)

            try:
                errortext = driver.find_element_by_xpath('//*[@id="TANGRAM__PSP_10__error"]')
            except:
                break
            print errortext.text
            if errortext.text.find(u'验证码'):
                print '错误验证码'
                rc.rk_report_error(rs['Id'])
                time.sleep(2)
            else:
                break
    pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))

def upload_first(reinfo):
    print '创建应用'
    time.sleep(5)
    driver.get('http://app.baidu.com/apps/')
    time.sleep(1)
    driver.find_element_by_xpath('/html/body/div[4]/div[4]/div/div[3]/div/a').click()
    driver.find_element_by_xpath('//*[@id="applink"]/span[1]/span[2]').click()
    time.sleep(3)
    # 应用名称
    driver.find_element_by_xpath('//*[@id="app_name"]').send_keys(reinfo['name'])
    time.sleep(2)
    # 应用图标
    # 下载icon
    driver.find_element_by_name('file').send_keys(reinfo['icon'])
    # 图片尺寸错误

    time.sleep(5)
    driver.find_element_by_xpath('//*[@id="vcode"]').click()
    #验证码
    while(True):
        imageurl = driver.find_element_by_xpath('//*[@id="vcode_img"]').get_attribute('src')
        rs = verifyCodeImg(imageurl, 3040)
        driver.find_element_by_xpath('//*[@id="vcode"]').send_keys(rs['Result'])
        time.sleep(2)
        driver.find_element_by_xpath('/html/body/div[4]/div[4]/div/div[2]/form/fieldset/div/div[5]/div/div/a[1]').click()
        time.sleep(3)
        try:
           el = driver.find_element_by_xpath('//*[@id="dialog"]/div[2]/p')
        except:
            break
        if el.text.find(u'验证码'):
            print u'弹出验证码'
            rc.rk_report_error(rs['Id'])
            time.sleep(2)
            # 确定
            driver.find_element_by_xpath('//*[@id="dialogConfirm"]').click()
        else:
            break

def upload_second(reinfo):
    print '提交应用信息'
    time.sleep(5)
    # 支付类型
    driver.find_element_by_xpath('//*[@id="divUpdate"]/form[2]/fieldset/div[1]/div[2]/div/div[3]/div/div/span').click()
    time.sleep(1)
    # 杀毒
    driver.find_element_by_xpath('/html/body/div[4]/div[4]/div/div[3]/div[3]/div[1]/div/span[1]').click()
    # 下一步
    driver.find_element_by_xpath('/html/body/div[4]/div[4]/div/div[3]/div[4]/div[1]/a[2]').click()
    # 网络应用
    driver.find_element_by_xpath('/html/body/div[4]/div[4]/div/div[3]/div[3]/div[1]/div/span[15]').click()
    # 完成
    driver.find_element_by_xpath('/html/body/div[4]/div[4]/div/div[3]/div[4]/div[2]/a[2]').click()
    # 一句话描述
    subname =reinfo['subname']
    if len(subname)>30:
        subname = subname[0:30]
    else:
        subname = reinfo['subname']

    print subname
    driver.find_element_by_xpath('//*[@id="summary"]').click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="summary"]').send_keys(subname)
    # 应用简介
    driver.find_element_by_xpath('//*[@id="description"]').click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="description"]').send_keys(reinfo['desc'])
    # 上传安装包 上完完成
    driver.find_element_by_xpath('//*[@id="btnUploadApk"]').find_element_by_name('file').send_keys(reinfo['url'])
    time.sleep(5)
    while(True):
        time.sleep(2)
        try:
            suc = driver.find_element_by_xpath('//*[@id="btnApkUploaded"]')
            # print suc.text
            if suc.text == '已上传':
                break
        except:
            pass
        # if driver.find_element_by_xpath('//*[@id="btnApkUploaded"]').text == '已上传':
        #     break
        try:
            sure = driver.find_element_by_xpath('//*[@id="dialogConfirm"]')
            error = driver.find_element_by_xpath('//*[@id="dialog"]/div[2]/p').text
            apk.apk_report_error(reinfo['ename'],'12',error)
            driver.find_element_by_xpath('//*[@id="dialogConfirm"]').click()
            print error
            return
        except:
            continue

    # 应用截图
    for name in reinfo['images']:
        time.sleep(3)
        driver.find_element_by_xpath('//*[@id="btnAddScreen"]').find_element_by_name('file').send_keys(name)
    # 提交
    driver.find_element_by_xpath('//*[@id="divUpdate"]/form[2]/fieldset/div[2]/div[1]/div/div/a[1]').click()
    time.sleep(20)
    try:
        driver.find_element_by_xpath('//*[@id="dialogConfirm"]')
        error = driver.find_element_by_xpath('//*[@id="dialog"]/div[2]/p').text
        driver.find_element_by_xpath('//*[@id="dialogConfirm"]').click()
        apk.apk_report_error(reinfo['ename'], '12', error)
        print error
        return
    except:
        pass
    # 成功上报
    apk.apk_report_error(reinfo['ename'],'11',None)

def removeapk(reinfo):
    # 删除apk 包
    if os.path.exists(reinfo['url']):
        os.remove(reinfo['url'])
    time.sleep(2)
    if os.path.exists(reinfo['icon']):
        os.remove(reinfo['icon'])
    for name in reinfo['images']:
        time.sleep(1)
        if os.path.exists(name):
            os.remove(name)
    print '截图删除完成'
    time.sleep(2)

if __name__ == '__main__':

    login()
    while(True):
        time.sleep(1)
        reinfo = apk.apk_info()
        if not reinfo:
            continue
        print '---------------------------------------我是分割线----------------------------------'
        print reinfo
        ename = reinfo['ename']
        icon = reinfo['icon']
        print icon
        apkname = reinfo['name']
        subname = reinfo['subname']
        if not subname:
            reinfo['subname'] = u'2019必玩手游!唯美画风,让你身临其境!'
        print u'app名字:'+apkname
        print u'副标题:'+subname
        desc = reinfo['desc']
        images = reinfo['images']
        if not len(images):
            print '没有截图'

        imagesurlList = images.split(',')
        apkurl = reinfo['url']
        print apkurl

        imagename = dowmload_image(icon)
        # 下载icon
        imagePath = BASEPATH + '/' + imagename
        img1 = Image.open(imagePath)
        new_img = img1.resize((512, 512), Image.ANTIALIAS)  # w代表宽度，h代表高度，最后一个参数指   定采用的算法
        new_img.save(imagePath, quality=100)
        reinfo['icon'] = imagePath
        print u'icon下载路径:' + imagePath

        # 下载游戏截图
        list = []
        for name in imagesurlList:
            image = dowmload_image(name)
            path = BASEPATH + '/' + image
            img = Image.open(path)
            new_img = img.resize((480, 800), Image.ANTIALIAS)  # w代表宽度，h代表高度，最后一个参数指   定采用的算法
            new_img.save(path, quality=100)
            print u"应用截图下载路径:" + path
            list.append(path)
        reinfo['images'] = list

        # 下载APK包
        apkurl = download_file(apkurl)
        reinfo['url'] = BASEPATH + '/' + apkurl
        print u'apk地址:' + reinfo['url']

        # 下载icon
        upload_first(reinfo)
        upload_second(reinfo)
        # 删除下载内容
        removeapk(reinfo)
