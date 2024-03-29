# autoUtill.py
import time, os;
from pywinauto.application import Application
from Utills import retry_function

retry_times = 3;
delay = 5;

@retry_function(retry_times, delay)
def clickComponent(app, title, name, parent=None):
    if(parent == None):
        rootWindows = getComponentByTitle(app, title);
    else:
        rootWindows = parent;
    rootWindows.set_focus();
    rootWindows[name].wait('visible', timeout=20, retry_interval=5)
    rootWindows[name].click_input();
    time.sleep(0.5);

@retry_function(retry_times, delay)
def setEditComponent(app, title, name, contentText, parent=None):
    if (parent == None):
        rootWindows = getComponentByTitle(app, title);
    else:
        rootWindows = parent;
    rootWindows.set_focus();
    rootWindows[name].wait('visible', timeout=10, retry_interval=1)
    textEdit = rootWindows[name];
    textEdit.set_edit_text("");
    textEdit.set_edit_text(contentText);
    time.sleep(0.5);

@retry_function(retry_times, delay)
def getRectangleByTitle(app, title, name, parent=None):
    if (parent == None):
        rootWindows = getComponentByTitle(app, title);
    else:
        rootWindows = parent;
    rootWindows[name].wait('visible', timeout=10, retry_interval=1)
    return (rootWindows[name]).rectangle();
@retry_function(retry_times, delay)
def getChildComponentByTitleAndAutoID(app, title, autoId):
    app.window(title=title, auto_id=autoId).wait('visible', timeout=600, retry_interval=20)
    return app.window(title=title, auto_id=autoId);

@retry_function(retry_times, delay)
def getComponentByTitle(app, title):
    app.window(title=title).wait('visible', timeout=60, retry_interval=5)
    return app.window(title=title);

@retry_function(retry_times, delay)
def getComponentByTitleAndAutoID(parent, title, autoId, timeout=20, retry_interval=5):
    parent.window(title=title, auto_id=autoId).wait('visible', timeout=timeout, retry_interval=retry_interval)
    return parent.window(title=title, auto_id=autoId);

@retry_function(retry_times, delay)
def getAppByTitle(title, type="uia"):
    app=Application(backend=type).connect(title=title);
    # app.window(title=title).wait('visible', timeout=30, retry_interval=5);
    return app;

@retry_function(retry_times, delay)
def waitOrWaitNotComponent(parent, name, type=0, timeout=10, retry_interval=1):
    if type == 0:
        parent[name].wait('visible', timeout=timeout, retry_interval=retry_interval);
    else:
        parent[name].wait_not('visible', timeout=timeout, retry_interval=retry_interval);

@retry_function(retry_times, delay)
def getApp(window_title, executable=r'D:\JianyingPro\JianyingPro.exe', backend="uia", timeout=5):
    # 尝试连接到已经打开的应用程序
    try:
        app = Application(backend=backend).connect(title=window_title, timeout=timeout)
        print("应用程序已经打开并连接成功。")
    except Exception as e:
        print("无法连接到应用程序，可能是因为它没有打开或者窗口标题不正确。尝试启动应用程序...")
        try:
            # 启动应用程序
            os.system(f"start {executable}");
            time.sleep(5);
            app = Application(backend=backend).connect(title=window_title, timeout=timeout)
            print("应用程序已成功启动。")
        except Exception as e:
            print("无法启动应用程序。", e)
    finally:
        return app;