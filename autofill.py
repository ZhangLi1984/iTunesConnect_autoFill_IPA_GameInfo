# -*- coding: UTF-8 -*-
import time
import  os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import xlrd
xlrd.Book.encoding = "utf8"

#初始化信息
gameName = raw_input('请输入游戏简称(拼音首字母):')
new_game_fill = raw_input('请输入0或者1(0代表新建游戏,1代表填写资料):')
driver = webdriver.Chrome()

#资料保存的路径可修改
basePath = '/Users/lz/Desktop/chubao/'
amount = {}
amount[6] = '//*[@id="tierSelectionID"]/div/table/tbody/tr[1]/td'
amount[12] = '//*[@id="tierSelectionID"]/div/table/tbody/tr[3]/td'
amount[18] = '//*[@id="tierSelectionID"]/div/table/tbody/tr[3]/td'
amount[25] = '//*[@id="tierSelectionID"]/div/table/tbody/tr[4]/td'
amount[30] = '//*[@id="tierSelectionID"]/div/table/tbody/tr[5]/td'
amount[68] = '//*[@id="tierSelectionID"]/div/table/tbody/tr[10]/td'
amount[98] = '//*[@id="tierSelectionID"]/div/table/tbody/tr[15]/td'
amount[108] = '//*[@id="tierSelectionID"]/div/table/tbody/tr[16]/td'
amount[128] = '//*[@id="tierSelectionID"]/div/table/tbody/tr[20]/td'
amount[198] = '//*[@id="tierSelectionID"]/div/table/tbody/tr[30]/td'
amount[328] = '//*[@id="tierSelectionID"]/div/table/tbody/tr[50]/td'
amount[488] = '//*[@id="tierSelectionID"]/div/table/tbody/tr[54]/td'
amount[648] = '//*[@id="tierSelectionID"]/div/table/tbody/tr[60]/td'
amount[1] = '//*[@id="tierSelectionID"]/div/table/tbody/tr[88]/td'
amount[3] = '//*[@id="tierSelectionID"]/div/table/tbody/tr[89]/td'
amount[8] = '//*[@id="tierSelectionID"]/div/table/tbody/tr[90]/td'

#游戏基本资料
def gameInfo():
    gameInfoPath = basePath+gameName+'/'+gameName+'.'+'xlsx'
    data = xlrd.open_workbook(gameInfoPath)
    try:
        tabinfo = data.sheet_by_index(0)
    except Exception as e:
        exit()
        print '未找到游戏资料表'
    lsInfo = []
    for i in range(tabinfo.nrows):
        lsInfo.append(tabinfo.row_values(i)[1])
    return lsInfo
#账号表格
def zhanghao():
    path = basePath+'zhanghao.xlsx'
    data = xlrd.open_workbook(path);
    try:
        tableinfo = data.sheet_by_index(0)
    except Exception as e:
        print e
        exit()
# 账号信息表
    lsinfo = []
    for i in range(tableinfo.nrows):
     lsinfo.append(tableinfo.row_values(i))
    for account in lsinfo:
     if account[1] == gameName:
        appname = account[0]
        zhanghao = account[2]
        password = account[3]
        connect = account[4]
        phone = account[5]
    return (appname,zhanghao,password,connect,phone)
#登录
def login():
    driver.get('https://itunesconnect.apple.com/login')
    time.sleep(18)
    driver.switch_to_frame("aid-auth-widget-iFrame")
    driver.find_element_by_id("account_name_text_field").send_keys(zhanghao()[1])
    driver.find_element_by_id("sign-in").click()
    time.sleep(3)
    driver.find_element_by_id("password_text_field").send_keys(zhanghao()[2])
    time.sleep(1)
    driver.find_element_by_id("sign-in").click()
    print '账号登录成功!!!!!!'
    time.sleep(8)
    driver.find_element_by_class_name("icon-wrapper").click()
    print '点击了我的App'
    time.sleep(28)
    # driver.find_element_by_link_text(zhanghao()[0]).click()  # 点击那个APP
    try:
        #点击创建的游戏
        driver.find_element_by_link_text(zhanghao()[0]+'-').click()
        time.sleep(8)
        if new_game_fill == '0':
            print '现在开始填写内购项目'
            neigou()
        elif new_game_fill == '1':
            print '现在开始填写游戏资料'
            try:
                filltext()
            except Exception as e:
                print e
                print '资料填写错误'
        else:
            print '输入错误'
        #填写APP资料提交审核
    except Exception as e:
        # print e.encode('utf-8')
        print '未找到对应游戏名,开始新建游戏'
        newGame()
        #新建游戏
#新建游戏
def newGame():
    print '开始新建游戏...'
    driver.find_element_by_xpath('//*[@id="control-bar"]/div[1]/div[1]/a').click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="new-menu"]/div[1]/a').click()
    time.sleep(5)
    #平台
    driver.find_element_by_xpath('//*[@id="platforms"]/span/div[1]/div/span/a').click()
    #APP名字
    driver.find_element_by_xpath('//*[@id="main-ui-view"]/div[3]/div[1]/div/div/div/div/div[2]/form/div/div[4]/span/input').send_keys(zhanghao()[0]+'-')
    selectLanguade = Select(driver.find_element_by_xpath('//*[@id="main-ui-view"]/div[3]/div[1]/div/div/div/div/div[2]/form/div/div[5]/span/select'))
    selectLanguade.select_by_visible_text('简体中文')
    #选择ID
    selectID = Select(driver.find_element_by_xpath('//*[@id="main-ui-view"]/div[3]/div[1]/div/div/div/div/div[2]/form/div/div[6]/span[1]/select'))
    appIdName = gameName+' '+'-'+' '+'com.'+gameName+'.yyw'
    try:
        #找不到游戏名ID
        selectID.select_by_visible_text(appIdName)
    except Exception as e:
        #等待十秒再次检查游戏名ID
        print '未找到对应APPID,开始创建证书'
        # 创建证书
        newCer()
        return
    #SKU
    driver.find_element_by_xpath('//*[@id="main-ui-view"]/div[3]/div[1]/div/div/div/div/div[2]/form/div/div[9]/span/input').send_keys(gameName)
    time.sleep(3)
    #创建
    driver.find_element_by_xpath('//*[@id="main-ui-view"]/div[3]/div[1]/div/div/div/div/div[3]/div/button[2]').click()
    time.sleep(10)
    print '新建游戏完成!!!!!!'
    neigou()#填写内购
#创建证书
def newCer():

    print('开始创建AppID...')
    driver.find_element_by_xpath('//*[@id="main-ui-view"]/div[3]/div[1]/div/div/div/div/div[2]/form/div/div[6]/span[2]/a').click()
    time.sleep(35)
    # driver.find_element_by_xpath('//*[@id="ios-nav"]/li[3]/ul/li[1]/a/span').click()
    #点击APP IDs
    url = 'https://developer.apple.com/account/ios/identifier/bundle/create'
    driver.execute_script("window.location.href='" + url + "'")
    time.sleep(4)
    #App ID Description
    driver.find_element_by_xpath('//*[@id="subcontent"]/div[2]/div/div[3]/form/div[1]/dl/dd/input').send_keys(gameName)
    #Bundle ID
    bundleid = 'com.'+gameName+'.yyw'
    driver.find_element_by_xpath('//*[@id="subcontent"]/div[2]/div/div[3]/form/div[1]/div/div[2]/div[1]/dl/dd/input').send_keys(bundleid)
    time.sleep(2)
    #提交
    driver.find_element_by_xpath('//*[@id="subcontent"]/div[2]/div/div[3]/form/div[2]/button').click()
    time.sleep(3)
    #register
    driver.find_element_by_xpath('//*[@id="subcontent"]/div[2]/div/div[3]/form/div[3]/button[2]').click()
    time.sleep(5)
    #Done
    driver.find_element_by_xpath('//*[@id="subcontent"]/div[2]/div/div[3]/div[2]/button').click()
    time.sleep(1)
    print 'AppID创建完成!!!!!!'

    print '开始创建证书...'
    #开始创建证书
    driver.find_element_by_xpath('//*[@id="ios-nav"]/li[5]/ul/li[1]/a/span').click()
    time.sleep(1)

    url1 = 'https://developer.apple.com/account/ios/profile/create'
    driver.execute_script("window.location.href='" + url1 + "'")
    time.sleep(5)
    #iOS App Developement
    driver.find_element_by_xpath('//*[@id="type-development"]').click()
    #conitinue
    driver.find_element_by_xpath('//*[@id="subcontent"]/div[2]/div/div[3]/div[2]/form/div[2]/a[2]/span').click()
    time.sleep(2)
    #选择APP ID
    select_ID()

    driver.find_element_by_xpath('//*[@id="subcontent"]/div[2]/div/div[3]/form/div[2]/a[3]/span').click()
    time.sleep(2)
    #选择全部证书
    driver.find_element_by_xpath('//*[@id="selectAllCId"]').click()
    driver.find_element_by_xpath('//*[@id="subcontent"]/div[2]/div/div[3]/form/div[2]/a[3]/span').click()
    #选择全部设备ID
    driver.find_element_by_xpath('//*[@id="selectAllDId"]').click()
    driver.find_element_by_xpath('//*[@id="subcontent"]/div[2]/div/div[3]/form/div[2]/a[3]/span').click()
    #填写证书的名字
    devCerName = gameName+'_dev'
    driver.find_element_by_xpath('//*[@id="subcontent"]/div[2]/div/div[3]/div[2]/dl/dd[1]/input').send_keys(devCerName)
    driver.find_element_by_xpath('//*[@id="subcontent"]/div[2]/div/div[3]/div[3]/a[3]/span').click()
    time.sleep(3)
    #下载证书
    driver.find_element_by_xpath('//*[@id="subcontent"]/div[2]/div/div[3]/div[2]/div[2]/a/span').click()
    time.sleep(3)
    #完成
    driver.find_element_by_xpath('//*[@id="subcontent"]/div[2]/div/div[3]/div[3]/a[2]/span').click()
    print 'dev证书创建完成!!!!!!'
    time.sleep(3)

    #dis证书创建

    #a 标签无法点击
    driver.find_element_by_xpath('//*[@id="subcontent"]/div[2]/div[1]/div[1]/div/div/a').click()
    time.sleep(1)

    driver.find_element_by_xpath('//*[@id="type-production"]').click()
    driver.find_element_by_xpath('//*[@id="subcontent"]/div[2]/div/div[3]/div[2]/form/div[2]/a[2]/span').click()
    time.sleep(2)
    select_ID()
    #继续
    driver.find_element_by_xpath('//*[@id="subcontent"]/div[2]/div/div[3]/form/div[2]/a[3]/span').click()
    time.sleep(2)
    driver.find_element_by_name('certificateIds').click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="subcontent"]/div[2]/div/div[3]/form/div[2]/a[3]/span').click()
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="subcontent"]/div[2]/div/div[3]/div[2]/dl/dd[1]/input').send_keys(gameName+'_dis')
    driver.find_element_by_xpath('//*[@id="subcontent"]/div[2]/div/div[3]/div[3]/a[3]/span').click()
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="subcontent"]/div[2]/div/div[3]/div[2]/div[2]/a/span').click()
    driver.find_element_by_xpath('//*[@id="subcontent"]/div[2]/div/div[3]/div[3]/a[2]/span').click()
    time.sleep(2)
    print 'dis证书创建完成!!!!!!'
    print '证书创建完毕.'
    print '----------------------------'
    print '重新登录!!!!!!'
    #重新登录
    login()
#APPID下拉框选择
def select_ID():
    js = "var vals = '';window.document.querySelectorAll('select[name=appIdId] option').forEach((d)=>{if(d.innerText.indexOf('" + gameName + "') >= 0){ vals = d.innerText}}); return vals;"
    sel_s = driver.execute_script(js)
    selectID = Select(driver.find_element_by_tag_name('select'))
    selectID.select_by_visible_text(sel_s)
    time.sleep(2)
#填写内购信息
def save(row):

    print row[1] #打印内购ID
    time.sleep(1)
    driver.find_element_by_link_text("功能").click()
    time.sleep(5)
    driver.find_element_by_xpath("//a[@class='addIcon ng-scope']").click()
    time.sleep(5)
    # 消耗型还是非续期订阅
    if row[5] == 0:
        driver.find_elements_by_xpath("//a[@class='radiostyle']")[3].click()
    else:
        driver.find_elements_by_xpath("//a[@class='radiostyle']")[0].click()

    time.sleep(5)
    # driver.find_element_by_xpath("//button[text()='创建']").click()
    driver.find_element(By.XPATH, '//button[text()="创建"]').click()
    time.sleep(5)
    driver.find_element_by_xpath(
        '//*[@id="iapwrapper"]/div[1]/form/div[5]/table/tbody/tr[2]/td[1]/div[1]/div[1]').click()  # 价格等级
    time.sleep(2)
    if amount[row[2]]:
        driver.find_element_by_xpath(amount[row[2]]).click()
        # driver.find_element_by_xpath('//*[@id="tierSelectionID"]/div/table/tbody/tr[1]/td').click()  # 选择价格等级

    driver.find_element_by_xpath('//*[@id="iapwrapper"]/div[1]/form/div[4]/div[1]/div[1]/span/input').send_keys(row[0])
    driver.find_element_by_xpath('//*[@id="iapwrapper"]/div[1]/form/div[4]/div[2]/div[2]/span/input').send_keys(row[1])
    driver.find_element_by_xpath(
        '//*[@id="iapwrapper"]/div[1]/form/div[9]/div[2]/div[2]/div/div[1]/div/span/input').send_keys(row[3])

    driver.find_element_by_xpath(
        '//*[@id="iapwrapper"]/div[1]/form/div[9]/div[2]/div[2]/div/div[3]/div/span/input').send_keys(row[4])
    driver.find_element_by_xpath(
        '//*[@id="iapwrapper"]/div[1]/form/div[9]/div[2]/div[4]/div/div[1]/div[1]/div/div[2]/div[2]/div/div/div/span/input').send_keys(
        basePath + gameName + '/' + row[6])  # 上传图片
    time.sleep(15)
    driver.find_element_by_xpath('//*[@id="buttonGroupHeader"]/button[1]/span[2]').click()  # 储存
    time.sleep(10)
    el = driver.find_element_by_xpath('//*[@id="buttonGroupHeader"]/button[2]/span[2]').is_enabled()
    if el:
        driver.find_element_by_xpath('//*[@id="buttonGroupHeader"]/button[2]/span[2]').click()  # 提交审核
    time.sleep(5)
#内购的表格
def neigou():
    path = basePath+gameName+'/'+'data'+'.'+'xlsx'
    print '内购ID表格路径 = '+path
    try:
        data = xlrd.open_workbook(path)
    except Exception as e:
        print '请检查该路径下是否创建Excel表格'
        exit()
    try:
        tableinfo = data.sheet_by_index(0)
    except Exception as e:
        print '检查表格的名字是否正确'
        exit()
    list = []#内购表
    for i in range(tableinfo.nrows):
        list.append(tableinfo.row_values(i))
    print '开始填写内购ID'
    for pngname in list:
       try:
           save(pngname)
       except Exception as e:
           print e
#填写游戏资料并提交审核
def filltext():
    print '开始填写资料...'

    #名称
    driver.find_element_by_xpath('//*[@id="localizationSection"]/div[2]/div[1]/div[1]/span/input').clear()
    driver.find_element_by_xpath('//*[@id="localizationSection"]/div[2]/div[1]/div[1]/span/input').send_keys(zhanghao()[0]+'-'+gameInfo()[0])
    #副标题
    #
    driver.find_element_by_xpath('//*[@id="localizationSection"]/div[2]/div[1]/div[2]/span/input').send_keys(gameInfo()[1])
    #类别
    select = Select(driver.find_element_by_xpath('//*[@id="appStorePageContent"]/div[3]/div[1]/form/div[7]/div[2]/div/div[2]/div[2]/span/span/select'))
    select.select_by_visible_text('游戏')
    #储存
    driver.find_element_by_xpath('//*[@id="appStorePageInfoHeaderId"]/div[2]/button/span[2]').click()
    time.sleep(3)
    print 'APP信息！！！！'
    #价格与销售范围
    driver.find_element_by_link_text('价格与销售范围').click()
    time.sleep(10)
    driver.find_element_by_xpath('//*[@id="main-ui-view"]/div[4]/div/div[3]/div[2]/div[1]/div[4]/div/table/tbody/tr[2]/td[1]/div[1]/div[1]').click()
    driver.find_element_by_xpath('//*[@id="tierSelectionID"]/div/table/tbody/tr[1]/td').click()
    driver.find_element_by_xpath('//*[@id="appVerionInfoHeaderId"]/div[2]/button').click()
    time.sleep(8)
    print '价格与销售范围！！！！'
    #1.0 准备提交
    driver.find_element_by_link_text('1.0 准备提交').click()
    time.sleep(8)
    print '1.0准备提交'
    driver.find_element_by_xpath('//*[@id="localizationSection"]/div[2]/div[3]/div[1]/div[1]/div/div[1]/ul/li[2]/a/div/div').click();
    #1242图片上传
    uploadImages(0)
    print '1024_截图上传完成'
    driver.find_element_by_xpath('//*[@id="localizationSection"]/div[2]/div[3]/div[1]/div[1]/div/div[1]/ul/li[3]/a/div/div').click();
    #2048图片上传
    uploadImages(1)
    print '2048_截图上传完成'
    time.sleep(5)

    # print gameInfo()[0]  # 副标题
    # print gameInfo()[1]  # 分类文案
    # print gameInfo()[2]  # 游戏简介
    # print gameInfo()[3]  # 关键词1
    # print gameInfo()[4]  # 关键词2
    # print gameInfo()[5]  # 关键词3
    # print gameInfo()[6]  # 关键词4
    #游戏简介
    driver.find_element_by_xpath('//*[@id="localizationSection"]/div[2]/div[4]/div[2]/span/span/textarea').send_keys(gameInfo()[2])
    #关键词
    driver.find_element_by_xpath('//*[@id="localizationSection"]/div[2]/div[5]/div[1]/span/input').send_keys(gameInfo()[3])
    #技术支持网址
    driver.find_element_by_xpath('//*[@id="localizationSection"]/div[2]/div[5]/div[2]/span/input').clear()
    driver.find_element_by_xpath('//*[@id="localizationSection"]/div[2]/div[5]/div[2]/span/input').send_keys('http://www.leizi.online')
    #构建版本
    driver.find_element_by_xpath('//*[@id="appStorePageContent"]/div[3]/div[1]/form/div/div[2]/h1/a').click()
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="appStorePageContent"]/div[3]/div[1]/form/div/div[2]/div[1]/div/div/div/div/div[1]/div[2]/table/tbody/tr/td[1]/div/span/a').click()
    driver.find_element_by_xpath('//*[@id="appStorePageContent"]/div[3]/div[1]/form/div/div[2]/div[1]/div/div/div/div/div[2]/div/button[2]').click()
    time.sleep(2)
    #版权
    driver.find_element_by_xpath('//*[@id="appStorePageContent"]/div[3]/div[1]/form/div/div[3]/div/div[2]/div[1]/span/input').send_keys('2108'+gameName)
    #姓
    driver.find_element_by_xpath('//*[@id="appStorePageContent"]/div[3]/div[1]/form/div/div[3]/div/div[2]/div[3]/div[3]/div[1]/div[1]/span/input').send_keys(zhanghao()[3])
    #名字
    driver.find_element_by_xpath('//*[@id="appStorePageContent"]/div[3]/div[1]/form/div/div[3]/div/div[2]/div[3]/div[3]/div[1]/div[2]/span/input').send_keys(zhanghao()[3])
    #电话号码
    driver.find_element_by_xpath('//*[@id="appStorePageContent"]/div[3]/div[1]/form/div/div[3]/div/div[2]/div[3]/div[3]/div[6]/div[2]/span/input').send_keys(zhanghao()[4])
    #电子邮件
    driver.find_element_by_xpath('//*[@id="appStorePageContent"]/div[3]/div[1]/form/div/div[3]/div/div[2]/div[3]/div[3]/div[6]/div[3]/span/input').send_keys(zhanghao()[1])

    #分级按钮点击
    driver.find_element_by_link_text('编辑').click()
    driver.find_element_by_xpath('//*[@id="appStorePageContent"]/div[3]/div[1]/form/div/div[3]/div/div[1]/div[3]/div[1]/div/div/div/div[1]/table/tbody/tr[1]/td[3]/div/span/a').click()
    driver.find_element_by_xpath('//*[@id="appStorePageContent"]/div[3]/div[1]/form/div/div[3]/div/div[1]/div[3]/div[1]/div/div/div/div[1]/table/tbody/tr[2]/td[2]/div/span/a').click()
    driver.find_element_by_xpath('//*[@id="appStorePageContent"]/div[3]/div[1]/form/div/div[3]/div/div[1]/div[3]/div[1]/div/div/div/div[1]/table/tbody/tr[3]/td[2]/div/span/a').click()
    driver.find_element_by_xpath('//*[@id="appStorePageContent"]/div[3]/div[1]/form/div/div[3]/div/div[1]/div[3]/div[1]/div/div/div/div[1]/table/tbody/tr[4]/td[2]/div/span/a').click()
    driver.find_element_by_xpath('//*[@id="appStorePageContent"]/div[3]/div[1]/form/div/div[3]/div/div[1]/div[3]/div[1]/div/div/div/div[1]/table/tbody/tr[5]/td[2]/div/span/a').click()
    driver.find_element_by_xpath('//*[@id="appStorePageContent"]/div[3]/div[1]/form/div/div[3]/div/div[1]/div[3]/div[1]/div/div/div/div[1]/table/tbody/tr[6]/td[2]/div/span/a').click()
    driver.find_element_by_xpath('//*[@id="appStorePageContent"]/div[3]/div[1]/form/div/div[3]/div/div[1]/div[3]/div[1]/div/div/div/div[1]/table/tbody/tr[7]/td[2]/div/span/a').click()
    driver.find_element_by_xpath('//*[@id="appStorePageContent"]/div[3]/div[1]/form/div/div[3]/div/div[1]/div[3]/div[1]/div/div/div/div[1]/table/tbody/tr[8]/td[2]/div/span/a').click()
    driver.find_element_by_xpath('//*[@id="appStorePageContent"]/div[3]/div[1]/form/div/div[3]/div/div[1]/div[3]/div[1]/div/div/div/div[1]/table/tbody/tr[10]/td[2]/div/span/a').click()
    driver.find_element_by_xpath('//*[@id="appStorePageContent"]/div[3]/div[1]/form/div/div[3]/div/div[1]/div[3]/div[1]/div/div/div/div[1]/table/tbody/tr[11]/td[2]/div/span/a').click()
    driver.find_element_by_xpath('//*[@id="appStorePageContent"]/div[3]/div[1]/form/div/div[3]/div/div[1]/div[3]/div[1]/div/div/div/div[1]/table/tbody/tr[9]/td[2]/div/span/a').click()
    driver.find_element_by_xpath('//*[@id="appStorePageContent"]/div[3]/div[1]/form/div/div[3]/div/div[1]/div[3]/div[1]/div/div/div/div[1]/table/tbody/tr[13]/td[2]/div/span/a').click()
    driver.find_element_by_xpath('//*[@id="appStorePageContent"]/div[3]/div[1]/form/div/div[3]/div/div[1]/div[3]/div[1]/div/div/div/div[1]/table/tbody/tr[14]/td[2]/div/span/a').click()
    #完成
    driver.find_element_by_xpath('//*[@id="appStorePageContent"]/div[3]/div[1]/form/div/div[3]/div/div[1]/div[3]/div[1]/div/div/div/div[5]/div/button[2]').click()
    time.sleep(2)

    #内购
    driver.find_element_by_xpath('//*[@id="appStorePageContent"]/div[3]/div[1]/form/div/div[4]/h1/a').click()
    driver.find_element_by_xpath('//*[@id="appStorePageContent"]/div[3]/div[1]/form/div/div[4]/div[1]/div/div/div/div/div[1]/table/thead/tr/th[1]/span/a').click()
    driver.find_element_by_xpath('//*[@id="appStorePageContent"]/div[3]/div[1]/form/div/div[4]/div[1]/div/div/div/div/div[2]/div/button[2]').click()
    #需要登录审核账号
    driver.find_element_by_xpath('//*[@id="appStorePageContent"]/div[3]/div[1]/form/div/div[6]/div[1]/div[1]/div/div[2]/div[1]/span/input').send_keys('tainss');
    driver.find_element_by_xpath('//*[@id="appStorePageContent"]/div[3]/div[1]/form/div/div[6]/div[1]/div[1]/div/div[2]/div[2]/span/input').send_keys('ent123');
    #APP审核信息 姓氏，名字，电话号码 联系人
    driver.find_element_by_xpath('//*[@id="appStorePageContent"]/div[3]/div[1]/form/div/div[6]/div[1]/div[2]/div/div[1]/div[3]/div[1]/span/input').send_keys(zhanghao()[3]);#姓
    driver.find_element_by_xpath('//*[@id="appStorePageContent"]/div[3]/div[1]/form/div/div[6]/div[1]/div[2]/div/div[1]/div[3]/div[2]/span/input').send_keys(zhanghao()[3]);#名
    driver.find_element_by_xpath('//*[@id="appStorePageContent"]/div[3]/div[1]/form/div/div[6]/div[1]/div[2]/div/div[2]/div[3]/span/input').send_keys(zhanghao()[4]);#电话
    driver.find_element_by_xpath('//*[@id="appStorePageContent"]/div[3]/div[1]/form/div/div[6]/div[1]/div[2]/div/div[2]/div[4]/span/input').send_keys(zhanghao()[1]);#邮箱
    # #版本发布 手动
    driver.find_element_by_xpath('//*[@id="appStorePageContent"]/div[3]/div[1]/form/div/div[7]/div[3]/div[1]/div/div/span/a').click()
    time.sleep(2)
    #点击储存
    driver.find_element_by_xpath('//*[@id="appVerionInfoHeaderId"]/div[2]/button[1]').click()
    time.sleep(5)
    KeyWordsList = gameInfo()[4:]

    #4填写关键词
    #window 滚动到顶部
    driver.execute_script("window.scrollTo(0,-1000)")
    time.sleep(1)
    print '填写其他语言：繁体中文-英文澳大利亚-英文英国'
    # 繁体中文 - 英文澳大利亚 -英文英国
    for index in range(len(KeyWordsList)):
        if index == 0:
            driver.find_element_by_xpath('//*[@id="verlocHeader"]/div/a').click();
            driver.find_element_by_xpath('//*[@id="applocalizations"]/div/table/tbody/tr[17]/td[1]').click()#繁体中文
        elif index == 1:
            driver.find_element_by_xpath('//*[@id="verlocHeader"]/div/a').click();
            driver.find_element_by_xpath('//*[@id="applocalizations"]/div/table/tbody/tr[20]/td[1]').click()  # 英文澳大利亚
        elif index == 2:
            driver.find_element_by_xpath('//*[@id="verlocHeader"]/div/a').click();
            driver.find_element_by_xpath('//*[@id="applocalizations"]/div/table/tbody/tr[22]/td[1]').click()  # 英文英国
        driver.find_element_by_xpath('//*[@id="localizationSection"]/div[2]/div[5]/div[1]/span/input').send_keys(KeyWordsList[index])#关键词
        driver.find_element_by_xpath('//*[@id="localizationSection"]/div[2]/div[4]/div[2]/span/span/textarea').send_keys(gameInfo()[2])# 简介
    #储存
    driver.find_element_by_xpath('//*[@id="appVerionInfoHeaderId"]/div[2]/button[1]').click()
    time.sleep(10)

    #提交审核
    driver.find_element_by_xpath('//*[@id="appVerionInfoHeaderId"]/div[2]/button[2]').click()
    time.sleep(13)
    print '提交审核！！！！'
    #出口合规信息
    driver.find_element_by_xpath('//*[@id="main-ui-view"]/div[4]/div/div[3]/div[3]/div/div[2]/div[1]/form/div[4]/div[2]/div/div[2]/div[2]/div/span/a').click()
    #内容版权
    ac = driver.find_element_by_xpath('//*[@id="rights-group-1"]/div/div/div[2]/div/span/a').is_enabled()
    if ac:
        driver.find_element_by_xpath('//*[@id="rights-group-1"]/div/div/div[2]/div/span/a').click()
    #广告标识符
    driver.find_element_by_xpath('//*[@id="main-ui-view"]/div[4]/div/div[3]/div[3]/div/div[2]/div[1]/form/div[6]/div/div[2]/div[1]/div/span/a').click()
    driver.find_element_by_xpath('//*[@id="main-ui-view"]/div[4]/div/div[3]/div[3]/div/div[2]/div[1]/form/div[6]/div/div[1]/div[1]/div[1]/div/span/a').click()
    driver.find_element_by_xpath('//*[@id="main-ui-view"]/div[4]/div/div[3]/div[3]/div/div[2]/div[1]/form/div[6]/div/div[1]/div[2]/div/div/span/a').click()
    #提交
    driver.find_element_by_xpath('//*[@id="submitForReviewActionBar"]/div/button[2]').click()
    time.sleep(5)
    print '👍👍👍提交审核完毕👍👍👍！！！！'
    return
#上传游戏截图：
def uploadImages(index):
    imagePaths_1242 = [basePath + gameName + '/images/1242/1.jpg',
                       basePath + gameName + '/images/1242/2.jpg',
                       basePath + gameName + '/images/1242/3.jpg',
                       basePath + gameName + '/images/1242/4.jpg',
                       basePath + gameName + '/images/1242/5.jpg']

    imagePaths_2048 = [basePath + gameName + '/images/2048/1.jpg',
                       basePath + gameName + '/images/2048/2.jpg',
                       basePath + gameName + '/images/2048/3.jpg',
                       basePath + gameName + '/images/2048/4.jpg',
                       basePath + gameName + '/images/2048/5.jpg']
    list = []
    if index == 0:
        list = imagePaths_1242
    else:
        list = imagePaths_2048
    for index in range(len(list)):
        if index == 0:
            driver.find_element_by_xpath('//*[@id="mainDropTrayFileSelect"]').send_keys(list[index]);
            time.sleep(15)
            driver.find_element_by_xpath('//*[@id="main-ui-view"]/div[4]/div/div[3]/div[5]/div[2]/div/div/div/div[2]/div/button').click()
            time.sleep(3)
        else:
             driver.find_element_by_xpath('//*[@id="mainDropTrayFileSelect"]').send_keys(list[index]);
             time.sleep(15)
    time.sleep(2)

print '------------------------'
print u'游戏 :' +zhanghao()[0]
print u'账号 :' +zhanghao()[1]
print u'密码 :' +zhanghao()[2]
print u'联系人:' +zhanghao()[3]
print u'电话号码:'+zhanghao()[4]
print 'APPID:'+'com.'+gameName+'.yyw'
print '-----------------------'
#登录--start
login()

# print gameInfo()[0]#副标题
# print gameInfo()[1]#分类文案
# print gameInfo()[2]#游戏简介
# print gameInfo()[3]#关键词1
# print gameInfo()[4]#关键词2
# print gameInfo()[5]#关键词3
# print gameInfo()[6]#关键词4

