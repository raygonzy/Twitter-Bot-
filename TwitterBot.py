
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QKeySequence, QMovie
from PyQt5.QtWidgets import QMessageBox, QMainWindow, QApplication
from PyQt5.QtCore import QCoreApplication, QThread

from second_window import Ui_second_window
from TwitterFunction import TwitterBot
from screeninfo import get_monitors
import time

class ThreadClass(QtCore.QThread):
    
    any_signal = QtCore.pyqtSignal(int)
    def __init__(self, parent=None,index=0, data=[]):
        super(ThreadClass, self).__init__(parent)
        self.index = index
        self.is_running = True
        self.data = data

    def run(self):
        tweet_id = self.data[0]
        max_delay = self.data[1]

        success = TwitterBot().like_n_retweet(int(tweet_id), max_delay)
        print('success',success)
        if not success:
            self.any_signal.emit(False) 
        else:
            self.any_signal.emit(True) 

    def stop(self):
        self.is_running = False
        self.terminate()


class Ui_MainWindow(QThread):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(548, 217)
        MainWindow.setWindowIcon(QtGui.QIcon('./Files/icon.png'))
        MainWindow.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
        
        self.m = get_monitors()[0]
        w = self.m.width//3
        h = self.m.height//4 
        MainWindow.move(w, h)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(240, 110, 121, 41))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.like_n_retweet)

        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(430, 10, 101, 31))

        font = QtGui.QFont()
        font.setFamily("Mongolian Baiti")
        font.setPointSize(10)

        font2 = QtGui.QFont()
        font2.setFamily("Mongolian Baiti")
        font2.setPointSize(15)

        self.comboBox.setFont(font)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("0 second")
        self.comboBox.addItem("30 seconds")
        self.comboBox.addItem("1 minute")
        self.comboBox.addItem("5 minutes")
        self.comboBox.addItem("10 minutes")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(260, 10, 161, 31))

        self.label.setFont(font)
        self.label.setObjectName("label")

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 60, 111, 31))

        self.label_2.setFont(font2)
        self.label_2.setObjectName("label_2")

        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(460, 160, 81, 31))

        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(10, 160, 151, 31))

        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(145, 160, 31, 31))

        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(130, 60, 401, 31))
        self.lineEdit.setFont(font2)
        self.lineEdit.setObjectName("lineEdit")

        fontx = QtGui.QFont()
        fontx.setFamily("Cambria Math")
        fontx.setPointSize(10)

        self.label_3.setFont(fontx)
        self.label_3.setObjectName("label_3")

        MainWindow.setCentralWidget(self.centralwidget)

        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 548, 21))
        self.menuBar.setObjectName("menuBar")

        self.menuFile = QtWidgets.QMenu(self.menuBar)
        self.menuFile.setObjectName("menuFile")

        MainWindow.setMenuBar(self.menuBar)

        self.actionView_Accounts = QtWidgets.QAction(MainWindow)
        self.actionView_Accounts.setObjectName("actionView_Accounts")
        self.actionView_Accounts.triggered.connect(lambda : self.openWindow())

        self.actionExit_Ctrl_Q = QtWidgets.QAction(MainWindow)
        self.actionExit_Ctrl_Q.setObjectName("actionExit_Ctrl_Q")
        self.actionExit_Ctrl_Q.triggered.connect(lambda : self.exitApp())
        self.actionExit_Ctrl_Q.setShortcut(QKeySequence("Ctrl+Q"))

        self.menuFile.addAction(self.actionView_Accounts)
        self.menuFile.addAction(self.actionExit_Ctrl_Q)
        self.menuBar.addAction(self.menuFile.menuAction())

        self.set_background()
        self.re_init()
        self.msg = QMessageBox()
        self.msg.setWindowIcon(QtGui.QIcon('./Files/icon.png'))

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def set_background(self):
        self.movie = QMovie("./Files/loading.gif")
        self.background = QtWidgets.QLabel(self.centralwidget)
        self.background.setGeometry(QtCore.QRect(0, 0, 548, 196))
        self.background.setObjectName("lb1")
        self.background.setMovie(self.movie)
        self.movie.start()
        self.background.setVisible(False)

    def loading(self):
        self.background.setVisible(not self.background.isVisible())

    def worker(self,data):
        self.thread = ThreadClass(parent=None,index=1,data=data)
        self.thread.start()
        self.thread.any_signal.connect(self.signal)

    def signal(self, success):
        if not success:
            self.error_message('Tweet not available')
        else:
            self.info_message()
        self.thread.stop()
        self.loading()


    def like_n_retweet(self):

        text = str(self.lineEdit.text())
        try:
            tweet_id = int(text.rsplit('/', 1)[-1])
        except:
            return
        if not isinstance(tweet_id, int): return
        max_delay = self.comboBox.currentText()
        max_delay = int(max_delay.rsplit(' ')[0])
        if max_delay != 30: max_delay *= 60

        self.loading()
        self.worker([tweet_id, max_delay])
        self.lineEdit.clear()

    def info_message(self):
        self.msg.setIcon(QMessageBox.Information)
        self.msg.setText("Likes and Retweets Done!")
        self.msg.setWindowTitle("Success!")
        self.msg.exec_()

    def error_message(self,message):
        self.msg.setIcon(QMessageBox.Critical)
        self.msg.setText("Error!")
        self.msg.setInformativeText(message)
        self.msg.setWindowTitle("Oops!")
        self.msg.exec_()

    def openWindow(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_second_window()
        self.ui.setupUi(self.window)
        self.ui.window_closed.connect(self.second_window_closed)

    def second_window_closed(self):
        self.view_total_user()

    def exitApp(self):
        app.quit()

    def do_something(self):
        print('do_something')

    def view_total_user(self):
        self.TwitterB = TwitterBot()
        n = self.TwitterB.get_total_user()
        self.label_5.setText(str(n))

        le = True if n > 0 else False
        self.lineEdit.setEnabled(le)

    def re_init(self):
        self.view_total_user()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Twitter Bot"))
        self.pushButton.setText(_translate("MainWindow", "Like and Retweet"))
        self.label.setText(_translate("MainWindow", "Max Random Delay Interval:"))
        self.label_2.setText(_translate("MainWindow", "Twitter Link:"))
        self.label_3.setText(_translate("MainWindow", "ACB-Solutions"))
        self.label_4.setText(_translate("MainWindow", "Total Number of Accounts:"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionView_Accounts.setText(_translate("MainWindow", "Account Setting"))
        self.actionExit_Ctrl_Q.setText(_translate("MainWindow", "Exit"))



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
