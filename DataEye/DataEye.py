# -*- coding: UTF-8 -*-
import os
from selenium import webdriver
from PIL import Image
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import sys
import requests
import json
from requests import exceptions
import time,urllib2,difflib
from fateadm_api import FateadmApi
import xlwt
from datetime import datetime


reload(sys)  # reload 才能调用 setdefaultencoding 方法
sys.setdefaultencoding('utf-8')  # 设置 'utf-8'



LOGIN = 'https://www.dataeye.com/ptlogin/v2/index.html#/Login'
LOGIN_NAME = 'morp@yayawan.com'
LOGIN_PWD = '1212123'

pd_id = "112729"
pd_key = "HsfKii2YwtjeyMNlmqMaQQ9Le1XHMzYn"
app_id = "312729"
app_key = "05+HjIfGKIRkuuFhqaoQR21SDx3qSa6c"
pred_type = "20400"
api = FateadmApi(app_id, app_key, pd_id, pd_key)




def login():
    driver.get(LOGIN)
    time.sleep(10)
    driver.find_element_by_xpath('//*[@id="userID"]').send_keys(LOGIN_NAME)
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="password"]').send_keys(LOGIN_PWD)
    code = verify_codeimg()

    while(True):
        time.sleep(10)
        try:
            text = driver.find_element_by_xpath('//*[@id="container"]/div/div/div[2]/div/div/div[2]/div/div/div/div/div[2]/div/a/div/div[1]/p[2]').text
            if u"游戏版" in text:
                print "登录成功"
                break
        except:
            time.sleep(6)
            verify_codeimg()
            pass

def ff_dama(image_data):
    rep = api.Predict(pred_type,image_data)
    return rep


# 验证码识别
def verify_codeimg():
    # 获取截图
    driver.get_screenshot_as_file('CrawlResult/screenshot.png')
    # 获取指定元素位置
    element = driver.find_element_by_xpath('//*[@id="container"]/div/div/div/form/div[3]/img')
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
    driver.find_element_by_xpath('//*[@id="code"]').clear()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="code"]').send_keys(code)
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="container"]/div/div/div/form/div[4]/button').click()
    return res



getLabelMenu_url ='https://adx.dataeye.com/common/getLabelMenu'
listHotProduct = 'https://adx.dataeye.com/product/listHotProduct'
listTopNewProductDay = 'https://adx.dataeye.com/product/listTopNewProductDay'

class DataEye(object):
    def __init__(self):
        self.headers = {
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
        }
        self.base_params = {
        }
    def getLabelMenu(self):

        params = {
           "firstId":"1"
        }
        params.update(self.base_params)
        try:
            re = requests.post(getLabelMenu_url, headers=self.headers, data=params)
            print re.content
            return re.json()
        except Exception as e:
            print e

    def getlistHotProcuct(self,titleA):
        params = {
            'labelIds' :titleA,
            'top': '500',
            'mobileType':''
        }
        s = requests.session()
        for cookie in driver.get_cookies():
            c = {cookie['name']: cookie['value']}
            s.cookies.update(c)

        try:
            re = s.post(listHotProduct, headers=self.headers, data=params)
            print re.json()['content']
            return re.json()['content']
        except Exception as e:
            print e

    def getlistTopNewProductDay(self):

        header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
        }

        s = requests.session()
        for cookie in driver.get_cookies():
            c = {cookie['name']: cookie['value']}
            s.cookies.update(c)
        try:
            re = s.post(listTopNewProductDay, headers=header)
            print 'yes'
            return re.json()
        except Exception as e:
            print e

        # try:
        #     re = requests.post(listTopNewProductDay, headers=header)
        #     return re.json()
        # except Exception as e:
        #     print e

# 经典题材1 角色扮演2  网络游戏3 经营策略4 飞行射击5 动作冒险6 扑克棋牌7 跑酷竞速8 休闲益智9 体育竞技10
list_title = ['经典题材','角色扮演','网络游戏','经营策略','飞行射击' ,'动作冒险' ,'扑克棋牌','跑酷竞速','休闲益智','体育竞技']

# 经典题材
k_data_0 = [11,12,13,14,15,16,17,72] #1
v_data_0 = ['传奇','西游','封神','水浒','三国','隋唐','航海','宫斗'] #1

# 角色扮演
k_data_1 = [18,19,20,21,22,23,24,25,26] #2
v_data_1 = ['魔幻','玄幻','武侠','仙侠','动漫','回合','即时','都市','日韩系']

# 网络游戏
k_data_2 = [27,28,29] #3
v_data_2 = ['卡牌竞技','策略动作','射击']

# 经营策略
k_data_3 = [30,31,32,33,34,35,36] #4
v_data_3 = ['养成','经营','战争','塔防','策略','历史','模拟']

# 飞行射击
k_data_4 = [37,38,39,40,41,42,43] #5
v_data_4 = ['射击','飞行','坦克','狙击','枪战','空战','海战']

# 动作冒险
k_data_5 = [44,45,46,47,48] #6
v_data_5 = ['格斗','冒险','横版','跳跃','街机']

# 扑克棋牌
k_data_6 = [49,50,51,52,53,54] #7
v_data_6 = ['斗地主','棋类','麻将','单机','桌游','纸牌']

# 跑酷竞速
k_data_7 = [55,56,57,58,59] #8
v_data_7 = ['跑酷','赛车','摩托','躲避','竞速']

# 休闲益智
k_data_8 = [60,61,62,63,64,65] #9
v_data_8 = ['休闲','消除','音乐','益智','捕鱼','解谜']

# 体育竞技
k_data_9 = [66,67,68,69,70,71] #10
v_data_9 = ['足球','篮球','桌球','极限','运动','其他球类']


book = xlwt.Workbook(encoding='utf-8', style_compression=0)

def down_icon_name(sheetname,k_data,v_data):
    data = DataEye()
    contents = data.getlistHotProcuct(k_data)
    sheet = book.add_sheet(sheetname, cell_overwrite_ok=True)
    sheet.width = 256 * 20

    for i in range(len(contents)):
        name = contents[i]['productName']
        save(sheet, 0, 0, sheetname)
        save(sheet, i+1, 0, name)

    for i in range(len(k_data)):
        content_sons = data.getlistHotProcuct(k_data[i])
        save(sheet, 0, i + 1, v_data[i])
        for j in range(len(content_sons)):
            name_son = content_sons[j]['productName']
            save(sheet,j+1,i+1,name_son)



def down_new():
    data = DataEye()
    contents = data.getlistTopNewProductDay()
    sheet = book.add_sheet('新品发现', cell_overwrite_ok=True)
    list_conts = contents['content']
    print list_conts

    for i in range(len(list_conts)):
        statDate = list_conts[i]['statDate']
        print statDate
        products = list_conts[i]['products']
        save(sheet, 0, i, statDate)

        for j in range(len(products)):
            productName = products[j]['productName']

            save(sheet, j+1, i, productName)


def save(sheet, row,col,data):
    sheet.col(col).width = 256*20
    sheet.write(row, col,data)
    book.save('./DataEye.xls')

if __name__ == '__main__':

    while (True):

        driver = webdriver.Chrome('/Users/mac04/Downloads/chromedriver')
        driver.set_window_size(1200, 800)

        if int(datetime.now().strftime("%H")) != 14:
            time.sleep(2)
            continue
        try:
            login()
        except Exception as e:
            driver.quit()
            break
        for i in range(len(list_title)):
            if i == 0:
                down_icon_name(list_title[0], k_data_0, v_data_0)
            elif i == 1:
                down_icon_name(list_title[1], k_data_1, v_data_1)
            elif i == 2:
                down_icon_name(list_title[2], k_data_2, v_data_2)
            elif i == 3:
                down_icon_name(list_title[3], k_data_3, v_data_3)
            elif i == 4:
                down_icon_name(list_title[4], k_data_4, v_data_4)
            elif i == 5:
                down_icon_name(list_title[5], k_data_5, v_data_5)
            elif i == 6:
                down_icon_name(list_title[6], k_data_6, v_data_6)
            elif i == 7:
                down_icon_name(list_title[7], k_data_7, v_data_7)
            elif i == 8:
                down_icon_name(list_title[8], k_data_8, v_data_8)
            elif i == 9:
                down_icon_name(list_title[9], k_data_9, v_data_9)

        down_new()

        cmd = 'rsync -avPh ./DataEye.xls /Volumes/data'
        os.system(cmd)
        time.sleep(3500)
