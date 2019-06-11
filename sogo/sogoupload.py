
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


reload(sys)  # reload 才能调用 setdefaultencoding 方法
sys.setdefaultencoding('utf-8')  # 设置 'utf-8'

BASEPATH = os.path.abspath(os.curdir)

pngquantPath = '/Users/mac04/Downloads/pngquant/pngquant'
APL_INFO_URL = ''
APL_INFO_ERROR_URL = ''

# APL_INFO_URL = 'http://cpanel.kingoo.com.cn/?act=game.pack_tool_api&action=get_baidu_task&key=wxj9dlpe'
# APL_INFO_ERROR_URL = 'http://cpanel.kingoo.com.cn/?act=game.pack_tool_api'

SOGOU_LOGIN = 'http://xuri.p4p.sogou.com/cpcadindex/init2.action#index'
SOGOU_LOGINL_SECOND = 'http://xuri.p4p.sogou.com/cpcadindex/init2.action#/appManage'


driver = webdriver.Chrome('/Users/mac04/Downloads/chromedriver')


yyw_qg = raw_input("请输入0或者1(0=千果||1=千骐): \n")
if yyw_qg == "1":
    APL_INFO_URL = 'https://cpanel.yayawan.com/?act=game.pack_tool_api&action=get_baidu_task&key=wxj9dlpe&lib=sogou'
    APL_INFO_ERROR_URL = 'http://cpanel.yayawan.com/?act=game.pack_tool_api'
elif yyw_qg == '0':
    APL_INFO_URL = 'http://cpanel.kingoo.com.cn/?act=game.pack_tool_api&action=get_baidu_task&key=wxj9dlpe&lib=sogou'
    APL_INFO_ERROR_URL = 'http://cpanel.kingoo.com.cn/?act=game.pack_tool_api'

class APK(object):
    def __init__(self):
        self.headers = {
            'Connection': 'close',
        }
        self.base_params = {
            'action': 'update_task_status',
            'key': 'wxj9dlpe',
        }

    def apk_info(self):
        try:
            # requests.adapters.DEFAULT_RETRIES = 5
            r = requests.post(APL_INFO_URL, headers=self.headers)
            if r.json()['err_code'] == 1:
                # 无任务
                print 'no task'
                return {}
            else:
                return r.json()['data']
        except exceptions as e:
            print e

    def apk_report_error(self, ename, status, error):
        params = {
            'ename': ename,
            'status': status,
            'tag': error,
        }
        params.update(self.base_params)
        try:
            r = requests.post(APL_INFO_ERROR_URL, data=params, headers=self.headers)
            return r.json()
        except exceptions as e:
            print e
apk = APK()

# # 若快识别验证码
# class RClient(object):
#     def __init__(self, username, password, soft_id, soft_key):
#         self.username = username
#         self.password = password
#         self.soft_id = soft_id
#         self.soft_key = soft_key
#
#         self.base_params = {
#             'username': self.username,
#             'password': self.password,
#             'softid': self.soft_id,
#             'softkey': self.soft_key,
#         }
#         self.headers = {
#             'Connection': 'Keep-Alive',
#             'Expect': '100-continue',
#             'User-Agent': 'ben',
#         }
#
#     def rk_create(self, im, im_type, timeout=60):
#         """
#         im: 图片字节
#         im_type: 题目类型
#         """
#         params = {
#             'typeid': im_type,
#             'timeout': timeout,
#         }
#         params.update(self.base_params)
#         files = {'image': ('a.jpg', im)}
#         try:
#             r = requests.post('http://api.ruokuai.com/create.json', data=params, files=files, headers=self.headers)
#             print r
#             print r.json()
#             return r.json()
#         except exceptions as e:
#             print e
#
#     def rk_report_error(self, im_id):
#         params = {
#             'id': im_id,
#         }
#         params.update(self.base_params)
#         try:
#             r = requests.post('http://api.ruokuai.com/reporterror.json', data=params, headers=self.headers)
#             return r.json()
#         except exceptions as e:
#             print e
# rc = RClient(rk_username, rk_password, '121093', 'c746b4d86af24b27b18bd3c0a92a6a79')

pd_id = "112729"
pd_key = "HsfKii2YwtjeyMNlmqMaQQ9Le1XHMzYn"
app_id = "312729"
app_key = "05+HjIfGKIRkuuFhqaoQR21SDx3qSa6c"
# 具体类型可以查看官方网站的价格页选择具体的类型，不清楚类型的，可以咨询客服
pred_type = "20400"
# 初始化api接口
api = FateadmApi(app_id, app_key, pd_id, pd_key)

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
    with open('tkcode.png'+yyw_qg, 'wb') as img:
        img.write(r.content)
    image = open('tkcode.png'+yyw_qg, 'rb').read()
    return image

def dowmload_image(url):
    local_filename = url.split('/')[-1]
    # NOTE the stream=True parameter
    try:
        r = requests.get(url, allow_redirects=True, timeout=10)
        with open(local_filename, 'wb') as img:
            img.write(r.content)
    except:
        return dowmload_image(url)
    return local_filename

def download_file(url):
    local_filename = url.split('/')[-1]
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
                # f.flush() commented by recommendation from J.F.Sebastian
    return local_filename

def login(reinfo):
    # print '开始登陆'
    driver.get(SOGOU_LOGIN)
    time.sleep(5)
    driver.find_element_by_xpath('//*[@id="username"]').send_keys(reinfo['sgusername'])
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="password"]').send_keys(reinfo['sgpassword'])

    imageurl = driver.find_element_by_xpath('//*[@id="validateCodeImg"]').get_attribute('src')
    image_data = verifyCodeImg(imageurl)
    # 打码平台调用
    res = ff_dama(image_data)
    # 验证码
    code = res.pred_rsp.value
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="validateCode"]').clear()
    driver.find_element_by_xpath('//*[@id="validateCode"]').send_keys(code)
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="button"]/img').click()
    time.sleep(1)

    while(True):
        time.sleep(1)
        try:
            errortext = driver.find_element_by_xpath('//*[@id="errorMsg"]')
            print errortext.text
            res1 = u"验证码无效" in errortext.text
            if res1:
                print '错误验证码'
                if res.ret_code == 0:
                    api.Justice(res.request_id)
                return 0
                break
            else:
                return 0
                break
        except:
            print '登录成功!!!!'
            return 1
            break

def upload_first(reinfo):
    time.sleep(5)
    driver.get(SOGOU_LOGINL_SECOND)
    time.sleep(6)
    driver.find_element_by_xpath('//*[@id="content"]/div/div[3]/div/button[1]').click()
    # APP名称
    driver.find_element_by_xpath('/html/body/div[6]/div/div/div/ul[2]/li/input').send_keys(reinfo['name'])
    # APP图标
    driver.find_element_by_xpath('/html/body/div[6]/div/div/div/ul[3]/li/div[1]/table/tbody/tr[2]/td[2]/div/a/span').click()
    time.sleep(2)
    driver.find_element_by_xpath('/html/body/div[8]/div[1]/div/table/tbody/tr/td[1]/div[2]/input').send_keys(reinfo['icon'])
    time.sleep(1)
    # 保存
    driver.find_element_by_xpath('/html/body/div[8]/div[2]/button[1]').click()
    time.sleep(3)
    # APP类型
    driver.find_element_by_xpath('/html/body/div[6]/div/div/div/ul[4]/li/div/div').click()
    gettagClick('手机游戏')
    driver.find_element_by_xpath('/html/body/div[6]/div/div/div/ul[4]/li/div/div[2]/a/span[1]').click()
    driver.find_element_by_xpath('/html/body/ul[4]/li[5]').click()

    # *下载链接：
    driver.find_element_by_xpath('/html/body/div[6]/div/div/div/ul[5]/li/input').send_keys(reinfo['url'])
    # *详情介绍链接:
    driver.find_element_by_xpath('/html/body/div[6]/div/div/div/ul[6]/li/input').send_keys(reinfo['page_url'])
    # *APP描述：
    driver.find_element_by_xpath('/html/body/div[6]/div/div/div/ul[7]/li/input').send_keys(reinfo['desc'])

    # *APP截图：
    for name in reinfo['images']:
        time.sleep(3)
        driver.find_element_by_xpath('/html/body/form/input[3]').send_keys(name)
    # 提交
    #  安装包大小:
    driver.find_element_by_xpath('/html/body/div[6]/div/div/div/ul[9]/li/input').send_keys(reinfo['apksize'])
    #  更新时间 日历：
    currenttime = time.strftime("%Y-%m-%d", time.localtime())
    driver.find_element_by_xpath('//*[@id="add-app-dialog-update-date-form-item"]').send_keys(currenttime)
    # 版本号：
    driver.find_element_by_xpath('/html/body/div[6]/div/div/div/ul[11]/li/input').send_keys(reinfo['ename'])
    # 包名：
    driver.find_element_by_xpath('/html/body/div[6]/div/div/div/ul[12]/li/input').send_keys(reinfo['apkname'])
    time.sleep(1)
    # 提交
    driver.find_element_by_xpath('/html/body/div[6]/div/div/div/div[3]/button[1]').click()
    time.sleep(3)
    # 成功上报
    rs = apk.apk_report_error(reinfo['ename'], '23', None)
    # 退出登录
    driver.find_element_by_xpath('//*[@id="app"]/div/div[1]/ul[2]/li[4]/a/i').click()
    print '退出登录！！！'
    print rs

def remove_current_apk(reinfo):
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
def remove_error_other():
    rmcmd = 'cd ' + BASEPATH + '&&' + 'rm *.png *.jpg'
    os.system(rmcmd)
    # for root, folders, files in os.walk(BASEPATH):
    #     for fname in files:
    #         print root
    #         if fname.endswith('.apk') | fname.endswith('.png') | fname.endswith('.jpg'):
    #             fullname = os.path.join(root, fname)
    #             print fullname
    #             os.remove(fullname)
    # print '删除完成'
def get_FileSize(filePath):
    filePath = unicode(filePath,'utf8')
    fsize = os.path.getsize(filePath)
    fsize = fsize/float(1024*1024)
    return round(fsize,2)
def getRemoteFileInfo(url, proxy=None):

    opener = urllib2.build_opener()
    if proxy:
        if url.lower().startswith('https://'):
            opener.add_handler(urllib2.ProxyHandler({'https': proxy}))
        else:
            opener.add_handler(urllib2.ProxyHandler({'http': proxy}))
    try:
        request = urllib2.Request(url)
        request.get_method = lambda: 'HEAD'
        response = opener.open(request)
        response.read()
    except Exception, e: # 远程文件不存在
        return 0
    else:
        return int(dict(response.headers)['content-length']) / 1000 / 1000

def gettagClick(name):
    tags = driver.find_elements_by_tag_name('li')
    for ta in tags:
        if ta.get_attribute('innerText') == name:
            ta.click()


def iconcovert(path):
    img = Image.open(path).convert("RGBA")
    new_img = img.resize((160, 160), Image.ANTIALIAS)  # w代表宽度，h代表高度，最后一个参数指   定采用的算法
    # 处理处理图片白边
    x, y = new_img.size
    try:
        # 使用白色来填充背景 from：www.outofmemory.cn
        # (alpha band as paste mask).
        p = Image.new('RGBA', new_img.size, (255, 255, 255))
        p.paste(new_img, (0, 0, x, y), new_img)
        p.save(path)
    except:
        pass
    cmd = pngquantPath + ' ' + path + ' --force --ext .png'
    # 压缩图片大小
    os.system(cmd)


if __name__ == '__main__':

    i = 0;
    if i:
        remove_error_other()
    while (True):

        i = i + 1
        time.sleep(2)
        reinfo = apk.apk_info() #游戏数据
        if not reinfo:
            continue

        print u'-------------------------------- 我是分割线:' + str(
            i) + '--------' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '--------------------------------'
        ename = reinfo['ename']
        icon = reinfo['icon']
        apkname = reinfo['name']
        subname = reinfo['subname']
        page_url = reinfo['page_url']
        sogouname = 'com.' + reinfo['ename'] + '.yyw'
        reinfo['apkname'] = sogouname
        print reinfo['dev_access']
        sogouusename = reinfo['dev_access']['username']
        sougoupassword = reinfo['dev_access']['password']
        reinfo['sgusername'] = sogouusename
        reinfo['sgpassword'] = sougoupassword

        images = reinfo['images']
        if not len(images):
            print '没有截图'
            apk.apk_report_error(reinfo['ename'], '24', "无应用截图")
            continue

        desc = reinfo['desc']
        if not desc:
            print '没有游戏简介'
            apk.apk_report_error(reinfo['ename'], '24', "无副标题")
            continue

        #ICON 压缩处理
        images = reinfo['images']
        imagesurlList = images.split(',')
        apkurl = reinfo['url']
        imagename = dowmload_image(icon)
        imagePath = BASEPATH + '/' + imagename

        iconcovert(imagePath)
        reinfo['icon'] = imagePath

        # 游戏截图
        list = []
        for name in imagesurlList:
            image = dowmload_image(name)
            path = BASEPATH + '/' + image
            img = Image.open(path)
            new_img = img.resize((336, 600), Image.ANTIALIAS)
            new_img.save(path, optimize=True, quality=5)
            print u"应用截图下载路径:" + path
            list.append(path)
        reinfo['images'] = list

        # 获取远程APK包大小
        size = getRemoteFileInfo(apkurl)
        reinfo['apksize'] = str(size)

        # 打印信息
        print u'icon下载路径:' + imagePath
        print u'APK下载路径'+ apkurl
        print u'游戏名:' + apkname
        print u'副标题:' + reinfo['desc']
        print u"APK包大小:" + str(size) + "M"
        print u"版本号:" + ename
        print u"包名：" + sogouname

        while(True):
            if login(reinfo):
                break
            else:
                driver.quit()
                print "login again"
                driver = webdriver.Chrome('/Users/mac04/Downloads/chromedriver')
        try:
            upload_first(reinfo)
        except:
            driver.quit()
            print "upload error"
            apk.apk_report_error(reinfo['ename'],24,'upload_error')
        remove_current_apk(reinfo)
