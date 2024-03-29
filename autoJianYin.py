# autoJianYin.py
import ctypes
import time, os, sys

import pyperclip

from Utills import retry_function
from autoUtill import clickComponent, getAppByTitle, setEditComponent, getRectangleByTitle,\
    getComponentByTitle, waitOrWaitNotComponent, getComponentByTitleAndAutoID, getChildComponentByTitleAndAutoID, getApp

sys.coinit_flags = 2  # COINIT_APARTMENTTHREADED

from pathlib import Path
from pywinauto.application import Application
from pywinauto import mouse, Desktop, keyboard
from docx import Document

def clickTaskJianYin(taskExePath = 'D:\\JianyingPro\\5.2.0.11062\\JianyingPro.exe'):
    # 创建Desktop对象
    desktop = Desktop(backend='uia')
    # 查找任务栏窗口
    taskbar = desktop.window(class_name='Shell_TrayWnd')
    # 遍历任务栏上的按钮来找到你想要激活的窗口按钮
    target = (taskbar.child_window(title="运行中的应用程序", control_type="ToolBar")).child_window(auto_id=taskExePath, control_type="Button")
    target.click_input();
def reTitle(cancelVideoOutBasePos, title):
    # offsets = calculateOffSet(cancelVideoOutBasePos, 1160, 251)
    # print(offsets);
    cancelVideoOutPos = getComponentXY(cancelVideoOutBasePos, 0.81, 0.09);
    mouse.click(button='left', coords=(cancelVideoOutPos[0], cancelVideoOutPos[1]));
    time.sleep(1)
    pyperclip.copy(title);
    paste()
    # print("点击导出生成完成")
def paste():
    # 定义键代码
    VK_CONTROL = 0x11
    VK_A = 0x41
    VK_DELETE = 0x2E
    #   Ctrl + A 全选
    ctypes.windll.user32.keybd_event(VK_CONTROL, 0, 0, 0)  # 按下Ctrl
    ctypes.windll.user32.keybd_event(VK_A, 0, 0, 0)  # 按下A
    ctypes.windll.user32.keybd_event(VK_A, 0, 2, 0)  # 释放A
    ctypes.windll.user32.keybd_event(VK_CONTROL, 0, 2, 0)  # 释放Ctrl
    time.sleep(0.5);
    #   DELETE 删除
    ctypes.windll.user32.keybd_event(VK_DELETE, 0, 0, 0)  # 按下DELETE
    ctypes.windll.user32.keybd_event(VK_DELETE, 0, 2, 0)  # 释放DELETE
    time.sleep(0.5);
    # Ctrl + V 粘贴
    ctypes.windll.user32.keybd_event(VK_CONTROL, 0, 0, 0)  # 按下Ctrl
    ctypes.windll.user32.keybd_event(0x56, 0, 0, 0)  # 按下V
    ctypes.windll.user32.keybd_event(0x56, 0, 2, 0)  # 释放V
    ctypes.windll.user32.keybd_event(VK_CONTROL, 0, 2, 0)  # 释放Ctrl
def calculateOffSet(basePos, x, y):
    w = basePos.right - basePos.left;
    h = basePos.bottom - basePos.top;
    xOffset = round((x-basePos.left)/w, 2)
    yOffSet = round((y-basePos.top)/h, 2)
    return [xOffset, yOffSet]
def getComponentXY(basePos, xOffset, yOffSet):
    return [int(basePos.right * xOffset + (1 - xOffset) * basePos.left),
                         int(basePos.bottom * yOffSet + (1 - yOffSet) * basePos.top)]
def readWordRun(filePath):
    """
       剪映自动生成配音与字幕。
       参数:
       * file_path -- Word文件路径。
    """
    doc = Document(filePath);
    full_text = []  # 用于存储文档的全部文本
    file_path = Path(filePath)

    # 遍历文档中的所有段落和表格
    for para in doc.paragraphs:
        full_text.append(para.text)
    # 将所有文本合并为一个长字符串
    full_text_str = '\n'.join(full_text)
    autoGenerate(full_text_str, file_path.stem)

def autoGenerate(contentText = '123', title="测试"):
    # 读取文本信息
    # 定义应用程序的执行文件名和窗口标题
    executable = r'D:\JianyingPro\JianyingPro.exe'
    window_title = '剪映专业版'
    # # 尝试连接到已经打开的应用程序
    # try:
    #     app = Application(backend='uia').connect(title=window_title, timeout=5)
    #     print("应用程序已经打开并连接成功。")
    # except Exception as e:
    #     print("无法连接到应用程序，可能是因为它没有打开或者窗口标题不正确。尝试启动应用程序...")
    #     try:
    #         # 启动应用程序
    #         os.system(f"start {executable}");
    #         time.sleep(5);
    #         app = Application(backend='uia').connect(title=window_title, timeout=5)
    #         print("应用程序已成功启动。")
    #     except Exception as e:
    #         print("无法启动应用程序。
    app = getApp(window_title, executable);
    autoGenerate_First(app, window_title, contentText);
    autoGenerate_Two(app, window_title, title);

# 主页面操作，点击关闭BGM音轨，并且点击导出打开文件夹
def autoGenerate_Two(app, window_title, title):
    print("进入第二阶段生成")
    jianyinMainWindows = getComponentByTitleAndAutoID(app, window_title, "MainWindow", 600, 20)
    print("剪辑窗口出现")
    # clickTaskJianYin();
    jianyinMainWindows.set_focus();
    # jianyinMainWindows.print_control_identifiers();
    print("等待BGM轨道静音按钮")
    waitOrWaitNotComponent(jianyinMainWindows, "GroupBox13", 0, 20, 5)
    # jianyinMainWindows['GroupBox13'].wait('visible', timeout=20, retry_interval=5)
    # bottomPanel = jianyinMainWindows['GroupBox13']
    # BGM轨道静音
    basePos = jianyinMainWindows.rectangle();
    mouse.click(button='left', coords=(basePos.left + 97, basePos.bottom - 98))
    print("BGM轨道静音完成")
    # 点击导出
    # jianyinMainWindows['GroupBox4'].wait('visible', timeout=20, retry_interval=5)
    waitOrWaitNotComponent(jianyinMainWindows, "GroupBox4", 0, 20, 5)
    # exportBasePos =  (jianyinMainWindows['GroupBox4']).rectangle();
    exportBasePos = getRectangleByTitle(app, window_title, "GroupBox4", jianyinMainWindows);
    exportPos = [int((exportBasePos.left + exportBasePos.right) / 2), int((exportBasePos.top + exportBasePos.bottom)/2)]
    mouse.click(button='left', coords=(exportPos[0], exportPos[1]));

    print("右上角导出按钮点击完成")
    # jianyinMainWindows.child_window(title="导出", auto_id="ExportWindow_Container").wait('visible', timeout=20, retry_interval=5);
    # #点击取消视频导出(默认取消则不需要点击)
    # videoOutBase = jianyinMainWindows.child_window(title="导出", auto_id="ExportWindow_Container");
    videoOutBase = getChildComponentByTitleAndAutoID(jianyinMainWindows, "导出", "ExportWindow_Container");
    # videoOutBase.print_control_identifiers();
    # videoOutBase["GroupBox"]["Static"]
    time.sleep(1);
    cancelVideoOutBasePos = videoOutBase.rectangle();
    # cancelVideoOutPos = getComponentXY(cancelVideoOutBasePos, 0.57, 0.23);
    # mouse.click(button='left', coords=(cancelVideoOutPos[0], cancelVideoOutPos[1]));
    # print("点击取消视频导出完成")
    # time.sleep(1);
    #点击导出生成
    reTitle(cancelVideoOutBasePos, title);
    time.sleep(1);
    cancelVideoOutPos = getComponentXY(cancelVideoOutBasePos, 0.79, 0.95);
    mouse.click(button='left', coords=(cancelVideoOutPos[0], cancelVideoOutPos[1]));
    print("点击导出生成完成")
    #打开文件夹
    time.sleep(5);
    # print(cancelVideoOutBasePos);
    # videoOutBase = jianyinMainWindows.child_window(title="导出", auto_id="ExportWindow_Container");
    videoOutBase = getChildComponentByTitleAndAutoID(jianyinMainWindows, "导出", "ExportWindow_Container");
    cancelVideoOutBasePos = videoOutBase.rectangle();
    # print(cancelVideoOutBasePos);
    # offsets = calculateOffSet(cancelVideoOutBasePos, 1147, 644)
    # print(offsets);
    clickPos = getComponentXY(cancelVideoOutBasePos, 0.79, 0.9);
    # print(clickPos);
    mouse.click(button='left', coords=(clickPos[0], clickPos[1]));
    print("打开文件夹完成")

#自动打开剪映点击图文成片功能进行生成视频

def autoGenerate_First(app, window_title, contentText):
    # app.window(title=window_title).wait('visible', timeout=60, retry_interval=5)
    # jianyinPcWindows = app.window(title=window_title, auto_id="HomeWindow");
    # jianyinPcWindows.set_focus();
    # jianyinPcWindows['Static13'].wait('visible', timeout=20, retry_interval=5)
    # jianyinPcWindows['Static13'].click_input();
    clickComponent(app, window_title, "Static13")
    app2WindowsTitle = "图文成片"
    componentTitle = "图文成片";
    app2 = getAppByTitle(app2WindowsTitle);
    pic2Video = getComponentByTitle(app2, componentTitle);
    # # pic2Video.print_control_identifiers()
    # pic2Video['Static4'].click_input();
    clickComponent(app2, componentTitle, "Static4", pic2Video)

    setEditComponent(app2, componentTitle, "Edit", contentText, pic2Video)
    # pic2Video['Edit'].wait('visible', timeout=10, retry_interval=1)
    # #time.sleep(0.5)
    # textEdit =  pic2Video['Edit'];
    # textEdit.set_edit_text("");
    # textEdit.set_edit_text(contentText);

    # 暂时无法选择配音员
    clickComponent(app2, componentTitle, "GroupBox7", pic2Video)
    # pic2Video['GroupBox7'].click_input();
    # pic2Video['JianyingPro'].print_control_identifiers();

    # pic2Video['JianyingPro'].wait('visible', timeout=10, retry_interval=1)
    # pos = (pic2Video['JianyingPro']).rectangle();
    pos = getRectangleByTitle(app2, componentTitle, "JianyingPro", pic2Video);
    # 选择最近使用的第一个配音员
    mouse.click(button='left', coords=(pos.left + 129, pos.top + 93))
    # 选择最近使用的第二个配音员
    # mouse.click(button='left', coords=(pos.left + 129, pos.top + 121))
    # pic2Video['JianyingPro'].wait_not('visible', timeout=10, retry_interval=1)
    waitOrWaitNotComponent(pic2Video, "JianyingPro", 1);
    # 点击生成视频
    # nearPos = (pic2Video['GroupBox7']).rectangle();
    nearPos = getRectangleByTitle(app2, componentTitle, "GroupBox7", pic2Video);
    mouse.click(button='left', coords=(nearPos.right + 50, nearPos.bottom - 15))  # 点击生成视频
    # pic2Video['JianyingPro'].wait('visible', timeout=10, retry_interval=1)
    waitOrWaitNotComponent(pic2Video, "JianyingPro");
    mouse.click(button='left', coords=(nearPos.right, nearPos.bottom - 155))  # 点击智能匹配素材


# Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     # clickTaskJianYin("D:\\JianyingPro\\5.2.0.11062\\JianyingPro.exe");
#     # autoGenerate();
#     readWordRun(r"J:\storyFile\学姐别怕，我来保护你\改写版本\改_学姐别怕，我来保护你_4-6.docx")
    # autoGenerate()



