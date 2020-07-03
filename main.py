import os
import time


# import cv2


class Member:
    def __init__(self, a='', p=''):
        self.account = a
        self.password = p


class Farm:
    def __init__(self):
        # 同时开4个模拟器
        # 必须与实际情况匹配，否则报错
        self.nameList = ['' for i in range(4)]

        # 打开应用，用
        # adb -s <serial number> shell dumpsys window windows | findstr “Current”
        # 找到返回的结果，通常为“package/activity”的格式
        self.pcrActivityName = 'com.bilibili.priconne/com.bilibili.princonne.bili.MainActivity'

        # 会长与公会的20名成员
        # 必须与.txt文件内容匹配，否则报错
        self.president = Member()
        self.memberLst = [Member() for i in range(20)]

    def m_connect(self, name):
        """
        连接模拟器
        :param name:模拟器的serialNo
        :return:NULL
        """
        cmd = 'adb connect %s' % name
        try:
            os.system(cmd)
        except:
            print('connect %s fail' % name)
            exit(1)

    def m_tap(self, x, y, name):
        """
        屏幕点击
        :param x:x坐标
        :param y:y坐标
        :param name:模拟器的serialNo
        :return:
        """
        print(name)
        print(x, y)
        cmd = 'adb -s' + name + 'shell input tap %s %s' % (x, y)
        try:
            os.system(cmd)
        except:
            print('click fail' + name)
            exit(1)
        print(cmd)

    def m_swipe(self, x1, y1, x2, y2, duration, name):
        """
        屏幕滑动
        :param x1:起始x坐标
        :param y1:起始y坐标
        :param x2:终止x坐标
        :param y2:终止y坐标
        :param duration:持续时间
        :param name:模拟器的serialNo
        :return:
        """
        print(x1, y1, x2, y2)
        cmd = 'adb -s' + name + 'shell input swipe %s %s %s %s %s' % (x1, y1, x2, y2, duration)
        try:
            os.system(cmd)
        except:
            print('swipe fail' + name)
            exit(1)
        print(cmd)

    def m_text(self, s, name):
        """
        屏幕输入
        :param s:输入文本内容
        :param name:模拟器的serialNo
        :return:
        """
        cmd = 'adb -s' + name + 'shell input text %s' % s
        try:
            os.system(cmd)
        except:
            print('text fail' + name)
            exit(1)
        print(cmd)

    def m_screencap(self, name):
        """
        屏幕截屏
        :param name:模拟器的serialNo
        :return:
        """
        path = os.path.abspath('.') + '\\' + name + 'screenshot.png'
        print(path)
        try:
            os.system('adb -s ' + name + ' shell screencap /data/' + name + 'screen.png')
        except:
            print('%s screencap fail' % name)
            exit(1)

        try:
            os.system('adb -s ' + name + ' pull /data/' + name + 'screen.png %s' % path)
        except:
            print('%s pull screencap fail' % name)
            exit(1)

    def getSerialNo(self):
        """
        获取模拟器的serialNo
        :return:
        """
        cmd0 = 'adb kill-server'
        cmd = 'adb devices'
        try:
            os.system(cmd0)
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
                self.nameList[i] = name[0]
                i += 1

    def startGame(self):
        """
        启动所有模拟器内的应用
        :return:
        """
        for emulatorName in self.nameList:
            cmd = 'adb -s %s shell am start -n %s' % (emulatorName, self.pcrActivityName)
            try:
                os.system(cmd)
            except:
                print('%s start game fail' % emulatorName)
                exit(1)

    def getScreenshot(self):
        """
        同时截取4个模拟器的屏幕
        可能用不上
        :return:
        """
        for emulatorName in self.nameList:
            Farm.m_screencap(self, emulatorName)

    def image2position(self, image, name):
        Farm.m_screencap(self, name)

    def setAccount(self, text):
        """
        从.txt文件中获取会长与成员的账号密码
        :param text:存储了公会所有账号密码的.txt文件
        :return:
        """
        f = open(text, 'r')
        if (not f):
            print('guild file open fail')
            exit(1)

        president = f.readline()
        presidentAccount = president.split()
        self.president.account = presidentAccount[0]
        self.president.password = presidentAccount[1]
        i = 0
        for line in f.readlines():
            memberAccount = line.split()
            self.memberLst[i].account = memberAccount[0]
            self.memberLst[i].password = memberAccount[1]
            i += 1

    def printAccount(self):
        """
        账号信息打印
        :return:
        """
        print('%s %s' % (self.president.account, self.president.password))
        for m in self.memberLst:
            print('%s %s' % (m.account, m.password))


if __name__ == '__main__':
    farm1 = Farm()
    farm1.getSerialNo()
    farm1.startGame()
    farm1.setAccount(os.path.abspath('.') + '\m_script\guild1.txt')
    farm1.printAccount()

    time.sleep(20)

    farm1.getScreenshot()
