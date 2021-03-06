import os
import time
import cv2
import threading


class Member:
    def __init__(self, a='', p=''):
        self.account = a
        self.password = p


class Farm:
    def __init__(self):
        # 同时开2个模拟器
        # 必须与实际情况匹配，否则报错
        # self.nameList = ['' for i in range(2)]
        self.nameList = ["emulator-5558", "emulator-5560"]

        self.member_result = ['' for i in range(29)]

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
            print('---------------------------connect %s fail' % name)
            exit(1)

    def m_tap(self, x, y, name):
        """
        屏幕点击
        :param x:x坐标
        :param y:y坐标
        :param name:模拟器的serialNo
        :return:
        """
        cmd = 'adb -s ' + name + ' shell input tap %s %s' % (x, y)
        try:
            os.system(cmd)
            print('---------------------------' + time.strftime("%Y-%m-%d %H:%M:%S",
                                                                time.localtime()) + ' %s 点击 %s %s ' % (name, x, y))
        except:
            print('---------------------------click fail' + name)
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
        cmd = 'adb -s ' + name + ' shell input swipe %s %s %s %s %s' % (x1, y1, x2, y2, duration)
        try:
            os.system(cmd)
            print('---------------------------' + time.strftime("%Y-%m-%d %H:%M:%S",
                                                                time.localtime()) + ' %s 滑动 %s %s %s %s ' % (
                      name, x1, y1, x2, y2))
        except:
            print('---------------------------swipe fail' + name)
            exit(1)
        print(cmd)

    def m_text(self, s, name):
        """
        屏幕输入
        :param s:输入文本内容
        :param name:模拟器的serialNo
        :return:
        """
        cmd = 'adb -s ' + name + ' shell input text %s' % s
        try:
            os.system(cmd)
            print(
                '---------------------------' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' %s 输入 %s ' % (
                    name, s))
        except:
            print('---------------------------text fail' + name)
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
            print('---------------------------%s screencap fail' % name)
            exit(1)

        try:
            os.system('adb -s ' + name + ' pull /data/' + name + 'screen.png %s' % path)
        except:
            print('---------------------------%s pull screencap fail' % name)
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
            print('---------------------------get serial number fail')
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
                print('---------------------------%s start game fail' % emulatorName)
                exit(1)

    def endGame(self):
        """
        关闭所有模拟器内的应用
        :return:
        """
        for emulatorName in self.nameList:
            cmd = 'adb -s %s shell am force-stop com.bilibili.priconne' % emulatorName
            try:
                os.system(cmd)
            except:
                print('---------------------------%s end game fail' % emulatorName)
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
            print('---------------------------guild file open fail')
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

    def writeMemberResult(self, text):
        f = open(text, 'w')
        if not f:
            print('---------------------------member result file open fail')
            exit(1)
        for index in self.member_result:
            f.write(index + '\n')

    def recognize(self, name, ipath, t, templatename='模板图像'):
        """
        识别函数
        :param name: 模拟器serialNo
        :param ipath: 模板图像路径
        :param t: 循环次数
        :param templatename: 模板图像名称，用于输出
        :return: cen
        """
        print('---------------------------' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' %s 开始识别 %s %s次' % (
            name, templatename, t))
        cen = False
        ts = 0
        while (not cen):
            print('---------------------------' + time.strftime("%Y-%m-%d %H:%M:%S",
                                                                time.localtime()) + ' %s 循环识别 %s %s/%s' % (
                      name, templatename, ts + 1, t))
            ts += 1
            if (ts == t):
                print('---------------------------' + name + ' fail recognize :' + templatename)
                break
            cen = Farm.image2position(self, name, ipath)
        print('---------------------------' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' %s 识别结束 %s ' % (
            name, templatename))
        return cen

    def memberhavior(self, emulator_no, member_no, mem):
        emulator_name = self.nameList[emulator_no]
        if emulator_name == '':
            print('---------------------------emulator name error')
            exit(1)

        member = Member()
        if member_no == 28:
            member = self.getPresident()
        else:
            member = self.getMember(member_no)

        cen = False
        ipath = ''
        # zhucaidan.png
        ipath = os.path.abspath('.') + '\m_script\images\m1zhucaidan.png'
        cen = Farm.recognize(self, emulator_name, ipath, 120, '主菜单' + mem)
        if not cen:
            self.member_result[member_no] = '%s 无法识别 主菜单' % member_no
            exit(1)
        Farm.m_tap(self, 600, 400, emulator_name)

        # qiehuanzhanghao.png
        # ipath = os.path.abspath('.') + '\m_script\images\m2qiehuanzhanghao.png'
        # cen = Farm.distinguish(self, name, ipath, '切换账号' + mem)
        # if (not cen): exit(1)
        # Farm.m_tap(self, cen[0], cen[1], name)
        for i in range(16):
            Farm.m_tap(self, 1209.5, 50, emulator_name)  # 特例，识别速度不够快

        # bilibiliyouxi.png
        ipath = os.path.abspath('.') + '\m_script\images\m3bilibiliyouxi.png'
        cen = Farm.recognize(self, emulator_name, ipath, 15, 'bilibili游戏' + mem)
        if not cen:
            self.member_result[member_no] = '%s 无法识别 bilibili游戏' % member_no
            exit(1)
        Farm.m_tap(self, 600, 245, emulator_name)
        time.sleep(0.5)
        Farm.m_text(self, member.account, emulator_name)
        time.sleep(0.5)
        Farm.m_tap(self, 600, 325, emulator_name)
        time.sleep(0.5)
        Farm.m_text(self, member.password, emulator_name)

        # denglu.png
        ipath = os.path.abspath('.') + '\m_script\images\m4denglu.png'
        cen = Farm.recognize(self, emulator_name, ipath, 15, '登录' + mem)
        if not cen:
            self.member_result[member_no] = '%s 无法识别 登录' % member_no
            exit(1)
        Farm.m_tap(self, cen[0], cen[1], emulator_name)

        # m5tiaoguo.png
        ipath = os.path.abspath('.') + '\m_script\images\m5tiaoguo.png'
        cen = Farm.recognize(self, emulator_name, ipath, 15, '跳过' + mem)
        if cen:
            Farm.m_tap(self, cen[0], cen[1], emulator_name)

        """
        # 兰德索尔杯特制版
        # m53.png
        ipath = os.path.abspath('.') + '\m_script\images\m53.png'
        cen = Farm.recognize(self, name, ipath, 15, '3' +  mem)
        if not cen: exit(1)
        Farm.m_tap(self, cen[0], cen[1], name)

        # m5jingsaikaishi.png
        ipath = os.path.abspath('.') + '\m_script\images\m5jingsaikaishi.png'
        cen = Farm.recognize(self, name, ipath, 15, '竞赛开始' +  mem)
        if not cen: exit(1)
        Farm.m_tap(self, cen[0], cen[1], name)

        # m5end.png
        ipath = os.path.abspath('.') + '\m_script\images\m5end.png'
        cen = Farm.recognize(self, name, ipath, 60, '赛马结束' +  mem)
        if not cen: exit(1)
        Farm.m_tap(self, cen[0], cen[1], name)
        # 兰德索尔杯特制版
        """

        time.sleep(8)
        Farm.m_tap(self, 600, 400, emulator_name)

        time.sleep(2)
        Farm.m_tap(self, 600, 400, emulator_name)

        # m6tongzhi.png
        ipath = os.path.abspath('.') + '\m_script\images\m6tongzhi.png'
        cen = Farm.recognize(self, emulator_name, ipath, 15, '通知' + mem)
        if not cen:
            self.member_result[member_no] = '%s 无法识别 通知' % member_no
            exit(1)
        # m7guanbi.png
        ipath = os.path.abspath('.') + '\m_script\images\m7guanbi.png'
        cen = Farm.recognize(self, emulator_name, ipath, 15, '关闭' + mem)
        if not cen:
            self.member_result[member_no] = '%s 无法识别 关闭（通知）' % member_no
            exit(1)
        Farm.m_tap(self, cen[0], cen[1], emulator_name)

        # m8maoxian.png
        ipath = os.path.abspath('.') + '\m_script\images\m8maoxian.png'
        cen = Farm.recognize(self, emulator_name, ipath, 15, '冒险' + mem)
        if not cen:
            self.member_result[member_no] = '%s 无法识别 冒险' % member_no
            exit(1)
        Farm.m_tap(self, cen[0], cen[1], emulator_name)

        # m9dixiacheng.png
        ipath = os.path.abspath('.') + '\m_script\images\m9dixiacheng.png'
        cen = Farm.recognize(self, emulator_name, ipath, 15, '地下城' + mem)
        if not cen:
            self.member_result[member_no] = '%s 无法识别 地下城' % member_no
            exit(1)
        Farm.m_tap(self, cen[0], cen[1], emulator_name)

        # m91putong.png
        ipath = os.path.abspath('.') + '\m_script\images\m91putong.png'
        cen = Farm.recognize(self, emulator_name, ipath, 15, '普通' + mem)
        if not cen:
            self.member_result[member_no] = '%s 无法识别 普通' % member_no
            exit(1)
        Farm.m_tap(self, cen[0], cen[1], emulator_name)
        # above done

        # m92OK.png
        ipath = os.path.abspath('.') + '\m_script\images\m92OK.png'
        cen = Farm.recognize(self, emulator_name, ipath, 15, 'OK' + mem)
        if not cen:
            self.member_result[member_no] = '%s 无法识别 OK（普通）' % member_no
            exit(1)
        Farm.m_tap(self, cen[0], cen[1], emulator_name)

        # m93yiceng.png
        ipath = os.path.abspath('.') + '\m_script\images\m93yiceng.png'
        cen = Farm.recognize(self, emulator_name, ipath, 15, '1层' + mem)
        if not cen:
            self.member_result[member_no] = '%s 无法识别 1层' % member_no
            exit(1)
        Farm.m_tap(self, cen[0], cen[1], emulator_name)

        # m93tiaozhan.png
        ipath = os.path.abspath('.') + '\m_script\images\m93tiaozhan.png'
        cen = Farm.recognize(self, emulator_name, ipath, 15, '挑战' + mem)
        if not cen:
            self.member_result[member_no] = '%s 无法识别 挑战' % member_no
            exit(1)
        Farm.m_tap(self, cen[0], cen[1], emulator_name)

        # m94zhiyuan.png
        ipath = os.path.abspath('.') + '\m_script\images\m94zhiyuan.png'
        cen = Farm.recognize(self, emulator_name, ipath, 15, '支援' + mem)
        if not cen:
            self.member_result[member_no] = '%s 无法识别 支援' % member_no
            exit(1)
        Farm.m_tap(self, cen[0], cen[1], emulator_name)

        # m95yly.png
        ipath = os.path.abspath('.') + '\m_script\images\m95yly.png'
        cen = Farm.recognize(self, emulator_name, ipath, 15, '伊莉雅' + mem)
        if not cen:
            self.member_result[member_no] = '%s 无法识别 伊莉雅' % member_no
            exit(1)
        Farm.m_tap(self, cen[0], cen[1], emulator_name)

        # m96zhandoukaishi.png
        ipath = os.path.abspath('.') + '\m_script\images\m96zhandoukaishi.png'
        cen = Farm.recognize(self, emulator_name, ipath, 15, '战斗开始' + mem)
        if not cen:
            self.member_result[member_no] = '%s 无法识别 战斗开始' % member_no
            exit(1)
        Farm.m_tap(self, cen[0], cen[1], emulator_name)

        # m97OK.png
        ipath = os.path.abspath('.') + '\m_script\images\m97OK.png'
        cen = Farm.recognize(self, emulator_name, ipath, 15, 'OK' + mem)
        if not cen:
            self.member_result[member_no] = '%s 无法识别 OK（战斗开始）' % member_no
            exit(1)
        Farm.m_tap(self, cen[0], cen[1], emulator_name)

        # m98qianwangdixiacheng.png
        ipath = os.path.abspath('.') + '\m_script\images\m98qianwangdixiacheng.png'
        cen_fail = Farm.recognize(self, emulator_name, ipath, 15, '前往地下城' + mem)

        # m98xiayibu.png
        ipath = os.path.abspath('.') + '\m_script\images\m98xiayibu.png'
        cen_success = Farm.recognize(self, emulator_name, ipath, 15, '下一步' + mem)

        if cen_fail:
            Farm.m_tap(self, cen_fail[0], cen_fail[1], emulator_name)
        if cen_success:
            Farm.m_tap(self, cen_success[0], cen_success[1], emulator_name)
            # m98OK.png
            ipath = os.path.abspath('.') + '\m_script\images\m98OK.png'
            cen = Farm.recognize(self, emulator_name, ipath, 15, 'OK' + mem)
            if not cen:
                self.member_result[member_no] = '%s 无法识别 OK（前往地下城/下一步）' % member_no
                exit(1)
            Farm.m_tap(self, cen[0], cen[1], emulator_name)

        # m99chetui.png
        ipath = os.path.abspath('.') + '\m_script\images\m99chetui.png'
        cen = Farm.recognize(self, emulator_name, ipath, 15, '撤退' + mem)
        if not cen:
            self.member_result[member_no] = '%s 无法识别 撤退' % member_no
            exit(1)
        Farm.m_tap(self, cen[0], cen[1], emulator_name)

        # m991OK.png
        ipath = os.path.abspath('.') + '\m_script\images\m991OK.png'
        cen = Farm.recognize(self, emulator_name, ipath, 15, 'OK' + mem)
        if not cen:
            self.member_result[member_no] = '%s 无法识别 OK（撤退）' % member_no
            exit(1)
        Farm.m_tap(self, cen[0], cen[1], emulator_name)

        time.sleep(5)

        # m992gonghuizhijia.png
        ipath = os.path.abspath('.') + '\m_script\images\m992gonghuizhijia.png'
        cen = Farm.recognize(self, emulator_name, ipath, 15, '公会之家' + mem)
        if not cen:
            self.member_result[member_no] = '%s 无法识别 公会之家' % member_no
            exit(1)
        Farm.m_tap(self, cen[0], cen[1], emulator_name)

        # m993quanbushouqu.png
        ipath = os.path.abspath('.') + '\m_script\images\m993quanbushouqu.png'
        cen = Farm.recognize(self, emulator_name, ipath, 15, '全部收取' + mem)
        if not cen:
            self.member_result[member_no] = '%s 无法识别 全部收取' % member_no
            exit(1)
        Farm.m_tap(self, cen[0], cen[1], emulator_name)

        # m994guanbi.png
        ipath = os.path.abspath('.') + '\m_script\images\m994guanbi.png'
        cen = Farm.recognize(self, emulator_name, ipath, 15, '关闭' + mem)
        if not cen:
            self.member_result[member_no] = '%s 无法识别 关闭（全部收取）' % member_no
            exit(1)
        Farm.m_tap(self, cen[0], cen[1], emulator_name)

        # m995maoxian.png
        ipath = os.path.abspath('.') + '\m_script\images\m995maoxian.png'
        cen = Farm.recognize(self, emulator_name, ipath, 15, '冒险' + mem)
        if not cen:
            self.member_result[member_no] = '%s 无法识别 冒险（2）' % member_no
            exit(1)
        Farm.m_tap(self, cen[0], cen[1], emulator_name)

        # m996zhuxianguanqia.png
        ipath = os.path.abspath('.') + '\m_script\images\m996zhuxianguanqia.png'
        cen = Farm.recognize(self, emulator_name, ipath, 15, '主线关卡' + mem)
        if not cen:
            self.member_result[member_no] = '%s 无法识别 主线关卡' % member_no
            exit(1)
        Farm.m_tap(self, cen[0], cen[1], emulator_name)

        # m9991sanyi.png
        ipath = os.path.abspath('.') + '\m_script\images\m9991sanyi.png'
        cen = Farm.recognize(self, emulator_name, ipath, 15, '3-1' + mem)
        if not cen:
            self.member_result[member_no] = '%s 无法识别 3-1' % member_no
            exit(1)
        Farm.m_tap(self, cen[0], cen[1], emulator_name)

        # m9992jia.png
        ipath = os.path.abspath('.') + '\m_script\images\m9992jia.png'
        cen = Farm.recognize(self, emulator_name, ipath, 15, '加' + mem)
        if not cen:
            self.member_result[member_no] = '%s 无法识别 加（3-1）' % member_no
            exit(1)
        Farm.m_swipe(self, cen[0], cen[1], cen[0], cen[1], 15000, emulator_name)  # 长按15000ms = 15s

        # m9993shiyong.png
        ipath = os.path.abspath('.') + '\m_script\images\m9993shiyong.png'
        cen = Farm.recognize(self, emulator_name, ipath, 15, '使用' + mem)
        if not cen:
            self.member_result[member_no] = '%s 无法识别 使用' % member_no
            exit(1)
        Farm.m_tap(self, cen[0], cen[1], emulator_name)

        # m9993OK.png
        ipath = os.path.abspath('.') + '\m_script\images\m9993OK.png'
        cen = Farm.recognize(self, emulator_name, ipath, 15, 'OK' + mem)
        if not cen:
            self.member_result[member_no] = '%s 无法识别 OK（使用）' % member_no
            exit(1)
        Farm.m_tap(self, cen[0], cen[1], emulator_name)

        # m9994tiaoguo.png
        ipath = os.path.abspath('.') + '\m_script\images\m9994tiaoguo.png'
        cen = Farm.recognize(self, emulator_name, ipath, 15, '跳过' + mem)
        if cen:
            Farm.m_tap(self, cen[0], cen[1], emulator_name)

        # m9995OK.png
        ipath = os.path.abspath('.') + '\m_script\images\m9995OK.png'
        cen = Farm.recognize(self, emulator_name, ipath, 15, 'OK' + mem)
        if not cen:
            self.member_result[member_no] = '%s 无法识别 OK（跳过）' % member_no
            exit(1)
        Farm.m_tap(self, cen[0], cen[1], emulator_name)

        self.member_result[member_no] = '%s 成功结束）' % member_no


if __name__ == '__main__':
    farm1 = Farm()
    # farm1.getSerialNo()
    farm1.setAccount(os.path.abspath('.') + '\m_script\guild1.txt')
    farm1.printAccount()

    # farm1.memberhavior(farm1.nameList[0], farm1.getMember(1))

    for i in range(14):
        farm1.startGame()
        time.sleep(5)

        print('---------------------------emulator 0 start member %s' % (2 * i + 1))
        t0 = threading.Thread(target=farm1.memberhavior, args=(0, (2 * i + 0), ' - ' + str(2 * i + 1)))
        print('---------------------------emulator 1 start member %s' % (2 * i + 2))
        t1 = threading.Thread(target=farm1.memberhavior, args=(1, (2 * i + 1), ' -  ' + str(2 * i + 2)))

        t0.start()
        t1.start()

        t0.join()
        t1.join()

        if i == 0 or i == 1:
            time.sleep(30)
            print('---------------------------wait 30s')

        farm1.endGame()

    emulatorName = farm1.nameList[0]

    cmd = 'adb -s %s shell am start -n %s' % (emulatorName, farm1.pcrActivityName)
    try:
        os.system(cmd)
    except:
        print('---------------------------%s start game fail' % emulatorName)
        exit(1)

    print('---------------------------emulator 0 start president')

    t = threading.Thread(target=farm1.memberhavior, args=(0, 28, ' - president'))
    t.start()
    t.join()

    time.sleep(30)
    print('---------------------------wait 30s')

    cmd = 'adb -s %s shell am force-stop com.bilibili.priconne' % emulatorName
    try:
        os.system(cmd)
    except:
        print('---------------------------%s end game fail' % emulatorName)
        exit(1)

    fn = os.path.abspath('.') + '\m_script\MAIN ' + time.strftime("%Y-%m-%d %H-%M-%S", time.localtime()) + '.txt'
    farm1.writeMemberResult(fn)