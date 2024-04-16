import os
import fnmatch
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from adbtool import *
from tkinter.scrolledtext import ScrolledText


class APKSelector:
    def __init__(self, root):
        self.root = root
        self.root.title('APK 文件选择器')
        self.root.geometry('500x300')  # 设置窗口大小

        # 创建一个下拉列表
        self.combobox = ttk.Combobox(root, width=100, state="readonly")
        self.combobox.pack(padx=10, pady=10)

        # 创建按钮
        self.create_buttons()

        # 更新下拉列表中的条目
        self.update_combobox()

        # 创建输出面板
        self.create_output_panel()

        self.adb_devices()

    def adb_devices(self):
        try:
            result = subprocess.run(['adb', 'devices'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if 'device' in result.stdout:
                devices = result.stdout.splitlines()
                connected_devices = [device for device in devices[1:] if device.strip()]
                if connected_devices:
                    print('成功连接到设备：')
                    for device in connected_devices:
                        print(device)
                    return True
                else:
                    print('没有检测到连接的设备。')
            else:
                print(f'错误：{result.stderr}')
        except Exception as e:
            print(f'执行ADB命令时出现异常：{e}')
        return False

    def create_buttons(self):
        # 创建“刷新”按钮
        button_refresh = ttk.Button(root, text="刷新", command=self.update_combobox)
        button_refresh.pack(padx=10, pady=10)

        # 创建“安装”按钮
        button_install = ttk.Button(root, text="安装", command=self.install_apk)
        button_install.pack(padx=10, pady=10)

    def find_apks(self, directory_path):
        apk_files = []
        if os.path.exists(directory_path):
            for root, dirs, files in os.walk(directory_path):
                for filename in fnmatch.filter(files, '*.apk'):
                    apk_files.append(os.path.join(root, filename))
        return apk_files

    def create_output_panel(self):
        # 创建一个滚动文本框用于显示输出内容
        self.output_text = ScrolledText(root, height=10, width=50)
        self.output_text.pack(padx=10, pady=10)

    def update_combobox(self):
        apk_files = self.find_apks(directory_path)
        self.combobox['values'] = apk_files
        self.combobox.set(apk_files[0] if apk_files else '')
        if not apk_files:
            messagebox.showinfo("信息", "指定目录中未找到 .apk 文件。")

    def install_apk(self):
        selected_apk = self.combobox.get()
        self.output_text.insert(tk.END, "开始装包\n")
        # install_apks(selected_apk)
        if selected_apk:
            # 添加安装选定 APK 的代码
            messagebox.showinfo("信息", f"正在安装 {selected_apk}")
        else:
            messagebox.showinfo("信息", "请选择一个 APK 文件。")


if __name__ == '__main__':
    directory_path = "D:/xiangm"
    root = tk.Tk()
    apk_selector = APKSelector(root)
    apk_selector.adb_devices()

    # root.mainloop()


