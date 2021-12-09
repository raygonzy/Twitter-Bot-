
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QMainWindow
from TwitterFunction import TwitterBot
from PyQt5.QtCore import Qt, pyqtSignal

class Ui_second_window(QMainWindow):
    window_closed = pyqtSignal()

    def closeEvent(self,event):
        self.window_closed.emit()
        event.accept()

    def setupUi(self, second_window):
        second_window.setObjectName("second_window")
        self.setWindowIcon(QtGui.QIcon('./Files/icon.png'))
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)

        self.setFixedSize(563, 276)

        font = QtGui.QFont()
        font.setFamily("Mongolian Baiti")

        self.setFont(font)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(140, 10, 141, 31))

        font = QtGui.QFont()
        font.setFamily("Mongolian Baiti")
        font.setPointSize(15)

        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 70, 101, 16))

        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 110, 131, 21))

        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(20, 150, 151, 21))

        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(20, 190, 141, 21))

        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(20, 230, 191, 21))

        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")

        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(190, 60, 251, 31))
        self.lineEdit.setFont(font)
        self.lineEdit.setObjectName("lineEdit")

        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(190, 100, 251, 31))
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setObjectName("lineEdit_2")

        self.lineEdit_3 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_3.setGeometry(QtCore.QRect(190, 140, 251, 31))
        self.lineEdit_3.setFont(font)
        self.lineEdit_3.setObjectName("lineEdit_3")

        self.lineEdit_4 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_4.setGeometry(QtCore.QRect(190, 180, 251, 31))
        self.lineEdit_4.setFont(font)
        self.lineEdit_4.setObjectName("lineEdit_4")

        self.lineEdit_5 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_5.setGeometry(QtCore.QRect(190, 220, 251, 31))
        self.lineEdit_5.setFont(font)
        self.lineEdit_5.setObjectName("lineEdit_5")


        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(390, 10, 161, 31))

        self.comboBox.setFont(font)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.currentTextChanged.connect(self.on_combobox_changed)
        self.TwitterB = TwitterBot()
        
        self.editButton = QtWidgets.QPushButton(self.centralwidget)
        self.editButton.setGeometry(QtCore.QRect(460, 60, 91, 41))
        self.editButton.setFont(font)
        self.editButton.setObjectName("editButton")
        self.editButton.clicked.connect(self.edit_button_clicked)

        self.saveButton = QtWidgets.QPushButton(self.centralwidget)
        self.saveButton.setGeometry(QtCore.QRect(460, 160, 91, 41))
        self.saveButton.setFont(font)
        self.saveButton.setObjectName("saveButton")
        self.saveButton.clicked.connect(self.save_button_clicked)

        self.deleteButton = QtWidgets.QPushButton(self.centralwidget)
        self.deleteButton.setGeometry(QtCore.QRect(460, 210, 91, 41))
        self.deleteButton.setFont(font)
        self.deleteButton.setObjectName("deleteButton")
        self.deleteButton.clicked.connect(self.delete_button_clicked)

        self.exitButton = QtWidgets.QPushButton(self.centralwidget)
        self.exitButton.setGeometry(QtCore.QRect(460, 210, 91, 41))
        self.exitButton.setFont(font)
        self.exitButton.setObjectName("exitButton")
        self.exitButton.clicked.connect(self.exit_button_clicked)

        font.setPointSize(10)
        self.addButton = QtWidgets.QPushButton(self.centralwidget)
        self.addButton.setGeometry(QtCore.QRect(460, 110, 91, 41))
        self.addButton.setFont(font)
        self.addButton.setObjectName("addButton")
        self.addButton.clicked.connect(self.add_button_clicked)

        self.msg = QMessageBox()
        self.reset()
        self.show()
        
        self.setCentralWidget(self.centralwidget)
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def reset(self):
        self.lineEdit_clear()
        self.view_buttons(True,True,False,True,False)
        self.comboBox.clear()
        self.Items()
        self.delete = False

    def delete_button_clicked(self):
        name = str(self.comboBox.currentText())
        if name == '': return
        if self.delete:
            b = True
        else:
            b = self.raise_question()
        if b: 
            self.TwitterB.delete_data(name)
            self.reset()

    def exit_button_clicked(self):
        self.reset()

    def raise_question(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setWindowTitle("Delete")
        msg.setText("Do you want to delete user profile?")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.setDefaultButton(QMessageBox.Cancel)
        ret = msg.exec_()
        if ret == QMessageBox.Ok:
            return True
        return False


    def error_message(self,message):
        self.msg.setIcon(QMessageBox.Critical)
        self.msg.setText("Error!")
        self.msg.setInformativeText(message)
        self.msg.setWindowTitle("Oops!")
        self.msg.exec_()

    def save_button_clicked(self):

        texts = self.lineEdit_get_text()
        error = '' in texts
        if error: 
            self.error_message('Please complete all the details.')
            return

        if self.delete: self.delete_button_clicked()
        [name, consumer_key, consumer_secret, access_token, access_token_secret] = texts
        valid = self.TwitterB.check_if_valid_keys(consumer_key, consumer_secret, access_token, access_token_secret)
        
        if not valid:
            self.error_message('Keys not valid! Double check the keys')
            return

        success = self.TwitterB.add_new_user(name, consumer_key, consumer_secret, access_token, access_token_secret, self.delete)
        if not success: #
            self.error_message('Username already in the system.')
            self.lineEdit.setText('')
            return #
        self.reset()
        self.comboBox.setCurrentText(name)


    def add_button_clicked(self):
        self.lineEdit_clear()
        self.lineEdit_color('black')
        self.activate_view_only(False)
        self.view_buttons(False,False,True,False,True)

    def view_buttons(self, edit_button, add_button, save_button, delete_button, exit_button):
        self.editButton.setVisible(edit_button)
        self.addButton.setVisible(add_button)
        self.saveButton.setVisible(save_button)
        self.deleteButton.setVisible(delete_button)
        self.exitButton.setVisible(exit_button)

    def edit_button_clicked(self):
        self.activate_view_only(False)
        self.lineEdit_color('black')
        self.view_buttons(False,False,True,False,True)
        self.delete = True 


    def Items(self):
        data = self.TwitterB.read_data()
        if len(data) == 0: 
            self.view_buttons(False,True,False,False,False)
            self.activate_view_only(True)
            return
        for d in data:
            name = d['name']
            self.comboBox.addItem(name)

    def on_combobox_changed(self):
        text = str(self.comboBox.currentText())
        if text == '': return
        [name, ck, cs, at, ats] = self.TwitterB.view_user_data(text)
        self.lineEdit.setText(text)
        self.lineEdit_2.setText(ck)
        self.lineEdit_3.setText(cs)
        self.lineEdit_4.setText(at)
        self.lineEdit_5.setText(ats)
        self.lineEdit_color('gray')
        self.activate_view_only(True)

    def lineEdit_clear(self):
        self.lineEdit.setText('')
        self.lineEdit_2.setText('')
        self.lineEdit_3.setText('')
        self.lineEdit_4.setText('')
        self.lineEdit_5.setText('')

    def lineEdit_color(self,color):
        self.lineEdit.setStyleSheet("color: {}".format(color))
        self.lineEdit_2.setStyleSheet("color: {}".format(color))
        self.lineEdit_3.setStyleSheet("color: {}".format(color))
        self.lineEdit_4.setStyleSheet("color: {}".format(color))
        self.lineEdit_5.setStyleSheet("color: {}".format(color))

    def lineEdit_get_text(self):
        a = self.lineEdit.text()
        b = self.lineEdit_2.text()
        c = self.lineEdit_3.text()
        d = self.lineEdit_4.text()
        e = self.lineEdit_5.text()
        return [a,b,c,d,e]


    def activate_view_only(self, b):
        self.lineEdit.setReadOnly(b)
        self.lineEdit_2.setReadOnly(b)
        self.lineEdit_3.setReadOnly(b)
        self.lineEdit_4.setReadOnly(b)
        self.lineEdit_5.setReadOnly(b)


    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("second_window", "Accounts"))
        self.label.setText(_translate("second_window", "Account Details"))
        self.label_2.setText(_translate("second_window", "username:"))
        self.label_3.setText(_translate("second_window", "consumer key:"))
        self.label_4.setText(_translate("second_window", "consumer secret:"))
        self.label_5.setText(_translate("second_window", "access token:"))
        self.label_6.setText(_translate("second_window", "access token secret:"))
        self.editButton.setText(_translate("second_window", "Edit"))
        self.addButton.setText(_translate("second_window", "Add Account"))
        self.deleteButton.setText(_translate("second_window", "Delete"))
        self.saveButton.setText(_translate("second_window", "Save"))
        self.exitButton.setText(_translate("second_window", "Exit"))

