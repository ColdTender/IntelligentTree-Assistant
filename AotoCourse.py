
# 刷课

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options
import cv2
from selenium.webdriver.support.wait import WebDriverWait   #等待类
from selenium.webdriver.support import expected_conditions as EC  #等待条件类
from selenium.webdriver.common.action_chains import ActionChains
from urllib import request
import random
import pyautogui

# 无界面
def noInterface(path):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')

    # 通过pyautogui方法获得屏幕尺寸
    driver_width, driver_height = pyautogui.size()
    chrome_options.add_argument('--window-size=%sx%s' % (driver_width, driver_height))

    # 加载本地谷歌浏览器cookie
    chrome_options.add_argument(fr'--user-data-dir={path}')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])

    # 规避window.navigator.webdriver检测
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")


    # chrome浏览器的安装位置   Chromedriver需在当前py文件的相同路径下
    path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
    chrome_options.binary_location = path
    browser = webdriver.Chrome(chrome_options=chrome_options)
    return browser


def interface(path):
    option = webdriver.ChromeOptions()
    option.add_argument(fr'--user-data-dir={path}')
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    # 规避window.navigator.webdriver检测
    option.add_argument("--disable-blink-features=AutomationControlled")
    browser = webdriver.Chrome(options=option)
    return browser

# 弹窗答题
def response():
    try:
        # 检查是否有弹窗检验
        browser.find_element(By.XPATH, '//div[@id="app"]/div[1]/div[7]/div[@class="el-dialog"]')
        option = browser.find_elements(By.XPATH, '//ul[@class="topic-list"]/li')
        for i in range(len(option)):
            option[i].click()

        # 获取正确答案
        answer = browser.find_element(By.XPATH, "//p[@class='answer']/span").text.split(',')
        print('正确答案是：' + str(answer))

        # 点击正确答案

        for i in range(len(option)):
            print('选项' + str(i) + ':' + option[i].text)
            flag = False
            for j in range(len(answer)):
                if option[i].text.find(answer[j]) != -1:
                    flag = True
                    break
            if (flag == False):
                option[i].click()
        # 点击关闭
        close = browser.find_element(By.XPATH, '//div[@class="btn"]')
        close.click()
        print("答题成功！\t\t\t√")
        play()
        return True
    except:
        try:
            el_close = browser.find_element(By.XPATH, '/html/body/div[5]/div/div[1]/button')
            el_close.click()
            print('关闭el弹窗成功')
        except:
            print('未检测到el弹窗')
        print("未找到弹窗测验\t\t✘")
        return False


# 点击我知道了
def clickIknow():
    try:
        # 检测是否有我知道了
        browser.find_element(By.XPATH, '//div[@id="app"]/div[1]/div[6]')
        # 点击我知道了
        iKnow = browser.find_element(By.XPATH, '//div[@id="app"]/div[1]/div[6]/div[1]/div[3]/span/button')
        iKnow.click()

        print("关闭我知道成功！\t√")
        return True
    except:
        print("未发现我知道了\t\t✘")
        return False


# 点击学前必读
def clickBeforeRead():
    try:
        # 检测是否有学前必读
        browser.find_element(By.XPATH, '//div[@id="app"]/div[1]/div[7]')
        # 点击×
        close = browser.find_element(By.XPATH, '//*[@id="app"]/div/div[6]/div[2]/div[1]/i')
        close.click()
        print("关闭学前必读成功！\t√")
        return True
    except:
        print("未发现学前必读\t\t✘")
        return False


# 获取当前播放时间
def getCurrentTime():
    openControlsBar()
    time = browser.find_element(By.XPATH, '//*[@id="vjs_container"]/div[10]/div[4]/span[1]').text
    print('当前播放时间为：' + time)
    return time


# 获取当前视频总时间
def getTotalTime():
    openControlsBar()
    time = browser.find_element(By.XPATH, '//*[@id="vjs_container"]/div[10]/div[4]/span[2]').text
    print('本集视频时间为：' + time)
    return time


# 播放下一个视频
def nextVideo():
    openControlsBar()
    nextBtn = browser.find_element(By.XPATH, '//div[@id="nextBtn"]')
    nextBtn.click()
    print('\n切换下一个视频\n')


# 1.5速度
def fasterPlay():
    try:
        openControlsBar()
        speed = browser.find_element(By.XPATH, '//div[@class="speedBox"]/div/div[1]')
        speedbox = browser.find_element(By.XPATH, '//div[@class="speedBox"]')
        time.sleep(5)
        openControlsBar()
        ActionChains(browser).move_to_element(speedbox).perform()
        speed.click()
        print('成功切换成' + speed.text + '倍速\t√')
    except:
        print('切换倍速失败，稍后将重试\t✘')


# 点击开始播放
def play():
    start_status = browser.find_element(By.XPATH, '//div[@id="playButton"]').get_attribute('class')
    start_button = browser.find_element(By.XPATH, '//*[@id="vjs_container"]/div[8]')
    # time.sleep(2)
    if start_status.find('playButton') != -1:
        print('当前静止')
        openControlsBar()
        time.sleep(1)
        start_button.click()
        print('点击播放成功\t\t√')


# 点击静音
def noVoice():
    try:
        voice_status = browser.find_element(By.XPATH, '//*[@id="vjs_container"]/div[10]/div[7]').get_attribute('class')
        voice_buttton = browser.find_element(By.XPATH, '//*[@id="vjs_container"]/div[10]/div[7]')

        if voice_status.find('volumeNone') == -1:
            print('此时非静音')
            time.sleep(3)
            openControlsBar()
            voice_buttton.click()
            print('静音成功\t\t\t√')
    except:
        print('静音失败，稍后将重试\t\t✘')


# 切换流畅画质
def changeVideoQuality():
    try:
        openControlsBar()
        videoQuality = browser.find_element(By.XPATH, ' //div[@class="definiBox"]/div/b[1]')
        definiBox = browser.find_element(By.XPATH, ' //div[@class="definiBox"]')
        time.sleep(5)
        openControlsBar()
        ActionChains(browser).move_to_element(definiBox).perform()
        videoQuality.click()
        print('成功切换到流畅画质\t√')
        checkWindow()
    except:
        print('切换到流畅画质失败，稍后将重试\t\t✘')


# 打开ControlsBar
def openControlsBar():
    checkWindow()
    controlsBar = browser.find_element(By.XPATH, ' //div[@id="container"]')
    ActionChains(browser).move_to_element(controlsBar).perform()


# 检测弹窗
def checkWindow():
    print(time.strftime('%Y-%m-%d  %H:%M:%S') + '\n' + '正在播放:' + getUnitName())
    clickIknow()
    clickBeforeRead()
    response()
    print('\n\n')


# 获取当前章节
def getUnitName():
    try:
        name = browser.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div[1]/div[1]/div[1]')
        return name.text
    except:
        return '暂未加载'



# 获取一节，用于对比是否完成
def getEndDirectory():
    view = browser.find_elements(By.XPATH, '//*[@id="app"]/div/div[2]/div[2]/div[2]/div[1]/div/ul/div')
    directory = view[len(view) - 1].text
    return directory

# 获取滑块到缺口的距离
def get_distance():
    '''
    bg: 背景图片
    tp: 缺口图片
    return:空缺距背景图左边的距离
    '''
    # 读取背景图片和缺口图片
    bg_img = cv2.imread('bgimg.png') # 背景图片
    tp_img = cv2.imread('slimg.png') # 缺口图片
    # 识别图片边缘
    bg_edge = cv2.Canny(bg_img, 100, 200)
    tp_edge = cv2.Canny(tp_img, 100, 200)
    # 转换图片格式
    bg_pic = cv2.cvtColor(bg_edge, cv2.COLOR_GRAY2RGB)
    tp_pic = cv2.cvtColor(tp_edge, cv2.COLOR_GRAY2RGB)
    # cv2.imwrite("bg_style.png", bg_pic) # 保存背景轮廓提取
    # cv2.imwrite("slide_style.png", tp_pic) # 保存滑块背景提取
    # 缺口匹配
    res = cv2.matchTemplate(bg_pic, tp_pic, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)  # 寻找最优匹配
    th, tw = tp_pic.shape[:2]
    tl = max_loc  # 左上角点的坐标
    # 返回缺口的左上角X坐标
    br = (tl[0] + tw, tl[1] + th)  # 右下角点的坐标
    cv2.rectangle(bg_img, tl, br, (0, 0, 255), 2)  # 绘制矩形
    cv2.imwrite("result_new.png", bg_img)  # 保存在本地
    # 返回缺口的左上角X坐标
    return tl[0] + 10

# 移动小滑块匹配验证码
def move(distance):
    slider = browser.find_element(By.XPATH, '/html/body/div[31]/div[2]/div/div/div[2]/div/div[2]/div[2]')
    time.sleep(2)
    ActionChains(browser).click_and_hold(slider).perform()
    moved = 0
    while moved < distance:
        x = random.randint(3, 10)
        ActionChains(browser).move_by_offset(xoffset=x, yoffset=0).perform()
        moved += x
    ActionChains(browser).release().perform()

# 登录
def lonIn():

    print(time.strftime('%Y-%m-%d  %H:%M:%S') + '\n' + '开始学习\n')

    # userName = ''
    # passWord = ''
    # time.sleep(3)
    # # 元素定位 输入用户名密码
    # print(time.strftime('%Y-%m-%d  %H:%M:%S') + '\n' + '正在输入账号\n')
    # inputUsername = browser.find_element(By.XPATH, '//input[@id="lUsername"]')
    # inputUsername.send_keys(userName)
    # print(time.strftime('%Y-%m-%d  %H:%M:%S') + '\n' + '账号输入成功\n')
    # print(time.strftime('%Y-%m-%d  %H:%M:%S') + '\n' + '正在输入密码\n')
    # inputPassword = browser.find_element(By.XPATH, '//input[@id="lPassword"]')
    # inputPassword.send_keys(passWord)
    # print(time.strftime('%Y-%m-%d  %H:%M:%S') + '\n' + '密码输入成功\n')

    # 点击登录
    time.sleep(2)
    print(time.strftime('%Y-%m-%d  %H:%M:%S') + '\n' + '正在登陆\n')
    time.sleep(2)
    login = browser.find_element(By.XPATH, "//span[@class='wall-sub-btn']")
    login.click()

    # 破解验证码
    WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[31]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/img[1]')))
    while True:
        try:
            bgImgSrc = browser.find_element(By.XPATH,'/html/body/div[31]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/img[1]').get_attribute('src')
            slImgSrc = browser.find_element(By.XPATH,'/html/body/div[31]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/img[2]').get_attribute('src')
            request.urlretrieve(bgImgSrc, 'bgimg.png')
            request.urlretrieve(slImgSrc, 'slimg.png')
            distance = get_distance()
            move(distance)
            time.sleep(2)
        except:
            print(time.strftime('%Y-%m-%d  %H:%M:%S') + '\n' + '登陆成功\n')
            print(time.strftime('%Y-%m-%d  %H:%M:%S') + '\n' + '正在进入课程\n\n')
            break

    print('----------------------------------')


# 获取所有课程
def getCourse():
    allCourses = []
    while True:
        try:
            shareClass = browser.find_elements(By.XPATH, '//*[@id="sharingClassed"]/div[2]/ul')
            for i in shareClass:
                course = i.find_element(By.XPATH, './div/dl/dt/div[1]/div[1]')
                allCourses.append(course)
            if len(allCourses) > 0:
                print('课程获取成功')
                break
        except:
            time.sleep(2)
    return allCourses

# 视频播放
def auto():
    while (True):

        # 有时进入视频会直接弹出窗口，且窗口显示顺序不定，故检测三次，保证再开始播放之前关闭
        print(time.strftime('%Y-%m-%d  %H:%M:%S') + '\n' + '正在在执行视频播放前检查')
        for i in range(3):
            print('\n第' + str(i) + '检测')
            checkWindow()
            time.sleep(2)

        print(time.strftime('%Y-%m-%d  %H:%M:%S') + '\n检查完毕\n\n\n开始优化播放\n')
        if getEndDirectory().find(getUnitName()) == -1 and getCurrentTime() == getTotalTime():
            browser.back()
            browser.switch_to.window(browser.window_handles[-1])
            time.sleep(2)
            print('--------------------------')
            print('已完成一门课程的播放')
            print('--------------------------')
            break
        # 避免在前三次中未检测出窗口，开始操作前全部检查一次
        # print('正在修改画质')
        checkWindow()
        changeVideoQuality()
        # print('画质修改成功\t\t\t√')
        # print('正在修该播放速度')
        checkWindow()
        fasterPlay()
        # print('播放速度修改成功\t\t\t√')
        # print('正在修改静音')
        checkWindow()
        noVoice()
        # print('静音修改成功\t\t√\n\n')
        checkWindow()
        play()
        time.sleep(5)

        # 每隔5秒检测是否有我知道了，学前必读，是否播放完
        while (True):
            print(time.strftime('%Y-%m-%d  %H:%M:%S'))
            # 播放完毕，下一集
            if getCurrentTime() == getTotalTime():
                print('\n\n')
                checkWindow()
                nextVideo()
                break

            print('\n\n')
            checkWindow()
            print('\n\n')
            time.sleep(5)


def run(url):

    browser.get(url)
    time.sleep(2)
    lonIn()
    time.sleep(8)
    allCourses = getCourse()

    for course in allCourses:
        course.click()
        time.sleep(2)
        auto()

    print('所有课程视频都已经观看完毕')

if __name__ == '__main__':

    # 有界面
    # 加载cookie   需要在文心一言和智慧树上都登陆一次，记录cookie
    # 谷歌cookie保存路径
    # C:\Users\<用户名>\AppData\Local\Google\Chrome\User Data
    # 一份cookie只能给一个浏览器用
    # 需要自己复制这个文件随便放在哪里都行，在把复制的文件地址填入下方path
    # path = 'E:\\<文件名>\\<文件名>\\<文件名>'
    path= 'E:\\yuziqizng\\cookie\\UserData'
    browser = interface(path)

    # 无界面
    # 无头模式会使智慧树cookie加载失效，需要打开lohIn里的注释并填入账号密码
    # # 加载驱动  无界面 加载cookie
    # browser = noInterface(path)

    # 访问网站 课程的地址
    url = 'https://onlineweb.zhihuishu.com/onlinestuh5'

    run(url)











