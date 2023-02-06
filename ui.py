import sys  # 系统内置类
from PyQt5.QtCore import * # 主要包含了我们常用的一些类，汇总到了一块
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import autopaste
import pyautogui as pg

class Thread_1(QThread):  # 线程1
    st = pyqtSignal()
    def __init__(self):
        super(Thread_1, self).__init__()
        self.fun = autopaste.execute()

    def accept(self,prefix,is_time,is_dupforbid,coordinate):
        self.prefix = prefix
        self.is_time=is_time
        self.is_dupforbid=is_dupforbid
        self.coordinate=coordinate

    def run(self):
        self.st.emit()
        self.fun.start(self.prefix,self.is_time,self.is_dupforbid,self.coordinate)





class MainWidget(QWidget):
    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)
        # 创建一个空白控件(窗口)
        self.fun = autopaste.execute()
        # 设置窗口标题
        self.setWindowTitle("自动辅助工具")
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        # 设置窗口尺寸
        self.resize(500, 300)
        # # 移动窗口位置
        # window.move(200, 200)
        self.setMouseTracking(True)

        self.title = QLabel(self)
        self.title.setText("自动辅助工具")
        self.title.move(150, 10)
        self.title.resize(200,50)
        self.title.setFont(QFont('宋体', 20))
        self.label1 = QLabel(self)
        self.label1.setText("执行自动粘贴")
        self.label1.move(10, 100)

        self.label2 = QLabel(self)
        self.label2.setText("状态：未启动")
        self.label2.move(100, 100)

        self.prefix_text=QLineEdit(self)
        self.prefix_text.setPlaceholderText('请输入需要插入在粘贴内容前的文本')
        self.prefix_text.move(200,120)
        self.prefix_text.resize(QSize(250,20))
        self.prefix_text.textChanged.connect(lambda: self.onChange_prefix(self.prefix_text.text()))#文本框改变时重新设置
        self.prefix =""#"单位：上海局徐州处"
        self.prefix_label = QLabel(self)
        self.prefix_label.setText("前缀：")
        self.prefix_label.move(200, 100)

        self.prefix_label2 = QLabel(self)
        self.prefix_label2.setText("（在运行期间无法更改前缀！）")
        self.prefix_label2.move(200, 170)

        self.check_time=QCheckBox('加入当前时间',self)
        self.check_time.move(200,150)
        self.check_time.stateChanged.connect(lambda: self.onChange_time(self.check_time.isChecked()))
        self.check_dupforbid=QCheckBox('禁止重复粘贴',self)
        self.check_dupforbid.move(50,150)
        self.check_dupforbid.stateChanged.connect(lambda: self.onChange_dupforbid(self.check_dupforbid.isChecked()))
        self.is_time=False
        self.is_dupforbid=False

        self.thread1=Thread_1()
        self.thread1.st.connect(lambda: self.ap_start())#执行自动粘贴程序的线程
        self.bt1 = QPushButton(self)
        self.bt1.setText('启动')
        self.bt1.move(10, 120)
        self.bt1.clicked.connect(lambda:self.start_thread(self.thread1,self.prefix,self.is_time,self.is_dupforbid,self.dialog.coordinate))#点击按钮时启动线程
        self.bt2 = QPushButton(self)
        self.bt2.setText('停止')
        self.bt2.move(100, 120)
        self.bt2.clicked.connect(lambda: self.ap_stop())

        self.bt3 = QPushButton(self)
        self.bt3.setText('设置粘贴位置')
        self.bt3.move(350, 200)
        self.bt3.clicked.connect(lambda: self.coor(self.dialog))

        self.dialog = My_Dialog(self)
        self.dialog.setMouseTracking(True)
        # print(self.dialog.hasMouseTracking())  # 返回设置的状态


        self.coordinate_label=QLabel(self)
        self.coordinate_label.move(300, 230)
        self.coordinate_label.resize(200,100)




    def mouseMoveEvent(self, event):
        # globalPos = self.mapToGlobal(event.pos())  # 窗口坐标转换为屏幕坐标
        # self.coordinate_label.setText("""鼠标位置：
        # 窗口坐标为：({0}, {1})
        # 屏幕坐标为：({2}, {3}) """.format(event.pos().x(), event.pos().y(), globalPos.x(), globalPos.y()))
        # # print(self.coordinate)
        self.coordinate_label.setText(
            """粘贴坐标为：({0}, {1})""".format(self.dialog.coordinate[0], self.dialog.coordinate[1]))
        self.update()

    def coor(self,dialog):
        dialog.show()
        # print(dialog.coordinate)



    def onChange_prefix(self,text):
        self.prefix=text
        # print(text)
        # print("...", facename)

    def onChange_time(self,is_time):
        self.is_time= is_time


    def onChange_dupforbid(self,is_dupforbid):
        self.is_dupforbid= is_dupforbid


    def start_thread(self,thread,prefix,is_time,is_dupforbid,coordinate):
        try:
            thread.accept(prefix,is_time,is_dupforbid,coordinate)
            thread.start()
        except Exception as e:
            print(e)


    def ap_start(self):

        self.label2.setText("状态：已启动")

    def ap_stop(self):
        self.thread1.terminate()
        self.label2.setText("状态：未启动")


class My_Dialog(QDialog):
    def __init__(self, parent=None):
        super(My_Dialog, self).__init__(parent)
        width,height=pg.size()
        self.setWindowOpacity(0.5)
        # self.setStyleSheet("background: transparent;border:0px")
        # self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, False)


        # self.setupUi()
        self.coordinate_label=QLabel(self)
        self.coordinate_label.move(width//5,height//5)
        self.coordinate_label.resize(400,200)

        self.coordinate=(width-200,height-100)

        self.last_coordinate = QLabel(self)
        self.last_coordinate.resize(200,20)
        self.last_coordinate.setStyleSheet('border-width: 1px;border-style: solid;border-color: rgb(255, 170, 0);background-color: rgb(100, 149, 237);')
        self.last_coordinate.move(self.coordinate[0],self.coordinate[1])
        self.last_coordinate.setText("<-当前已设置的粘贴位置！")
        self.last_coordinate.setAlignment(Qt.AlignLeft)

    # def paintEvent(self, e):
    #     qp = QPainter()
    #     qp.begin(self)
    #     self.drawPoints(qp)
    #     qp.end()
    #
    # def drawPoints(self, qp):
    #
    #     qp.setPen(Qt.GlobalColor.red)
    #     size = self.size()
    #     qp.drawPoint(self.coordinate[0], self.coordinate[1])

    def setupUi(self):
        # self.setWindowFlags(Qt.framelessWindowHint)  # 去除边框

        self.setWindowFlags(Qt.Dialog | Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)  # 最大化最小化关闭按钮
        pass

    def mouseMoveEvent(self, QMouseEvent):  # 5
        x = QMouseEvent.x()
        y = QMouseEvent.y()
        self.coordinate_label.setText("""鼠标位置：
        屏幕坐标为：({}, {}),
        请在屏幕上选择位置单击以确定粘贴坐标！""".format(x, y))
        # print(self.coordinate)
        self.update()

    def mousePressEvent(self, QMouseEvent):
        x = QMouseEvent.x()
        y = QMouseEvent.y()
        global_x = QMouseEvent.globalX()
        global_y = QMouseEvent.globalY()
        self.coordinate=(x,y)
        self.last_coordinate.move(x, y)
        self.close()

    def return_coordinate(self):
        return self.coordinate





if __name__ == '__main__':
    # 创建一个应用程序对象
    app = QApplication(sys.argv)

    windows=MainWidget()
    windows.show()
    # 进入程序的主循环，并通过exit函数确保主循环安全结束
    sys.exit(app.exec_())