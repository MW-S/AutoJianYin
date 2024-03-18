# startWindows.py

import tkinter as tk


def startInput(func) :
    # 创建主窗口
    root = tk.Tk()
    root.title("多行输入框")
    # 创建Text控件，设置高度和宽度
    text_box = tk.Text(root, height=50, width=200)
    text_box.pack()

    # 定义一个函数来获取输入的文本并关闭窗口
    def on_submit():
        user_input = text_box.get("1.0", tk.END)  # 获取Text控件中的所有文本
        root.destroy()  # 关闭窗口
        print(user_input);
        func(user_input);

    # 创建一个按钮，点击时会调用on_submit函数
    submit_button = tk.Button(root, text="提交", command=on_submit)
    submit_button.pack()
    # 启动事件循环
    root.mainloop()

    #return user_input;

