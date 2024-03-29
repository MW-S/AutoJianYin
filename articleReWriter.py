# articleReWriter.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from concurrent.futures import ThreadPoolExecutor

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time, pyperclip, threading, os
# 创建互斥锁
lock = threading.Lock()

def sendContent2Rewriter(content):
    # 获取锁
    lock.acquire()
    try:
        content = f"请在保证内容含义不变且字数不变的情况下使用中文帮我重写以下内容：" + content;
        driver = connectCurrentChrome();
        element = driver.find_element(By.XPATH, '//*[@id="prompt-textarea"]')
        element.clear()
        _ = send_text_with_newlines(element, content)

        sendBtn = driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/div[2]/main/div[2]/div[2]/form/div/div/div/button');
        sendBtn.click();

        count = 0;
        isComplete = False;
        #超时时间为60秒
        startTime = time.time();
        while count<=120:
            time.sleep(1);
            # 检查元素是否存在
            elements = driver.find_elements(By.XPATH, '//*[@id="__next"]/div[1]/div[2]/main/div[2]/div[2]/form/div/div/div/button')
            isComplete = len(elements)>0;
            # if elements:
            #     print("Element exists on the page.")
            # else:
            #     print("Element does not exist on the page.")
            count = count+1;
            if isComplete:
                break;
            else:
                print(f"正在等待文章生成......：{time.time() - startTime}s")
        if not isComplete and count == 60:
            print("错误：回答超时，无法复制！")
            return;
        else:
            return clickCopy(driver);
    finally:
        # 释放锁
        lock.release()

def clickCopy(driver):
    # driver = connectCurrentChrome();
    chatRecordsEl = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/main/div[2]/div[1]/div/div/div');
    print(len(chatRecordsEl.find_elements()))
    # 定位 <div> 元素中的最后一个子元素
    last_child_element = chatRecordsEl.find_element(By.XPATH, './*[last()]')
    last_child_copy_element = last_child_element.find_element(By.XPATH, 'div/div/div[2]/div[2]/div[2]/div/span[1]/button')
    last_child_copy_element.click();
    # 获取剪贴板中的内容
    clipboard_content = pyperclip.paste()
    # 打印剪贴板中的内容
    # print("Clipboard content:", clipboard_content)
    return clipboard_content;


def connectCurrentChrome(address = '127.0.0.1:9222'):
    # 创建Chrome选项
    chrome_options = Options()
    # 设置debuggerAddress，这里的地址应替换为实际从步骤2中获得的调试URL
    chrome_options.add_experimental_option("debuggerAddress", address)
    # 创建一个新的WebDriver实例，指向已打开的浏览器会话
    return webdriver.Chrome(options=chrome_options)

def send_text_with_newlines(element, text):
    lines = text.split("\n")
    for line in lines:
        while not element.is_enabled():
            print("正在等待输入...")
        # 发送换行符
        element.send_keys(Keys.SHIFT+Keys.ENTER);
        while not element.is_enabled():
            print("正在等待输入...")
        element.send_keys(line);

# if __name__ == '__main__':
    # sendContent2Rewriter("你是谁？你来自哪里？1231231");
    # test()

