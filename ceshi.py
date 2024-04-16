import subprocess


def adb_devices():
    try:
        result = subprocess.run(['adb', 'devices'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print("result:", result)
        print("result.stdout:", result.stdout)
        if 'device' in result.stdout:

            devices = result.stdout.splitlines()
            print("devices:", devices)
            connected_devices = [device for device in devices[1:] if device.strip()]
            print("connected_devices:", connected_devices)
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


def shuchu():
    if adb_devices():
        print(111)
    else:
        print(222)


if __name__ == '__main__':
    shuchu()
