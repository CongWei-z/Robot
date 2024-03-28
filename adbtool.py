import subprocess
import os
import signal
import tkinter as tk
import fnmatch
import time
from Opencv_Gui import installation
from time import sleep


def GuiAdbTool():
    # 第1步，实例化object，建立窗口window
    window = tk.Tk()
    # 第2步，给窗口的可视化起名字
    window.title('ADBTool')
    # 第3步，设定窗口的大小(长 * 宽)
    window.geometry('500x300')  # 这里的乘是小x
    # 第4步，在图形界面上设定标签
    var = tk.StringVar()  # 将label标签的内容设置为字符类型，用var来接收hit_me函数的传出内容用以显示在标签上
    l = tk.Label(window, textvariable=var, bg='green', fg='white', font=('Arial', 12), width=30, height=2)
    # 说明： bg为背景，fg为字体颜色，font为字体，width为长，height为高，这里的长和高是字符的长和高，比如height=2,就是标签有2个字符这么高
    l.pack()
    # 显示窗口
    window.mainloop()


def find_apks(directory_path):
    for root, dirs, files in os.walk(directory_path):
        for filename in fnmatch.filter(files, '*.apk'):
            print(os.path.join(root, filename))


# 使用当前工作目录，你可以修改这个路径指向任何需要搜索的目录
start_path = '.'  # 或者直接填写路径，例如 'C:/'
find_apks(start_path)


# 检查ADB设备连接
def check_adb_devices():
    try:
        result = subprocess.run(['adb', 'devices'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print("看一下里面是什么", result)
        print(result.stdout)
        if 'device' in result.stdout:
            devices = result.stdout.splitlines()
            if len(devices) == 3:
                print('成功连接到设备：')
                for device in devices[1:]:
                    if device.strip():
                        print(device)
                return True
            else:
                print('没有检测到连接的设备。')
        else:
            print(f'错误：{result.stderr}')
    except Exception as e:
        print(f'执行ADB命令时出现异常：{e}')
    return False


# 开始录制视频
def start_screen_record():
    # 设定保存至电脑桌面的视频文件路径
    desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    video_path = os.path.join(desktop_path, 'screen_record.mp4')

    # 删除旧的录像文件
    if os.path.exists(video_path):
        os.remove(video_path)

    # 开始录像
    screen_record_command = ['adb', 'shell', 'screenrecord', '/sdcard/screen_record.mp4']
    screen_record_process = subprocess.Popen(screen_record_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return screen_record_process, video_path


# 停止录制视频并保存至桌面
def stop_screen_record(process, video_path):
    # 发送信号Ctrl+C到adb命令行, 停止录像
    process.send_signal(signal.CTRL_C_EVENT)
    process.wait()

    # 将视频从手机复制到桌面
    subprocess.run(['adb', 'pull', '/sdcard/screen_record.mp4', video_path], stdout=subprocess.PIPE,
                   stderr=subprocess.PIPE)
    subprocess.run(['adb', 'shell', 'rm', '/sdcard/screen_record.mp4'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f'视频已保存至桌面: {video_path}')


def install_apk(apk_path):
    if check_adb_devices() == True:
        try:
            # "adb install" 命令用于安装APK
            cmd = ['adb', 'install', apk_path]
            # 启动子进程来执行命令
            with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1,
                                  universal_newlines=True) as proc:
                print("Starting APK installation...")
                # 显示一个简单的文本进度条
                progress_signs = ['|', '/', '-', '\\']
                progress_idx = 0
                while proc.poll() is None:  # 如果进程仍在运行
                    print(f'\rInstalling APK {progress_signs[progress_idx % len(progress_signs)]}', end='')
                    time.sleep(0.25)  # 刷新进度符号的速率
                    progress_idx += 1
                # 读取最终的输出结果
                output = proc.stdout.read()
                print('\n' + output.strip())
                # 检查命令的执行结果
                if proc.returncode == 0:
                    print("APK installed successfully.")
                else:
                    print("Failed to install APK.")
        except FileNotFoundError:
            print("ADB not found, ensure it's installed and in your PATH.")
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    # 将 'path_to_apk' 替换成你的APK文件的实际路径
    install_apk('D:/xiangm/740263_release-Android-Shipping_universal.apk')
    # GuiAdbTool()
    # start_path = 'D:/xiangm'  # 或者直接填写路径，例如 'C:/'
    # find_apks(start_path)
    # if check_adb_devices():
    #     print('开始录制视频，按Ctrl+C结束...')
    #     screen_record_process, video_path = start_screen_record()
    #     try:
    #         # 这里可以放入任何需要在录屏期间运行的代码
    #         sleep(10)  # 示例: 录制10秒
    #     except KeyboardInterrupt:
    #         pass
    #     finally:
    #         stop_screen_record(screen_record_process, video_path)
    #         print('录制结束')
