# initUI.py
import sys,  re
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QMessageBox
from UI.start import Ui_Form
from UI.common import Ui_Dialog as CommonDialog
from UI.down import Ui_Dialog as DownDialog
from downContent2Word import toWeb
from correctDocFormat import contentFormat
from srcFileRewrite import srcFormat
from textSplit import chatgptReWriter
from autoJianYin import readWordRun
# 定义槽函数来打开文件夹选择对话框
def choose_folder(obj):
    # 打开文件夹对话框
    folder_name = QFileDialog.getExistingDirectory(None, "QFileDialog.getExistingDirectory()", "",
                                                   QFileDialog.ShowDirsOnly)

    # 处理选择的文件夹
    if folder_name:
        obj.setText(folder_name)


# 定义槽函数来打开文件选择对话框
def choose_file(obj):
    # 打开文件对话框
    options = QFileDialog.Options()
    file_name, _ = QFileDialog.getOpenFileName(None, "QFileDialog.getOpenFileName()", "",
                                               "All Files (*);;Text Files (*.txt)", options=options)

    # 处理选择的文件
    if file_name:
        obj.setText(file_name)

def is_url(s):
    # 正则表达式匹配网址
    pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\$\$,]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    return bool(pattern.match(s))
def is_empty(s):
    return not bool(s.strip())

def show_notification_dialog(title):
    # 创建并显示通知弹窗
    msg_box = QMessageBox()
    msg_box.setWindowTitle('通知')
    msg_box.setText(title)
    msg_box.setIcon(QMessageBox.Information)
    msg_box.setStandardButtons(QMessageBox.Ok)  # 只显示确定按钮
    msg_box.exec_()


# 校验参数
def validForm(type, _dia):
    text1 = _dia.lineEdit.text();
    text2 = _dia.lineEdit_2.text();
    if type == 2:  # 下载素材
        res = not is_empty(text1) and not is_empty(text2);
        if res:
            res = is_url(text1)
    elif type == 3:  # 剪映-生成字幕与配音
        res = True;
    elif type == 4:  # Chatgpt重写文案
        res = True;
    elif type == 5:  # 字幕格式纠正
        res = True;
    elif type == 6:  # Word文档格式修复
        res = True;
    return res;


def confirm(type, _dia):
    # 校验参数是否正确
    if(not validForm(type, _dia)):
        show_notification_dialog("参数异常！");
        return;
    # 校验完成后进行逻辑处理
    if type == 2:  # 下载素材
        toWeb(_dia.lineEdit.text(), _dia.lineEdit_2.text());
        return;
    elif type == 3:  # 剪映-生成字幕与配音
        readWordRun(_dia.lineEdit.text());
        return;
    elif type == 4:  # Chatgpt重写文案
        chatgptReWriter(_dia.lineEdit.text(), _dia.lineEdit_2.text());
        return;
    elif type == 5:  # 字幕格式纠正
        srcFormat(_dia.lineEdit.text(), _dia.lineEdit_2.text());
        return;
    elif type == 6:  # Word文档格式修复
        contentFormat(_dia.lineEdit.text(), _dia.lineEdit_2.text());
        return;


def showDialog(dialog, title, type):
    u = None;
    if (type == 2):
        u = DownDialog();
        u.setupUi(dialog, title);
        u.buttonBox.accepted.connect(lambda: confirm(type, u));
        u.toolButton_3.clicked.connect(lambda: choose_folder(u.lineEdit_2))
    else:
        u = CommonDialog();
        u.setupUi(dialog, title);
        u.buttonBox.accepted.connect(lambda: confirm(type, u));
        u.toolButton.clicked.connect(lambda: choose_file(u.lineEdit))
        u.toolButton_2.clicked.connect(lambda: choose_folder(u.lineEdit_2))
        if type == 3:
            u.lineEdit_2.setEnabled(False);
            u.toolButton_2.setEnabled(False);
        else:
            u.lineEdit_2.setEnabled(True);
            u.toolButton_2.setEnabled(True);
    # 连接对话框的关闭事件到槽函数
    dialog.setModal(True);
    dialog.show();


def run():
    # 创建应用程序实例
    app = QApplication(sys.argv)
    # 创建窗口实例
    window = QWidget()
    dialog2 = QtWidgets.QDialog();
    dialog3 = QtWidgets.QDialog();
    dialog4 = QtWidgets.QDialog();
    dialog5 = QtWidgets.QDialog();
    dialog6 = QtWidgets.QDialog();
    # 设置窗口的UI，这通常是从.ui文件生成的Ui_MainWindow类的实例
    ui = Ui_Form()
    ui.setupUi(window)
    ui.btnDown.clicked.connect(lambda: showDialog(dialog2, ui.btnDown.text(), 2));
    ui.btnGenerateSrc.clicked.connect(lambda: showDialog(dialog3, ui.btnGenerateSrc.text(), 3));
    ui.btnReWriter.clicked.connect(lambda: showDialog(dialog4, ui.btnReWriter.text(), 4));
    ui.btnSrcCorrect.clicked.connect(lambda: showDialog(dialog5, ui.btnSrcCorrect.text(), 5));
    ui.btnWordCorrect.clicked.connect(lambda: showDialog(dialog6, ui.btnWordCorrect.text(), 6));

    # 显示窗口
    window.show()

    # 运行应用程序的事件循环
    sys.exit(app.exec_())


