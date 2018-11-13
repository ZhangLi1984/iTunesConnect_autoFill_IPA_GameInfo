# -*- coding: UTF-8 -*-
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
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


reload(sys)                      # reload 才能调用 setdefaultencoding 方法
sys.setdefaultencoding('utf-8')  # 设置 'utf-8'
xlrd.Book.encoding = "utf8"

# 初始化信息
gameName = raw_input('请输入母包(拼音首字母):')
new_game_fill = raw_input('输入包名:')
driver = webdriver.Chrome('/Users/lz/Downloads/chromedriver3')
# driver = webdriver.Firefox()
# 资料保存的路径可修改
ExcelBasePath = '/Users/lz/Desktop/yyb/'
apkBasePath = '/Volumes/aliyun_package_path/apk/mubao/yingyongbao'
uploadFailedPath = '/Users/lz/Desktop/yyb/mhj/uploadFailed.text'
yywappid = 'gz'

# 上传包表格
gameUploadExcelPath = ExcelBasePath + gameName + '/' + gameName + '.' + 'xlsx'

def upLoadInfo():

    # path = basePath + gameName + 'zhanghao.xlsx'
    # print "EXCEL表格路径:" + gameUploadExcelPath
    data = xlrd.open_workbook(gameUploadExcelPath);
    try:
        tableinfo = data.sheet_by_index(0)
    except Exception as e:
        print e
        exit()
    # 账号信息表
    lsinfo = []
    listappName = []
    listapkName = []
    listapk = []

    for i in range(tableinfo.nrows):
        lsinfo.append(tableinfo.row_values(i))

    for account in lsinfo:
        appName = account[0]
        apkName = account[1]
        apk = account[2]
        listappName.append(appName)
        listapkName.append(apkName)
        listapk.append(apk)
    return (listappName,listapkName,listapk)

def login():

    driver.get('http://open.qq.com/login')
    driver.switch_to.frame('login_frame')
    # driver.switch_to.frame('login_frame')  # 需先跳转到iframe框架
    driver.maximize_window()
    time.sleep(5)
    driver.find_element_by_id('switcher_plogin').click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="u"]').send_keys('3402143438 ')
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="p"]').send_keys('UU123456')
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="login_button"]').click()
    time.sleep(8)
    try:
        # driver.find_element_by_class_name('cover')
        '//*[@id="j-guide-box"]/div[2]/div[2]/a'
        '//*[@id="j-guide-box"]/div[3]/div/div[2]/a'
        '//*[@id="j-guide-box"]/div[4]/div/div[2]/a'
        '//*[@id="j-guide-box"]/div[5]/div/div[2]/a'
        '/html/body/div[3]/div[2]/a'

        driver.find_element_by_xpath('//*[@id="j-guide-box"]/div[2]/div[2]/a').click()
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="j-guide-box"]/div[3]/div/div[2]/a').click()
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="j-guide-box"]/div[4]/div/div[2]/a').click()
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="j-guide-box"]/div[5]/div/div[2]/a').click()
        time.sleep(1)
        driver.execute_script("window.scrollTo(0,-100)")
        driver.find_element_by_xpath('/html/body/div[3]/div[2]/a').click()
        time.sleep(1)
    except Exception as e:
        print e
    print '账号登录成功'
    driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div/div[2]/div/div[2]/div/ul/li[2]/div[2]/div[1]').click()
    time.sleep(5)
    switchHandle(1)
    switchIframe()
    upLoad()

def switchHandle(number):
    handle = driver.window_handles;
    # print handle
    print '***************** 切换 window_handle ************************'
    driver.switch_to.window(handle[number]);
    time.sleep(2)

def switchIframe():
    time.sleep(1)
    frame = driver.find_element_by_id('frame')
    driver.switch_to.frame(frame)
    # print frame
    print '***************** 切换iFrame ************************'

def getTagA(tag):
     el = driver.find_elements_by_tag_name(tag);
     appname = upLoadInfo()[0][0];
     if tag == 'a':
         for name in el:
             if name.get_attribute('innerText') == appname:
                 name.click()
                 time.sleep(5)
     if tag == 'span':
         for name in el:
             st = name.get_attribute('innerText')
             if st.find("%"):
                 print '------------'+st

def upLoad():

    # 点击上传
    driver.find_element_by_xpath('//*[@id="content-1"]/div[1]/div[1]/p[3]/a').click()
    time.sleep(10)
    switchHandle(2)
    switchIframe()
    getTagA('a')
    time.sleep(2)
    print '点击了添加渠道包'
    upLoadApk()

def upLoadApk():

    for i in range(len(upLoadInfo()[0])):

        driver.find_element_by_xpath('//*[@id="modal_cppkg_detail"]/div[2]/div/p/a').click()
        time.sleep(10)
        driver.find_element_by_xpath('//*[@id="modal_upload_cppkg"]/div[2]/div[1]/div[2]/div/div[1]/div/input').send_keys(upLoadInfo()[1][i])
        apkPath = apkBasePath+'/'+upLoadInfo()[2][i]
        print upLoadInfo()[1][i]+' == '+apkPath
        driver.find_element_by_xpath('//*[@id="upload-file"]').click()
        time.sleep(20)
        robotUpLoad(apkPath)
        time.sleep(2)
        #第一次上传 勾选
        if i == 0:
            driver.find_element_by_xpath('//*[@id="modal_upload_cppkg"]/div[2]/div[1]/div[4]/div[1]/div/div/input').click()
        driver.find_element_by_xpath('//*[@id="modal_upload_cppkg"]/div[2]/div[2]/a[1]').click()
        # time.sleep(50)

        while 1:
            print 'while'
            if repeateUpload(apkPath) == 0:
                # print '0'
                break
            elif repeateUpload(apkPath) == 1:
                # print '1'
                break
            elif repeateUpload(apkPath) == 2:
                # print '2'
                break
            time.sleep(2)
        # print '--------------------------------------'
'''
返回值 0 - 上传成功,next
返回值 1 - 上传失败,next
返回值 2 - 抛出异常,next
'''
def repeateUpload(apkPath):
    # print 'repeateUpload'
    try:
        el = driver.find_elements_by_class_name('data')
        for e in el:
            if e.get_attribute('innerText') == ' - Complete':
                print '上传成功,继续上传!'  # 1.上传成功
                print '--------------------------------------sucess-----------------------------------------'
                return 0

        # print len(el)
        if len(el) == 0:  # 上传完成100%,失败
            print '100%,正在检测apk'
            # time.sleep(4)
            if driver.find_element_by_xpath('//*[@id="modal_upload_cppkg"]/div[1]').is_displayed():  # 'cp渠道上传包'是否显示
                faileInfo = driver.find_element_by_xpath(
                    '//*[@id="modal_upload_cppkg"]/div[2]/div[1]/div[5]/div/b/span').text  # 失败信息
                time.sleep(2)
                faileInfodeatil = apkPath + ': ' + faileInfo
                writefalieinfo(faileInfodeatil)  # 写入失败信息
                print '上传失败,失败文件已写入'
                time.sleep(5)
                driver.find_element_by_xpath('//*[@id="modal_upload_cppkg"]/div[1]/a').click()
                print '----------------------------------------failed---------------------------------------'
                return 1
                  # 点击了关闭按钮
            return 1
    except Exception as e:
        print e
        print "异常上传失败"
        print '-----------------------------------exception--------------------------------------------'
        time.sleep(3)
        try:
            driver.find_element_by_xpath('//*[@id="modal_upload_cppkg"]/div[1]/a').click()
        except Exception as e:
            return 2
        return 2

def writefalieinfo(apkpath):
    with open(uploadFailedPath, 'a') as f:
        f.write(apkpath)
        f.write('\n')

# 上传失败
def upLoadApkFaile(apkPath):
    driver.find_element_by_xpath('//*[@id="upload-file"]').click()
    time.sleep(10)
    robotUpLoad(apkPath)
    time.sleep(2)
    # driver.find_element_by_xpath('//*[@id="modal_upload_cppkg"]/div[2]/div[1]/div[4]/div[1]/div/div/input').click()
    driver.find_element_by_xpath('//*[@id="modal_upload_cppkg"]/div[2]/div[2]/a[1]').click()
    #print '点击了提交''

#粘贴apk路径到粘贴板
def paste(foo):
    pyperclip.copy(foo)
    pyautogui.hotkey('command', 'v')

# 模拟按键上传apk包
def robotUpLoad(apkPath):
    # pyautogui.keyDown('command')
    # pyautogui.press('tab')
    # pyautogui.press('tab')
    # pyautogui.keyUp('command')
    # time.sleep(10)
    pyautogui.keyDown('command')
    pyautogui.keyDown('shift')
    pyautogui.keyDown('g')
    pyautogui.keyUp('command')
    pyautogui.keyUp('shift')
    pyautogui.keyUp('g')
    time.sleep(5)
    paste(apkPath)
    time.sleep(5)
    pyautogui.press('enter')
    time.sleep(5)
    pyautogui.press('enter')
    time.sleep(3)

login()

    # driver.switch_to_frame("aid-auth-widget-iFrame")
    # driver.find_element_by_id("account_name_text_field").send_keys(zhanghao()[1])
    # driver.find_element_by_id("sign-in").click()
    # time.sleep(5)
    # driver.find_element_by_id("password_text_field").send_keys(zhanghao()[2])
    # time.sleep(1)
    # driver.find_element_by_id("sign-in").click()
    # print '账号登录成功!!!!!!'
    # time.sleep(25)
    # driver.find_elements_by_class_name("icon-wrapper")[0].click()
    # print '点击了我的App'
    # time.sleep(28)
    # # driver.find_element_by_link_text(zhanghao()[0]).click()  # 点击那个APP
    # try:
    #     # 点击创建的游戏
    #     driver.find_element_by_link_text(zhanghao()[0] + '-').click()
    #     time.sleep(8)
    #     if new_game_fill == '0':
    #         neigou()
    #     elif new_game_fill == '1':
    #         print '现在开始填写游戏资料'
    #         try:
    #             filltext()
    #         except Exception as e:
    #             print e
    #             print '资料填写错误'
    #     else:
    #         print '输入错误'
    #         # 填写APP资料提交审核
    # except Exception as e:
    #     # print e.encode('utf-8')
    #     print '未找到对应游戏名,开始新建游戏'
    #     newGame()
    #     # 新建游戏



# upLoadInfo()[0]
# print "----------"
# print upLoadInfo()[0]
# print upLoadInfo()[1]
# print upLoadInfo()[2]
#
# print len(upLoadInfo()[0])





#
# # 游戏资料表
# gameInfoPath = basePath + gameName + '/' + gameName + '.' + 'xlsx'
# # 内购ID表
# path = basePath + gameName + '/' + 'data' + '.' + 'xls'
#
#
# # 游戏基本资料
# def gameInfo():
#     data = xlrd.open_workbook(gameInfoPath)
#     try:
#         tabinfo = data.sheet_by_index(0)
#     except Exception as e:
#         exit()
#         print '未找到游戏资料表'
#     lsInfo = []
#     for i in range(tabinfo.nrows):
#         lsInfo.append(tabinfo.row_values(i)[1])
#     return lsInfo
#
#
# # 上传表格
# def zhanghao():
#     path = basePath + gameName +'zhanghao.xlsx'
#     data = xlrd.open_workbook(path);
#     try:
#         tableinfo = data.sheet_by_index(0)
#     except Exception as e:
#         print e
#         exit()
#     # 账号信息表
#     lsinfo = []
#     for i in range(tableinfo.nrows):
#         lsinfo.append(tableinfo.row_values(i))
#     for account in lsinfo:
#         if account[1] == gameName:
#             appname = account[0]
#             zhanghao = account[2]
#             password = account[3]
#             connect = account[4]
#             phone = account[5]
#     return (appname, zhanghao, password, connect, phone)
#
# # 登录
# def login():
#     driver.get('https://itunesconnect.apple.com/login')
#     time.sleep(25)
#     driver.switch_to_frame("aid-auth-widget-iFrame")
#     driver.find_element_by_id("account_name_text_field").send_keys(zhanghao()[1])
#     driver.find_element_by_id("sign-in").click()
#     time.sleep(5)
#     driver.find_element_by_id("password_text_field").send_keys(zhanghao()[2])
#     time.sleep(1)
#     driver.find_element_by_id("sign-in").click()
#     print '账号登录成功!!!!!!'
#     time.sleep(25)
#     driver.find_elements_by_class_name("icon-wrapper")[0].click()
#     print '点击了我的App'
#     time.sleep(28)
#     # driver.find_element_by_link_text(zhanghao()[0]).click()  # 点击那个APP
#     try:
#         # 点击创建的游戏
#         driver.find_element_by_link_text(zhanghao()[0] + '-').click()
#         time.sleep(8)
#         if new_game_fill == '0':
#             neigou()
#         elif new_game_fill == '1':
#             print '现在开始填写游戏资料'
#             try:
#                 filltext()
#             except Exception as e:
#                 print e
#                 print '资料填写错误'
#         else:
#             print '输入错误'
#             # 填写APP资料提交审核
#     except Exception as e:
#         # print e.encode('utf-8')
#         print '未找到对应游戏名,开始新建游戏'
#         newGame()
#         # 新建游戏
#
# def newGame():
#     print '开始新建游戏...'
#     driver.find_element_by_xpath('//*[@id="control-bar"]/div[1]/div[1]/a').click()
#     time.sleep(1)
#     driver.find_element_by_xpath('//*[@id="new-menu"]/div[1]/a').click()
#     time.sleep(8)
#
#     # el = driver.find_element_by_link_text('请在此处注册一个').is_displayed()
#     # if el:
#     #     driver.find_element_by_link_text('请在此处注册一个').click()
#     #     print '请在此注册一个'
#     #     time.sleep(10)
#     #     newCer()
#     #     return
#
#     # 平台
#
#     driver.find_element_by_xpath('//*[@id="platforms"]/span/div[1]/div/span/a').click()
#     # APP名字
#     driver.find_element_by_xpath(
#         '//*[@id="main-ui-view"]/div[3]/div[1]/div/div/div/div/div[2]/form/div/div[5]/span/input').send_keys(
#         zhanghao()[0] + '-')
#     selectLanguade = Select(driver.find_element_by_xpath(
#         '//*[@id="main-ui-view"]/div[3]/div[1]/div/div/div/div/div[2]/form/div/div[6]/span/select'))
#     selectLanguade.select_by_visible_text('简体中文')
#     # 选择ID
#     selectID = Select(driver.find_element_by_xpath(
#         '//*[@id="main-ui-view"]/div[3]/div[1]/div/div/div/div/div[2]/form/div/div[7]/span[1]/select'))
#     appIdName = gameName + ' ' + '-' + ' ' + 'com.' + gameName + '.' + yywappid
#     try:
#         # 找不到游戏名ID
#         selectID.select_by_visible_text(appIdName)
#     except Exception as e:
#         # 等待十秒再次检查游戏名ID
#         print '未找到对应APPID,开始创建证书'
#         driver.find_element_by_xpath(
#             '//*[@id="main-ui-view"]/div[3]/div[1]/div/div/div/div/div[2]/form/div/div[7]/span[2]/a').click()
#         # 创建证书
#         newCer()
#         return
#
#     # SKU
#     driver.find_element_by_xpath(
#         '//*[@id="main-ui-view"]/div[3]/div[1]/div/div/div/div/div[2]/form/div/div[10]/span/input').send_keys(gameName)
#     time.sleep(3)
#     # 用户访问权限
#     driver.find_element_by_xpath(
#         '//*[@id="main-ui-view"]/div[3]/div[1]/div/div/div/div/div[2]/form/div/div[11]/span/div/div[2]/div/span/a').click()
#     # 创建
#     driver.find_element_by_xpath('//*[@id="main-ui-view"]/div[3]/div[1]/div/div/div/div/div[3]/div/button[2]').click()
#     time.sleep(10)
#     print '新建游戏完成!!!!!!'
#     neigou()  # 填写内购
#
#
# # 创建证书
# def newCer():
#     print('开始创建AppID...')
#     time.sleep(20)
#     # driver.find_element_by_xpath('//*[@id="ios-nav"]/li[3]/ul/li[1]/a/span').click()
#     # 点击APP IDs
#     url = 'https://developer.apple.com/account/ios/identifier/bundle/create'
#     driver.execute_script("window.location.href='" + url + "'")
#     time.sleep(4)
#     # App ID Description
#     driver.find_element_by_xpath('//*[@id="subcontent"]/div[2]/div/div[3]/form/div[1]/dl/dd/input').send_keys(gameName)
#     # Bundle ID
#     bundleid = 'com.' + gameName + '.' + yywappid
#     driver.find_element_by_xpath(
#         '//*[@id="subcontent"]/div[2]/div/div[3]/form/div[1]/div/div[2]/div[1]/dl/dd/input').send_keys(bundleid)
#     time.sleep(2)
#     # 提交
#     driver.find_element_by_xpath('//*[@id="subcontent"]/div[2]/div/div[3]/form/div[2]/button').click()
#     time.sleep(4)
#     # register
#
#     driver.find_element_by_xpath('//*[@id="subcontent"]/div[2]/div/div[3]/form/div[2]/button[2]').click()
#     time.sleep(5)
#     # Done
#     driver.find_element_by_xpath('//*[@id="subcontent"]/div[2]/div/div[3]/div[2]/button').click()
#     time.sleep(1)
#     print 'AppID创建完成!!!!!!'
#
#     print '开始创建证书...'
#     # 开始创建证书
#     driver.find_element_by_xpath('//*[@id="ios-nav"]/li[5]/ul/li[1]/a/span').click()
#     time.sleep(1)
#
#     url1 = 'https://developer.apple.com/account/ios/profile/create'
#     driver.execute_script("window.location.href='" + url1 + "'")
#     time.sleep(5)
#     # iOS App Developement
#     driver.find_element_by_xpath('//*[@id="type-development"]').click()
#     # conitinue
#     driver.find_element_by_xpath('//*[@id="subcontent"]/div[2]/div/div[3]/div[2]/form/div[2]/a[2]/span').click()
#     time.sleep(2)
#     # 选择APP ID
#     select_ID()
#
#     driver.find_element_by_xpath('//*[@id="subcontent"]/div[2]/div/div[3]/form/div[2]/a[3]/span').click()
#     time.sleep(2)
#     # 选择全部证书
#     driver.find_element_by_xpath('//*[@id="selectAllCId"]').click()
#     driver.find_element_by_xpath('//*[@id="subcontent"]/div[2]/div/div[3]/form/div[2]/a[3]/span').click()
#     # 选择全部设备ID
#     driver.find_element_by_xpath('//*[@id="selectAllDId"]').click()
#     driver.find_element_by_xpath('//*[@id="subcontent"]/div[2]/div/div[3]/form/div[2]/a[3]/span').click()
#     # 填写证书的名字
#     devCerName = gameName + '_dev'
#     driver.find_element_by_xpath('//*[@id="subcontent"]/div[2]/div/div[3]/div[2]/dl/dd[1]/input').send_keys(devCerName)
#     driver.find_element_by_xpath('//*[@id="subcontent"]/div[2]/div/div[3]/div[3]/a[3]/span').click()
#     time.sleep(3)
#     # 下载证书
#     driver.find_element_by_xpath('//*[@id="subcontent"]/div[2]/div/div[3]/div[2]/div[2]/a/span').click()
#     time.sleep(3)
#     # 完成
#     driver.find_element_by_xpath('//*[@id="subcontent"]/div[2]/div/div[3]/div[3]/a[2]/span').click()
#     print 'dev证书创建完成!!!!!!'
#     time.sleep(3)
#
#     # dis证书创建
#     # a 标签无法点击
#     driver.find_element_by_xpath('//*[@id="subcontent"]/div[2]/div[1]/div[1]/div/div/a').click()
#     time.sleep(1)
#
#     driver.find_element_by_xpath('//*[@id="type-production"]').click()
#     driver.find_element_by_xpath('//*[@id="subcontent"]/div[2]/div/div[3]/div[2]/form/div[2]/a[2]/span').click()
#     time.sleep(2)
#     select_ID()
#     # 继续
#     driver.find_element_by_xpath('//*[@id="subcontent"]/div[2]/div/div[3]/form/div[2]/a[3]/span').click()
#     time.sleep(2)
#     driver.find_element_by_name('certificateIds').click()
#     time.sleep(1)
#     driver.find_element_by_xpath('//*[@id="subcontent"]/div[2]/div/div[3]/form/div[2]/a[3]/span').click()
#     time.sleep(3)
#     driver.find_element_by_xpath('//*[@id="subcontent"]/div[2]/div/div[3]/div[2]/dl/dd[1]/input').send_keys(
#         gameName + '_dis')
#     driver.find_element_by_xpath('//*[@id="subcontent"]/div[2]/div/div[3]/div[3]/a[3]/span').click()
#     time.sleep(2)
#     driver.find_element_by_xpath('//*[@id="subcontent"]/div[2]/div/div[3]/div[2]/div[2]/a/span').click()
#     driver.find_element_by_xpath('//*[@id="subcontent"]/div[2]/div/div[3]/div[3]/a[2]/span').click()
#     time.sleep(2)
#     print 'dis证书创建完成!!!!!!'
#
#     # #adhoc证书创建
#     # driver.find_element_by_xpath('//*[@id="subcontent"]/div[2]/div[1]/div[1]/div/div/a').click()
#     # time.sleep(2)
#     # driver.find_element_by_xpath('//*[@id="type-adhoc"]').click()
#     # #继续
#     # driver.find_element_by_xpath('//*[@id="subcontent"]/div[2]/div/div[3]/div[2]/form/div[2]/a[2]/span').click()
#     # time.sleep(3)
#     # select_ID()
#     # #继续
#     # driver.find_element_by_xpath('//*[@id="subcontent"]/div[2]/div/div[3]/form/div[2]/a[3]/span').click()
#     # driver.find_element_by_xpath('certificateIds').click()
#     # driver.find_element_by_xpath('//*[@id="subcontent"]/div[2]/div/div[3]/form/div[2]/a[3]/span').click()
#     # #Device select all
#     # driver.find_element_by_xpath('//*[@id="selectAllDId"]')
#     # driver.find_element_by_xpath('//*[@id="subcontent"]/div[2]/div/div[3]/form/div[2]/a[3]/span').click()
#     # driver.find_element_by_xpath('//*[@id="subcontent"]/div[2]/div/div[3]/div[2]/dl/dd[1]/input').send_keys(gameName+'_adhoc')
#     # driver.find_element_by_xpath('//*[@id="subcontent"]/div[2]/div/div[3]/div[3]/a[3]/span').click()
#     # time.sleep(1)
#     # #download
#     # driver.find_element_by_xpath('//*[@id="subcontent"]/div[2]/div/div[3]/div[2]/div[2]/a/span').click()
#     # time.sleep(2)
#     # print 'adhoc证书创建完毕'
#     print '证书创建完毕.'
#     print '----------------------------'
#     print '重新登录!!!!!!'
#     # 重新登录
#     login()
#
# # APPID下拉框选择
def select_ID():
    js = "var vals = '';window.document.querySelectorAll('select[name=appIdId] option').forEach((d)=>{if(d.innerText.indexOf('" + gameName + "') >= 0){ vals = d.innerText}}); return vals;"
    sel_s = driver.execute_script(js)
    selectID = Select(driver.find_element_by_tag_name('select'))
    selectID.select_by_visible_text(sel_s)
    time.sleep(2)
#
#
# # 填写内购信息
# def save(row, index):
#     print row[1]  # 打印内购ID
#     time.sleep(1)
#     driver.find_element_by_link_text("功能").click()
#     time.sleep(5)
#     driver.find_element_by_xpath("//a[@class='addIcon ng-scope']").click()
#     time.sleep(5)
#     # 消耗型还是非续期订阅
#     if row[5] == 0:
#         driver.find_elements_by_xpath("//a[@class='radiostyle']")[3].click()
#     else:
#         driver.find_elements_by_xpath("//a[@class='radiostyle']")[0].click()
#
#     time.sleep(5)
#     # driver.find_element_by_xpath("//button[text()='创建']").click()
#     driver.find_element(By.XPATH, '//button[text()="创建"]').click()
#     time.sleep(5)
#     driver.find_element_by_xpath(
#         '//*[@id="iapwrapper"]/div[1]/form/div[5]/table/tbody/tr[2]/td[1]/div[1]/div[1]').click()  # 价格等级
#     time.sleep(2)
#     if amount[row[2]]:
#         driver.find_element_by_xpath(amount[row[2]]).click()
#         # driver.find_element_by_xpath('//*[@id="tierSelectionID"]/div/table/tbody/tr[1]/td').click()  # 选择价格等级
#
#     driver.find_element_by_xpath('//*[@id="iapwrapper"]/div[1]/form/div[4]/div[1]/div[1]/span/input').send_keys(row[0])
#     driver.find_element_by_xpath('//*[@id="iapwrapper"]/div[1]/form/div[4]/div[2]/div[2]/span/input').send_keys(row[1])
#     driver.find_element_by_xpath(
#         '//*[@id="iapwrapper"]/div[1]/form/div[9]/div[2]/div[2]/div/div[1]/div/span/input').send_keys(row[3])
#
#     driver.find_element_by_xpath(
#         '//*[@id="iapwrapper"]/div[1]/form/div[9]/div[2]/div[2]/div/div[3]/div/span/input').send_keys(row[4])
#     driver.find_element_by_xpath(
#         '//*[@id="iapwrapper"]/div[1]/form/div[9]/div[2]/div[4]/div/div[1]/div[1]/div/div[2]/div[2]/div/div/div/span/input').send_keys(
#         basePath + gameName + '/' + row[6])  # 上传图片
#     time.sleep(25)
#     driver.find_element_by_xpath('//*[@id="buttonGroupHeader"]/button[1]/span[2]').click()  # 储存
#     time.sleep(10)
#
#     # 获取内购的APPID：
#     dr = driver.find_element_by_xpath('//*[@id="iapwrapper"]/div[1]/form/div[4]/div[2]/div[1]/div/p').text;
#     # print ('行数：'+str(index)+'____'+'内购APPID:'+dr)
#     style = xlwt.easyxf('');
#     writeExcel(index, 7, dr, style);
#     # value = dr.value_of_css_property('innerHTML')
#     # //*[@id="iapwrapper"]/div[1]/form/div[4]/div[2]/div[1]/div/p
#     # //*[@id="iapwrapper"]/div[1]/form/div[4]/div[2]/div[1]/div/p
#
#     el = driver.find_element_by_xpath('//*[@id="buttonGroupHeader"]/button[2]/span[2]').is_enabled()
#     if el:
#         driver.find_element_by_xpath('//*[@id="buttonGroupHeader"]/button[2]/span[2]').click()  # 提交审核
#     time.sleep(5)
#     # 提示是否储存
#     saveEl = driver.find_element_by_xpath(
#         '//*[@id="main-ui-view"]/div[4]/div/div[2]/div[4]/div/div/div/div[2]/div[1]/button').is_displayed();
#     if saveEl:
#         driver.find_element_by_xpath(
#             '//*[@id="main-ui-view"]/div[4]/div/div[2]/div[4]/div/div/div/div[2]/div[1]/button').click();
#     time.sleep(10);
#
#
# # 内购的APPID 写入Excel
# def writeExcel(row, col, str, styl=Style.default_style):
#     rb = xlrd.open_workbook(path, formatting_info=True)
#     wb = copy(rb)
#     ws = wb.get_sheet(0)
#     ws.write(row, col, str, styl)
#     wb.save(path)
#
# # 内购的表格
# def neigou():
#     print '现在开始填写内购项目'
#
#     print '内购ID表格路径 = ' + path
#     try:
#         data = xlrd.open_workbook(path)
#     except Exception as e:
#         print '请检查该路径下是否创建Excel表格'
#         exit()
#     try:
#         tableinfo = data.sheet_by_index(0)
#     except Exception as e:
#         print '检查表格的名字是否正确'
#         exit()
#     list = []  # 内购表
#     for i in range(tableinfo.nrows):
#         # list 每行的数组
#         list.append(tableinfo.row_values(i))
#     print '开始填写内购ID'
#     for pngname in range(len(list)):
#         try:
#             save(list[pngname], pngname);
#         except Exception as e:
#             print e
#
# # 填写游戏资料并提交审核
# def filltext():
#     print '开始填写资料...'
#     # 名称
#     driver.find_element_by_xpath('//*[@id="localizationSection"]/div[2]/div[1]/div[1]/span/input').clear()
#     driver.find_element_by_xpath('//*[@id="localizationSection"]/div[2]/div[1]/div[1]/span/input').send_keys(
#         zhanghao()[0] + '-' + gameInfo()[0])
#     # 副标题
#     driver.find_element_by_xpath('//*[@id="localizationSection"]/div[2]/div[1]/div[2]/span/input').send_keys(
#         gameInfo()[1])
#     # 类别
#     select = Select(driver.find_element_by_xpath(
#         '//*[@id="appStorePageContent"]/div[3]/div[1]/form/div[7]/div[2]/div/div[2]/div[2]/span/span/select'))
#     select.select_by_visible_text('游戏')
#     # 储存
#     driver.find_element_by_xpath('//*[@id="appStorePageInfoHeaderId"]/div[2]/button/span[2]').click()
#     time.sleep(3)
#     print 'APP信息！！！！'
#     # 价格与销售范围
#     driver.find_element_by_link_text('价格与销售范围').click()
#     time.sleep(15)
#     driver.find_element_by_xpath(
#         '//*[@id="main-ui-view"]/div[5]/div/div[3]/div[2]/div[1]/div[4]/div/table/tbody/tr[2]/td[1]/div[1]/div[1]').click()
#     driver.find_element_by_xpath('//*[@id="tierSelectionID"]/div/table/tbody/tr[1]/td').click()
#     driver.find_element_by_xpath('//*[@id="appVerionInfoHeaderId"]/div[2]/button').click()
#     time.sleep(10)
#     print '价格与销售范围！！！！'
#
#     # 1.0 准备提交
#     driver.find_element_by_link_text('1.0 准备提交').click()
#     time.sleep(8)
#     print '1.0准备提交'
#
#     driver.find_element_by_xpath(
#         '//*[@id="localizationSection"]/div[2]/div[3]/div[1]/div[1]/div/div[1]/ul/li[2]/a/div/div').click();
#     # 1242图片上传
#     uploadImages(0)
#     print '1024_截图上传完成'
#     driver.find_element_by_xpath(
#         '//*[@id="localizationSection"]/div[2]/div[3]/div[1]/div[1]/div/div[1]/ul/li[3]/a/div/div').click();
#     # 2048图片上传
#     uploadImages(1)
#     print '2048_截图上传完成'
#     time.sleep(5)
#
#     # print gameInfo()[0]  # 副标题
#     # print gameInfo()[1]  # 分类文案
#     # print gameInfo()[2]  # 游戏简介
#     # print gameInfo()[3]  # 关键词1
#     # print gameInfo()[4]  # 关键词2
#     # print gameInfo()[5]  # 关键词3
#     # print gameInfo()[6]  # 关键词4
#     # 游戏简介
#     driver.find_element_by_xpath('//*[@id="localizationSection"]/div[2]/div[4]/div[2]/span/span/textarea').send_keys(
#         gameInfo()[2])
#     # 关键词
#     driver.find_element_by_xpath('//*[@id="localizationSection"]/div[2]/div[5]/div[1]/span/input').send_keys(
#         gameInfo()[3])
#     # 技术支持网址
#     driver.find_element_by_xpath('//*[@id="localizationSection"]/div[2]/div[5]/div[2]/span/input').clear()
#     driver.find_element_by_xpath('//*[@id="localizationSection"]/div[2]/div[5]/div[2]/span/input').send_keys(
#         'http://www.leizi.online')
#
#     # 构建版本
#     el = driver.find_element_by_xpath(
#         '//*[@id="appStorePageContent"]/div[3]/div[1]/form/div/div[2]/h1/a').is_displayed()
#     if (el):
#         driver.find_element_by_xpath('//*[@id="appStorePageContent"]/div[3]/div[1]/form/div/div[2]/h1/a').click()
#         time.sleep(4)
#         driver.find_element_by_xpath(
#             '//*[@id="appStorePageContent"]/div[3]/div[1]/form/div/div[2]/div[1]/div/div/div/div/div[1]/div[2]/table/tbody/tr/td[1]/div/span/a').click()
#         time.sleep(2);
#         driver.find_element_by_xpath(
#             '//*[@id="appStorePageContent"]/div[3]/div[1]/form/div/div[2]/div[1]/div/div/div/div/div[2]/div/button[2]').click()
#         time.sleep(4)
#
#     # 版权
#     driver.find_element_by_xpath(
#         '//*[@id="appStorePageContent"]/div[3]/div[1]/form/div/div[3]/div/div[2]/div[1]/span/input').send_keys(
#         '2108' + gameName)
#     # 姓
#     driver.find_element_by_xpath(
#         '//*[@id="appStorePageContent"]/div[3]/div[1]/form/div/div[3]/div/div[2]/div[3]/div[3]/div[1]/div[1]/span/input').send_keys(
#         zhanghao()[3])
#     # 名字
#     driver.find_element_by_xpath(
#         '//*[@id="appStorePageContent"]/div[3]/div[1]/form/div/div[3]/div/div[2]/div[3]/div[3]/div[1]/div[2]/span/input').send_keys(
#         zhanghao()[3])
#     # 电话号码
#     driver.find_element_by_xpath(
#         '//*[@id="appStorePageContent"]/div[3]/div[1]/form/div/div[3]/div/div[2]/div[3]/div[3]/div[6]/div[2]/span/input').send_keys(
#         zhanghao()[4])
#     # 电子邮件
#     driver.find_element_by_xpath(
#         '//*[@id="appStorePageContent"]/div[3]/div[1]/form/div/div[3]/div/div[2]/div[3]/div[3]/div[6]/div[3]/span/input').send_keys(
#         zhanghao()[1])
#
#     # 分级按钮点击
#     driver.find_element_by_link_text('编辑').click()
#     driver.find_element_by_xpath(
#         '//*[@id="appStorePageContent"]/div[3]/div[1]/form/div/div[3]/div/div[1]/div[3]/div[1]/div/div/div/div[1]/table/tbody/tr[1]/td[3]/div/span/a').click()
#     driver.find_element_by_xpath(
#         '//*[@id="appStorePageContent"]/div[3]/div[1]/form/div/div[3]/div/div[1]/div[3]/div[1]/div/div/div/div[1]/table/tbody/tr[2]/td[2]/div/span/a').click()
#     driver.find_element_by_xpath(
#         '//*[@id="appStorePageContent"]/div[3]/div[1]/form/div/div[3]/div/div[1]/div[3]/div[1]/div/div/div/div[1]/table/tbody/tr[3]/td[2]/div/span/a').click()
#     driver.find_element_by_xpath(
#         '//*[@id="appStorePageContent"]/div[3]/div[1]/form/div/div[3]/div/div[1]/div[3]/div[1]/div/div/div/div[1]/table/tbody/tr[4]/td[2]/div/span/a').click()
#     driver.find_element_by_xpath(
#         '//*[@id="appStorePageContent"]/div[3]/div[1]/form/div/div[3]/div/div[1]/div[3]/div[1]/div/div/div/div[1]/table/tbody/tr[5]/td[2]/div/span/a').click()
#     driver.find_element_by_xpath(
#         '//*[@id="appStorePageContent"]/div[3]/div[1]/form/div/div[3]/div/div[1]/div[3]/div[1]/div/div/div/div[1]/table/tbody/tr[6]/td[2]/div/span/a').click()
#     driver.find_element_by_xpath(
#         '//*[@id="appStorePageContent"]/div[3]/div[1]/form/div/div[3]/div/div[1]/div[3]/div[1]/div/div/div/div[1]/table/tbody/tr[7]/td[2]/div/span/a').click()
#     driver.find_element_by_xpath(
#         '//*[@id="appStorePageContent"]/div[3]/div[1]/form/div/div[3]/div/div[1]/div[3]/div[1]/div/div/div/div[1]/table/tbody/tr[8]/td[2]/div/span/a').click()
#     driver.find_element_by_xpath(
#         '//*[@id="appStorePageContent"]/div[3]/div[1]/form/div/div[3]/div/div[1]/div[3]/div[1]/div/div/div/div[1]/table/tbody/tr[10]/td[2]/div/span/a').click()
#     driver.find_element_by_xpath(
#         '//*[@id="appStorePageContent"]/div[3]/div[1]/form/div/div[3]/div/div[1]/div[3]/div[1]/div/div/div/div[1]/table/tbody/tr[11]/td[2]/div/span/a').click()
#     driver.find_element_by_xpath(
#         '//*[@id="appStorePageContent"]/div[3]/div[1]/form/div/div[3]/div/div[1]/div[3]/div[1]/div/div/div/div[1]/table/tbody/tr[9]/td[2]/div/span/a').click()
#     driver.find_element_by_xpath(
#         '//*[@id="appStorePageContent"]/div[3]/div[1]/form/div/div[3]/div/div[1]/div[3]/div[1]/div/div/div/div[1]/table/tbody/tr[13]/td[2]/div/span/a').click()
#     driver.find_element_by_xpath(
#         '//*[@id="appStorePageContent"]/div[3]/div[1]/form/div/div[3]/div/div[1]/div[3]/div[1]/div/div/div/div[1]/table/tbody/tr[14]/td[2]/div/span/a').click()
#     # 完成
#     driver.find_element_by_xpath(
#         '//*[@id="appStorePageContent"]/div[3]/div[1]/form/div/div[3]/div/div[1]/div[3]/div[1]/div/div/div/div[5]/div/button[2]').click()
#     time.sleep(2)
#
#     # 内购
#     driver.find_element_by_xpath('//*[@id="appStorePageContent"]/div[3]/div[1]/form/div/div[4]/h1/a').click()
#     driver.find_element_by_xpath(
#         '//*[@id="appStorePageContent"]/div[3]/div[1]/form/div/div[4]/div[1]/div/div/div/div/div[1]/table/thead/tr/th[1]/span/a').click()
#     driver.find_element_by_xpath(
#         '//*[@id="appStorePageContent"]/div[3]/div[1]/form/div/div[4]/div[1]/div/div/div/div/div[2]/div/button[2]').click()
#     # 需要登录审核账号
#     driver.find_element_by_xpath(
#         '//*[@id="appStorePageContent"]/div[3]/div[1]/form/div/div[6]/div[1]/div[1]/div/div[2]/div[1]/span/input').send_keys(
#         'tainss');
#     driver.find_element_by_xpath(
#         '//*[@id="appStorePageContent"]/div[3]/div[1]/form/div/div[6]/div[1]/div[1]/div/div[2]/div[2]/span/input').send_keys(
#         'ent123');
#     # APP审核信息 姓氏，名字，电话号码 联系人
#     driver.find_element_by_xpath(
#         '//*[@id="appStorePageContent"]/div[3]/div[1]/form/div/div[6]/div[1]/div[2]/div/div[1]/div[3]/div[1]/span/input').send_keys(
#         zhanghao()[3]);  # 姓
#     driver.find_element_by_xpath(
#         '//*[@id="appStorePageContent"]/div[3]/div[1]/form/div/div[6]/div[1]/div[2]/div/div[1]/div[3]/div[2]/span/input').send_keys(
#         zhanghao()[3]);  # 名
#     driver.find_element_by_xpath(
#         '//*[@id="appStorePageContent"]/div[3]/div[1]/form/div/div[6]/div[1]/div[2]/div/div[2]/div[3]/span/input').send_keys(
#         zhanghao()[4]);  # 电话
#     driver.find_element_by_xpath(
#         '//*[@id="appStorePageContent"]/div[3]/div[1]/form/div/div[6]/div[1]/div[2]/div/div[2]/div[4]/span/input').send_keys(
#         zhanghao()[1]);  # 邮箱
#     # #版本发布 手动
#     driver.find_element_by_xpath(
#         '//*[@id="appStorePageContent"]/div[3]/div[1]/form/div/div[7]/div[3]/div[1]/div/div/span/a').click()
#     time.sleep(2)
#     # 点击储存
#     driver.find_element_by_xpath('//*[@id="appVerionInfoHeaderId"]/div[2]/button[1]').click()
#     time.sleep(20)
#
#     KeyWordsList = gameInfo()[4:]
#     # 4填写关键词
#     # window 滚动到顶部
#     # driver.execute_script("window.scrollTo(0,-1000)")
#     time.sleep(1)
#     print '填写其他语言：繁体中文-英文澳大利亚-英文英国'
#     # 繁体中文 - 英文澳大利亚 -英文英国 - 英文美国 - ....
#     for index in range(len(KeyWordsList)):
#         if index == 0:
#             driver.find_element_by_xpath('//*[@id="verlocHeader"]/div/a').click();
#             driver.find_element_by_xpath('//*[@id="applocalizations"]/div/table/tbody/tr[17]/td[1]').click()  # 繁体中文
#         elif index == 1:
#             driver.find_element_by_xpath('//*[@id="verlocHeader"]/div/a').click();
#             driver.find_element_by_xpath('//*[@id="applocalizations"]/div/table/tbody/tr[20]/td[1]').click()  # 英文澳大利亚
#         elif index == 2:
#             driver.find_element_by_xpath('//*[@id="verlocHeader"]/div/a').click();
#             driver.find_element_by_xpath('//*[@id="applocalizations"]/div/table/tbody/tr[22]/td[1]').click()  # 英文英国
#         elif index == 3:
#             driver.find_element_by_xpath('//*[@id="verlocHeader"]/div/a').click();
#             driver.find_element_by_xpath('//*[@id="applocalizations"]/div/table/tbody/tr[21]/td[1]').click()  # 英文美国
#         elif index == 4:
#             driver.find_element_by_xpath('//*[@id="verlocHeader"]/div/a').click();
#             driver.find_element_by_xpath('//*[@id="applocalizations"]/div/table/tbody/tr[23]/td[1]').click()  # 其他语言？
#         driver.find_element_by_xpath('//*[@id="localizationSection"]/div[2]/div[5]/div[1]/span/input').send_keys(
#             KeyWordsList[index])  # 关键词
#         driver.find_element_by_xpath(
#             '//*[@id="localizationSection"]/div[2]/div[4]/div[2]/span/span/textarea').send_keys(gameInfo()[2])  # 简介
#     # 储存
#     driver.find_element_by_xpath('//*[@id="appVerionInfoHeaderId"]/div[2]/button[1]').click()
#     time.sleep(10)
#
#     # 提交审核
#     driver.find_element_by_xpath('//*[@id="appVerionInfoHeaderId"]/div[2]/button[2]').click()
#     time.sleep(15)
#     print '提交审核！！！！'
#     # 出口合规信息
#     driver.find_element_by_xpath(
#         '//*[@id="main-ui-view"]/div[4]/div/div[3]/div[3]/div/div[2]/div[1]/form/div[4]/div[2]/div/div[2]/div[2]/div/span/a').click()
#     # 内容版权
#     ac = driver.find_element_by_xpath('//*[@id="rights-group-1"]/div/div/div[2]/div/span/a').is_enabled()
#     if ac:
#         driver.find_element_by_xpath('//*[@id="rights-group-1"]/div/div/div[2]/div/span/a').click()
#     # 广告标识符
#     driver.find_element_by_xpath(
#         '//*[@id="main-ui-view"]/div[4]/div/div[3]/div[3]/div/div[2]/div[1]/form/div[6]/div/div[2]/div[1]/div/span/a').click()
#     driver.find_element_by_xpath(
#         '//*[@id="main-ui-view"]/div[4]/div/div[3]/div[3]/div/div[2]/div[1]/form/div[6]/div/div[1]/div[1]/div[1]/div/span/a').click()
#     driver.find_element_by_xpath(
#         '//*[@id="main-ui-view"]/div[4]/div/div[3]/div[3]/div/div[2]/div[1]/form/div[6]/div/div[1]/div[2]/div/div/span/a').click()
#     # 提交
#     driver.find_element_by_xpath('//*[@id="submitForReviewActionBar"]/div/button[2]').click()
#     time.sleep(5)
#     print '👍👍👍提交审核完毕👍👍👍！！！！'
#     return
#
# # 上传游戏截图：
# def uploadImages(index):
#     imagePaths_1242 = [basePath + gameName + '/images/1242/1.jpg',
#                        basePath + gameName + '/images/1242/2.jpg',
#                        basePath + gameName + '/images/1242/3.jpg',
#                        basePath + gameName + '/images/1242/4.jpg',
#                        basePath + gameName + '/images/1242/5.jpg']
#
#     imagePaths_2048 = [basePath + gameName + '/images/2048/1.jpg',
#                        basePath + gameName + '/images/2048/2.jpg',
#                        basePath + gameName + '/images/2048/3.jpg',
#                        basePath + gameName + '/images/2048/4.jpg',
#                        basePath + gameName + '/images/2048/5.jpg']
#     list = []
#     if index == 0:
#         list = imagePaths_1242
#     else:
#         list = imagePaths_2048
#     for index in range(len(list)):
#         if index == 0:
#             driver.find_element_by_xpath('//*[@id="mainDropTrayFileSelect"]').send_keys(list[index]);
#             time.sleep(25)
#
#             driver.find_element_by_xpath(
#                 '//*[@id="main-ui-view"]/div[5]/div/div[3]/div[5]/div[2]/div/div/div/div[2]/div/button').click()
#             time.sleep(5)
#         else:
#             driver.find_element_by_xpath('//*[@id="mainDropTrayFileSelect"]').send_keys(list[index]);
#             time.sleep(20)
#     time.sleep(2)
#
#
# print '------------------------'
# print u'游戏 :' + zhanghao()[0]
# print u'账号 :' + zhanghao()[1]
# print u'密码 :' + zhanghao()[2]
# print u'联系人:' + zhanghao()[3]
# print u'电话号码:' + zhanghao()[4]
# print 'APPID:' + 'com.' + gameName + '.' + yywappid
# print '-----------------------'
#
# # 登录--start
# login()
#
# # print gameInfo()[0]#副标题
# # print gameInfo()[1]#分类文案
# # print gameInfo()[2]#游戏简介
# # print gameInfo()[3]#关键词1
# # print gameInfo()[4]#关键词2
# # print gameInfo()[5]#关键词3
# # print gameInfo()[6]#关键词4

