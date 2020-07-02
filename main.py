import os


def m_tap(x, y, name):
    print(name)
    print(x, y)
    cmd = 'adb -s' + name + 'shell input tap %s %s' % (x, y)
    try:
        os.system(cmd)
    except:
        print('click fail' + name)
        exit(1)
    print(cmd)


def m_swipe(x1, y1, x2, y2, duration, name):
    print(x1, y1, x2, y2)
    cmd = 'adb -s' + name + 'shell input swipe %s %s %s %s %s' % (x1, y1, x2, y2, duration)
    try:
        os.system(cmd)
    except:
        print('swipe fail' + name)
        exit(1)
    print(cmd)


def m_text(s, name):
    cmd = 'adb -s' + name + 'shell input text %s' % s
    try:
        os.system(cmd)
    except:
        print('text fail' + name)
        exit(1)
    print(cmd)


def getSerialNo():
    cmd = 'adb devices'
    try:
        os.system(cmd)
    except:
        print('get serial number fail')
        exit(1)
    r = os.popen(cmd)
    r.readline()
    i = 0
    for line in r.readlines():
        name = line.split()
        if (len(name) > 0):
            nameList[i] = name[0]
            i += 1


def m_connect(name):
    cmd = 'adb connect %s' % name
    try:
        os.system(cmd)
    except:
        print('connect %s fail' % name)
        exit(1)


def startGame(name):
    cmd = 'adb -s %s shell am start -n %s' % (name, pcrActivityName)
    try:
        os.system(cmd)
    except:
        print('%s start game fail' % name)
        exit(1)


if __name__ == '__main__':
    nameList = [0, 0, 0, 0]  # 同时开4个
    pcrActivityName = 'com.bilibili.priconne/com.bilibili.princonne.bili.MainActivity'
    # 打开应用，用
    # adb -s <serial number> shell dumpsys window windows | findstr “Current”
    # 找到返回的结果，通常为“package/activity”的格式
    getSerialNo()
    print(nameList)
    for emulatorName in nameList:
        startGame(emulatorName)
