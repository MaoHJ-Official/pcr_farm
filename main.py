import os
import time
import cv2
import _thread


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

        # 会长与公会的28名成员
        # 必须与.txt文件内容匹配，否则报错
        self.president = Member()
        self.memberLst = [Member() for i in range(28)]

    def getPresident(self):
        return self.president

    def getMember(self, i):
        return self.memberLst[i]

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
        print(x, y)
        cmd = 'adb -s ' + name + ' shell input tap %s %s' % (x, y)
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
        cmd = 'adb -s ' + name + ' shell input swipe %s %s %s %s %s' % (x1, y1, x2, y2, duration)
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
        print(s)
        cmd = 'adb -s ' + name + ' shell input text %s' % s
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
            # os.system(cmd0)
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

    def image2position(self, name, imagepath, m=0):
        Farm.m_screencap(self, name)
        templatetimg = cv2.imread(imagepath, 0)  # 模板图像
        # if (templatetimg.empty()):
        #     print('open template image fail!')
        #     exit(1)
        screenshot = cv2.imread(os.path.abspath('.') + '\\' + name + 'screenshot.png', 0)  # 屏幕截图
        # if (screenshot.empty()):
        #     print('open screenshot fail!')
        #     exit(1)

        methods = [cv2.TM_CCOEFF_NORMED, cv2.TM_SQDIFF_NORMED, cv2.TM_CCORR_NORMED]
        image_x, image_y = templatetimg.shape[:2]
        result = cv2.matchTemplate(screenshot, templatetimg, methods[m])
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        print(imagepath, max_val)
        if max_val > 0.7:
            center = (max_loc[0] + image_y / 2, max_loc[1] + image_x / 2)
            print(center[0], center[1])
            return center
        else:
            return False

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

    def distinguish(self, name, ipath, templatename):
        cen = False
        ts = 0
        while (not cen):
            ts += 1
            if (ts == 30):
                print(name + ' fail distinguish :' + templatename)
                break
            cen = Farm.image2position(self, name, ipath)
        return cen

    def memberhavior(self, name, member):
        if name == '':
            print('emulator name error')
            exit(1)
        cen = False
        ipath = ''
        # zhucaidan.png
        ipath = os.path.abspath('.') + '\m_script\images\m1zhucaidan.png'
        cen = Farm.distinguish(self, name, ipath, '主菜单')
        if (not cen): exit(1)
        Farm.m_tap(self, 600, 400, name)

        print('---------------------------%s 开始识别 -切换账号- ' % time.process_time())
        # qiehuanzhanghao.png
        ipath = os.path.abspath('.') + '\m_script\images\m2qiehuanzhanghao.png'
        cen = Farm.distinguish(self, name, ipath, '切换账号')
        print('---------------------------%s 结束识别 -切换账号- ' % time.process_time())
        if (not cen): exit(1)
        Farm.m_tap(self, cen[0], cen[1], name)

        # bilibilidenglu.png
        ipath = os.path.abspath('.') + '\m_script\images\m3bilibilidenglu.png'
        cen = Farm.distinguish(self, name, ipath, 'bilibili登录')
        if (not cen): exit(1)
        Farm.m_tap(self, 600, 260, name)
        Farm.m_text(self, member.account, name)
        Farm.m_tap(self, 600, 330, name)
        Farm.m_text(self, member.password, name)
        # denglu.png
        ipath = os.path.abspath('.') + '\m_script\images\m4denglu.png'
        cen = Farm.distinguish(self, name, ipath, '登录')
        if (not cen): exit(1)
        Farm.m_tap(self, cen[0], cen[1], name)


if __name__ == '__main__':
    farm1 = Farm()
    farm1.getSerialNo()
    farm1.startGame()
    farm1.setAccount(os.path.abspath('.') + '\m_script\guild1.txt')
    farm1.printAccount()

    farm1.memberhavior(farm1.nameList[0], farm1.getMember(1))
