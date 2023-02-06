import pyperclip
import time
import pyautogui as pg
import os
#稳定不出错
class execute():
    def start(self,prefix,is_time,is_dupforbid,coordinate):
        t=jianting()
        while True:
            # jianting().main()
            text= t.main(prefix,is_time,is_dupforbid,coordinate)
            print("当前粘贴内容：")
            print(text)
    def start_singal(self,prefix,is_time,is_dupforbid,coordinate):
        t = jianting().main(prefix,is_time,is_dupforbid,coordinate)
        print("当前粘贴内容：")
        print(t)
class jianting():
    def __init__(self):
        self.prev_paste=None
    def clipboard_get(self):
        """获取剪贴板数据"""
        data = pyperclip.paste()  #主要这里差别
        return data

    def send_msg(self,prefix,is_time,coordinate,msg):
        # 操作间隔为1秒
        width, height = pg.size()
        # print(width)
        # print(height)
        pg.PAUSE = 0.5
        nowtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        if is_time==True:
            unit=prefix+'\n'+nowtime+'\n'#单位：上海局徐州处\n'
        else:
            unit = prefix  + '\n'
        pyperclip.copy(unit+msg)
        # title=os.path.basename(__file__)[:-3]+".exe"#'C:\Windows\system32\cmd.exe' 'autopaste.exe'
        currentMouseX, currentMouseY = pg.position()
        # if len(pg.getWindowsWithTitle(title))!=0:
        #     pg.getWindowsWithTitle(title)[0].restore()
        # pg.click(width-200, height-100, 1,button='left')

        pg.click(coordinate[0], coordinate[1], 1, button='left')

        pg.hotkey('ctrl', 'v')
        pg.press('enter')
        pg.moveTo(currentMouseX, currentMouseY)
        self.prev_paste=msg
        # if len(pg.getWindowsWithTitle(title)) != 0:
        #     pg.getWindowsWithTitle(title)[0].minimize()
        # pg.click(width-200, height-200, 1, button='left')
        # otkey('ctrl', 'alt', 'w')
        # pg.hotkey('ctrl', 'f')
        # # 找到好友
        # pyperclip.copy(name)
        # pg.hotkey('ctrl', 'v')
        # pg.press('enter')
        # # 发送消息
        # pyperclip.copy(msg)
        # pg.hotkey('ctrl', 'v')
        # pg.press('enter')
        #
        # # 隐藏微信
        # time.sleep(0.3)
        # pg.hotkey('ctrl', 'alt', 'w')


    def main(self,prefix,is_time,is_dupforbid,coordinate):
        """后台脚本：每隔0.2秒，读取剪切板文本，检查有无指定字符或字符串，如果有则执行替换"""
        # recent_txt 存放最近一次剪切板文本，初始化值只多执行一次paste函数读取和替换
        recent_txt = self.clipboard_get()

        while True:
            # 检测间隔（延迟0.2秒）
            time.sleep(0.2)
            # txt 存放当前剪切板文本
            txt = self.clipboard_get()
            dupforbid=(txt!=self.prev_paste)if is_dupforbid else True
            # 剪切板内容和上一次对比如有变动，再进行内容判断，判断后如果发现有指定字符在其中的话，再执行替换
            if txt != recent_txt and dupforbid and txt!='':
                # print(f'txt:{txt}')
                recent_txt = txt  # 没查到要替换的子串，返回None
                self.send_msg(prefix,is_time,coordinate,recent_txt)
                return recent_txt




# if __name__ == '__main__':
#     execute().start()
