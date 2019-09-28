from PyQt5.QtWidgets import (QWidget, QPushButton,
    QLineEdit, QApplication,QLabel,QHBoxLayout,QVBoxLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont,QPixmap

import sys

def colloaction(id):
    #调用搭配系统
    #返回结果['id1','id2',...'idn']
    if id == '29':
        re = ['476354', '1315712','2485576','3138268', '3136530' ,'399283', '1061113', '2769393', '1903386', '2139972']
    return re

class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

        self.id = ''#输入框数据
        self.coll = []#返回搭配
        self.coll_num = 1#返回搭配数量
        self.page_now = 1#当前页数


    def initUI(self):
        tip = QLabel('图片名： ')
        # 文本事件
        pictureEdit = QLineEdit()
        pictureEdit.textChanged[str].connect(self.onChanged)

        self.btn = QPushButton('搭配', self)
        self.btn.setCheckable(True)
        # 按钮事件
        self.btn.clicked[bool].connect(self.get_id)

        self.leftBtn = QPushButton('←',self)
        self.leftBtn.setCheckable(True)
        self.leftBtn.clicked[bool].connect(self.last_page)

        self.rightBtn = QPushButton('→',self)
        self.rightBtn.setCheckable(True)
        self.rightBtn.clicked[bool].connect(self.next_page)

        self.pageLabel = QLabel('0/0')

        self.searchLabel = QLabel(self)
        self.searchLabel.resize(370,450)
        search = QPixmap('0.jpg').scaled(self.searchLabel.width(), self.searchLabel.height())
        self.searchLabel.setPixmap(search)
        #searchLabel.setScaledContents(True)

        self.findLabel = QLabel(self)
        self.findLabel.resize(370,450)
        find = QPixmap('0.jpg').scaled(self.findLabel.width(),self.findLabel.height())
        self.findLabel.setPixmap(find)
        #findLabel.setScaledContents(True)

        self.searchIdLabel = QLabel(' ')
        self.findIIdLabel = QLabel(' ')

        #布局
        #检索行
        hbox = QHBoxLayout()
        hbox.addWidget(tip)
        hbox.addWidget(pictureEdit)
        hbox.addWidget(self.btn)

        #图片行
        ssbox = QVBoxLayout()
        ssbox.addWidget(self.searchLabel,0,Qt.AlignHCenter)
        ssbox.addWidget(self.searchIdLabel,0,Qt.AlignHCenter)
        ffbox = QVBoxLayout()
        ffbox.addWidget(self.findLabel,0,Qt.AlignHCenter)
        ffbox.addWidget(self.findIIdLabel, 0, Qt.AlignHCenter)
        hbox2 = QHBoxLayout()
        hbox2.addLayout(ssbox)
        hbox2.addLayout(ffbox)

        #按钮行
        groupbox = QHBoxLayout()
        groupbox.addWidget(self.leftBtn)
        groupbox.addWidget(self.pageLabel,0,Qt.AlignHCenter)
        groupbox.addWidget(self.rightBtn)
        emptybox = QHBoxLayout()
        empty = QLabel('')
        emptybox.addWidget(empty)
        hbox3 = QHBoxLayout()
        hbox3.addLayout(emptybox)
        hbox3.addLayout(groupbox)

        #总布局
        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)

        self.setLayout(vbox)

        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('cloth')
        self.show()

    def onChanged(self,text):
        self.id = text

    def switch_pageLabel(self):
        s = str(self.page_now) +'/'+str(self.coll_num)
        self.pageLabel.setText(s)

    def switch_findLabel(self,item):
        self.findLabel.resize(300, 400)
        t = str(item) + '.jpg'
        self.findIIdLabel.setText(t)#修改显示文本
        t = 'pics/' + t
        find = QPixmap(t).scaled(self.findLabel.width(), self.findLabel.height())
        self.findLabel.setPixmap(find)

    #搭配按钮事件
    def get_id(self,pressed):
        if pressed:
            self.btn.toggle()
            print(self.id)
            #获得搭配列表
            self.coll = colloaction(self.id)
            self.coll_num = len(self.coll)
            #处理page label
            self.page_now = 1
            self.switch_pageLabel()
            #显示图片
            #search
            self.searchLabel.resize(300, 400)
            t = str(self.id) + '.jpg'
            self.searchIdLabel.setText(t)
            t = 'pics/' + t
            search = QPixmap(t).scaled(self.searchLabel.width(), self.searchLabel.height())
            self.searchLabel.setPixmap(search)
            #find
            self.switch_findLabel(self.coll[0])

    def last_page(self,pressed):
        if pressed:
            self.leftBtn.toggle()
            if self.page_now > 1:
                #处理page label
                self.page_now -= 1
                self.switch_pageLabel()
                #处理图片
                self.switch_findLabel(self.coll[self.page_now-1])

    def next_page(self,pressed):
        if pressed:
            self.rightBtn.toggle()
            if self.page_now < self.coll_num:
                # 处理page label
                self.page_now += 1
                self.switch_pageLabel()
                # 处理图片
                self.switch_findLabel(self.coll[self.page_now-1])



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

