

# 刷题

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options
from PIL import Image
from paddleocr import PaddleOCR
import re
import cv2
from selenium.webdriver.support.wait import WebDriverWait   #等待类
from selenium.webdriver.support import expected_conditions as EC  #等待条件类
from selenium.webdriver.common.action_chains import ActionChains
from urllib import request
import random


# 无界面
def noInterface(path):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')

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

# 有界面
def interface(path):
    option = webdriver.ChromeOptions()
    option.add_argument(fr'--user-data-dir={path}')
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    # 规避window.navigator.webdriver检测
    option.add_argument("--disable-blink-features=AutomationControlled")
    browser = webdriver.Chrome(options=option)
    return browser

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
        x = random.randint(3, 8)
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


def getTest():
    allTest = []
    while True:
        try:
            shareClass = browser.find_elements(By.XPATH, '//*[@id="sharingClassed"]/div[2]/ul')
            for i in shareClass:
                test = i.find_element(By.XPATH, './div/dl/dt/div[2]/ul/li[2]/div')
                allTest.append(test)
            if len(allTest) > 0:
                print('获取所有测试成功')
                break
        except:
            time.sleep(2)
    return allTest

def getQusetion(options):
    ocr = PaddleOCR(lang='ch')
    result = ocr.ocr('answer.png')
    temp = ''
    for line in result:
        for word in line:
            # 提取数据中的文字元组
            text_line = word[-1]
            # 提取文字元组中的文字内容
            text = text_line[0]
            temp = temp + text
    question = re.findall('.*?(【..题】.*?)A.*', temp)[0] + options
    return question + '，你只需回答：答案+选项'

def cutImg():
    # 安装pillow库
    img = Image.open('question.png')
    # 全屏
    # region = img.crop((495, 651, 2080, 1250))
    region = img.crop((495, 450, 2080, 1450))
    region.save('answer.png')
    print('裁切完毕')

# 接入文心一言回答问题
def yiyan(qusetion):
    # 进入文心一言
    browser.switch_to.window(browser.window_handles[-4])
    textArea = browser.find_element(By.XPATH,'//*[@id="root"]/div[2]/div/div[2]/div/div[2]/div/div[3]/div/div[2]/textarea')
    textArea.send_keys(qusetion)
    send = browser.find_element(By.XPATH, '//*[@id="root"]/div[2]/div/div[2]/div/div[2]/div/div[3]/div/div[3]/span')

    send.click()
    time.sleep(25)
    try:
        response = browser.find_element(By.XPATH,'//*[@id="root"]/div[2]/div/div[2]/div/div[1]/div/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]')
        # print(response.text)
    except:
        print('重新获取resp')
        response = browser.find_element(By.XPATH, '//*[@id="root"]/div[2]/div/div[2]/div/div[1]/div/div/div[3]')
        # print(response.text)
    answer = re.findall('答*案*正*确*.*([A-Z]{1,5}).*',response.text)
    if len(answer) == 0:
        answer = re.findall('(对.*?错.*?)',response.text)
    # 返回答题页面
    browser.switch_to.window(browser.window_handles[-1])
    return list(set(answer))

def auto(allTest):
    for test in allTest:
        test.click()
        time.sleep(3)
        browser.switch_to.window(browser.window_handles[-1])
        print('已经进入答题目录----------------')
        print('\n\n')
        print('\n\n')
        time.sleep(2)

        allStart = browser.find_elements(By.XPATH,'//*[@id="examBox"]/div[1]/ul/li')
        for i in range(1,len(allStart)+2):
            # 打开答题页面
            time.sleep(5)
            startTest = browser.find_element(By.XPATH,f'//*[@id="examBox"]/div[1]/ul/li[{i}]/div/div[2]/div')
            startTest.click()
            time.sleep(3)
            browser.switch_to.window(browser.window_handles[-1])
            print('已进入答题页面--------------------')
            print('\n\n')
            print('\n\n')

            # 题数
            time.sleep(2)
            el_num = browser.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div[2]/div[2]/div[1]/ul/li[2]/span')
            num = int(el_num.text)

            for i in range(2,num+2):
                time.sleep(3)
                options = browser.find_element(By.XPATH,f'//*[@id="app"]/div/div[2]/div[2]/div[2]/div[{i}]/div/div/div[2]').text
                options = options.replace('\n', '')


                # 由于智慧树shadow_root关闭了，并且有js检测，获取不到题目，所以我采用截图识别题目
                browser.save_screenshot('question.png')

                cutImg()

                question = getQusetion(options)
                print(question)

                time.sleep(2)
                answer = yiyan(question)
                print(f'第{i-1}题的答案是')
                print(answer)

                ABCD = browser.find_elements(By.XPATH, f'//*[@id="app"]/div/div[2]/div[2]/div[2]/div[{i}]/div/div/div[2]/div')
                for option in ABCD:
                    for awr in answer:
                        if option.text.find(awr) != -1:
                            option.click()
                time.sleep(1)
                next_btn = browser.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div[2]/div[3]/button[2]')
                next_btn.click()
                time.sleep(2)

            browser.close()
            # 返回答题目录 进入下一个测试
            time.sleep(2)
            browser.switch_to.window(browser.window_handles[-1])

        print('已经做完这个课程测试')
        browser.close()
        browser.switch_to.window(browser.window_handles[0])

    print('所有课程测试都已回答完毕')

def run(url):
    browser.get(url)

    # driver.window_handles
    # 获取当前页面所有的句柄
    # driver.switch_to.window(driver.window_handles[-1])
    # 定位到最新打开窗口
    # driver.switch_to.window(driver.window_handles[-2])
    # 定位到倒数第二个窗口
    # driver.switch_to.window(driver.window_handles[0])
    # 定位最开始的页面

    # 打开并进入智慧树
    js = "window.open('https://onlineweb.zhihuishu.com/onlinestuh5')"
    browser.execute_script(js)
    browser.switch_to.window(browser.window_handles[-1])

    time.sleep(3)
    lonIn()
    time.sleep(8)
    allTest = getTest()
    time.sleep(2)
    auto(allTest)


if __name__ == '__main__':
    url = 'https://yiyan.baidu.com/'


    # 有界面
    # 加载cookie
    # 谷歌cookie保存路径
    # C:\Users\<用户名>\AppData\Local\Google\Chrome\User Data
    # 一份cookie只能给一个浏览器用
    # 需要自己复制这个文件随便放在哪里都行，在把复制的文件地址填入下方
    # path = 'E:\\<文件名>\\<文件名>\\<文件名>'
    path = 'E:\\yuziqizng\\cookie\\UserData'
    browser = interface(path)

    # 无界面
    # 无头模式会使智慧树cookie加载失效，需要打开lohIn里的注释并填入账号密码
    # browser = noInterface(path)

    # 答完题后自动保存，并未提交
    run(url)



