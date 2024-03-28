import os
import fnmatch
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

directory_path = "D:/xiangm"


# 查找文件夹中所有的 .apk 文件
def find_apks(directory_path):
    apk_files = []
    # 判断是否存在文件路径
    if os.path.exists(directory_path):
        # 遍历 directory_path 指定的目录及其所有子目录，产生三个值：当前文件夹路径（root），当前文件夹下的子目录列表（dirs），以及当前文件夹下所有文件的列表（files）
        for root, dirs, files in os.walk(directory_path):
            # 用 fnmatch.filter 函数筛选出所有以 .apk 结尾的文件
            for filename in fnmatch.filter(files, '*.apk'):
                apk_files.append(os.path.join(root, filename))
    else:
        messagebox.showerror("Error", "The specified directory does not exist.")
    return apk_files


# 更新下拉列表中的条目
def update_combobox(directory_path):
    apk_files = find_apks(directory_path)
    combobox['values'] = apk_files
    if apk_files:
        combobox.current(0)
    else:
        combobox.set('')
        messagebox.showinfo("Info", "No .apk files found in the specified directory.")


# 当用户点击显示 APK 文件按钮时的操作
def on_submit():
    update_combobox(directory_path)

def on_submit2():
    return


if __name__ == '__main__':
    # 创建主窗口
    root = tk.Tk()
    root.title('APK Files Selector')
    root.geometry('500x300')  # 这里的乘是小x

    # 创建一个下拉列表
    combobox = ttk.Combobox(root, width=100, state="readonly")
    combobox.pack(padx=10, pady=10)

    # 创建一个按钮，用户点击后显示 .apk 文件
    button_submit = ttk.Button(root, text="刷新", command=on_submit)
    button_submit2 = ttk.Button(root, text="安装", command=on_submit2)
    button_submit.pack(padx=10, pady=10)
    button_submit2.pack(padx=10, pady=10)
    update_combobox(directory_path)
    # 运行主事件循环
    root.mainloop()
