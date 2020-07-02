import os


def m_tap(x, y, name):
    print(name)
    print(x, y)
    com = 'adb -s' + name + 'shell input tap %s %s' % (x, y)
    try:
        os.system(com)
    except:
        print('click fail' + name)
        exit(1)
    print(com)


def m_swipe(x1, y1, x2, y2, duration, name):
    print(x1, y1, x2, y2)
    com = 'adb -s' + name + 'shell input swipe %s %s %s %s %s' % (x1, y1, x2, y2, duration)
    try:
        os.system(com)
    except:
        print('swipe fail' + name)
        exit(1)
    print(com)


def m_text(s, name):
    com = 'adb -s' + name + 'shell input text %s' % s
    try:
        os.system(com)
    except:
        print('text fail' + name)
        exit(1)
    print(com)
