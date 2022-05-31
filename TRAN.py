
import Gui
import sys
import googletrans
from PyQt5 import QtWidgets, QtCore,QtGui, uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox, QLineEdit, QInputDialog, QFileDialog, QTextEdit, QApplication
from PyQt5.QtGui import QTextCursor

import mysql.connector as con


class log(QtWidgets.QMainWindow):
    def __init__(self):
        super(log, self).__init__()
        uic.loadUi('login-form.ui', self)
        self.b1.clicked.connect(self.login)
        self.b2.clicked.connect(self.show_reg)

    def login(self):
        un = self.tb1.text()
        pw = self.tb2.text()
        db = con.connect(host="localhost", user="root", password="", db="sample")
        cursor = db.cursor()
        cursor.execute("select * from userlist where username='" + un + "' and password ='" + pw + "'")
        result = cursor.fetchone()
        self.tb1.setText("")
        self.tb2.setText("")
        if result:
            QMessageBox.information(self, "Login Output", "Congrats!! You login successfully!")
            widget.setCurrentIndex(2)

        else:
            QMessageBox.information(self, "Login Output", "Invalid, Register for new user!")

    def show_reg(self):
        widget.setCurrentIndex(1)


class regi(QtWidgets.QMainWindow):
    def __init__(self):
        super(regi, self).__init__()
        uic.loadUi('register-form.ui', self)
        self.b3.clicked.connect(self.reg)
        self.b4.clicked.connect(self.show_login)


    def reg(self):
        un = self.tb3.text()
        pw = self.tb4.text()
        em = self.tb5.text()
        ph = self.tb6.text()

        db = con.connect(host="localhost", user="root", password="", db="sample")
        cursor = db.cursor()
        cursor.execute("select * from userlist where username=' " + un + "' and password='" + pw + "'")
        result = cursor.fetchone()

        if result:
            QMessageBox.information(self, "Login form", "The user already registered try new username")

        else:
            cursor.execute("insert into userlist values('" + un + "','" + pw + "','" + em + "','" + ph + "')")
            db.commit()
            QMessageBox.information(self, "Login form", "The user registered successfully")

    def show_login(self):
        widget.setCurrentIndex(0)


class Main(QtWidgets.QMainWindow):

    def __init__(self):

        super(Main, self).__init__()
        uic.loadUi('Gui.ui', self)

        self.textEdit.clear()
        self.add_languages()

        self.pushButton.clicked.connect(self.translate)
        self.pushButton_2.clicked.connect(self.clear)
        self.pushButtonb.clicked.connect(self.pushButtonb_handler)
        self.pushButtons.clicked.connect(self.pushButtons_handler)
        self.pushButtoni.clicked.connect(self.pushButtoni_handler)
        self.profile.clicked.connect(self.my_profile)

    def my_profile(self):
        widget.setCurrentIndex(3)

    def add_languages(self):

        for x in googletrans.LANGUAGES.values():
            self.comboBox.addItem(x.capitalize())
            self.comboBox_2.addItem(x.capitalize())

    def translate(self):

        try:

            text_1 = self.textEdit.toPlainText()
            lang_1 = self.comboBox.currentText()
            lang_2 = self.comboBox_2.currentText()

            translator = googletrans.Translator()

            translate = translator.translate(text_1, src=lang_1, dest=lang_2)
            self.textEdit_2.setText(translate.text)


        except Exception as e:
            self.error_message(e)



    def error_message(self,text):

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle('Error')
        msg.setText(str(text))
        msg.exec_()


    def clear(self):

        self.textEdit.clear()

        self.textEdit_2.clear()




    def pushButtonb_handler(self):
        self.open_dialog_box()

    def open_dialog_box(self):
        fname = QFileDialog.getOpenFileName(self,'(*.pdf)')

        path = fname[0]
        self.filename.setText(fname[0])


        with open(path, "r") as f:
            file = f.readline()
            self.textEdit.setText(file)

    def pushButtons_handler(self):
        self.save_file()

    def save_file(self):
        name = QFileDialog.getSaveFileName()
        with open('savedfile.txt', 'w') as wr:

            text = self.textEdit_2.toPlainText()
            wr.write(text)
            QMessageBox.information(self,"Saved","Saved sucessfully")
            widget.setCurrentIndex(2)

    def pushButtoni_handler(self):
        widget.setCurrentIndex(4)

class Myprofile(QtWidgets.QMainWindow):

    def __init__(self):

        super(Myprofile, self).__init__()
        uic.loadUi('profile.ui', self)
        self.back.clicked.connect(self.go_back)
        self.logout.clicked.connect(self.log_out)


    def go_back(self):
        widget.setCurrentIndex(2)

    def log_out(self):

        widget.setCurrentIndex(0)
        QMessageBox.information(self, "LogOut form", "Logout sucessful!")

class Imagetranslator(QtWidgets.QMainWindow):
    def __init__(self):
        super(Imagetranslator,self).__init__()
        uic.loadUi('imagetrans.ui',self)
        self.back.clicked.connect(self.go_back)
        self.clear.clicked.connect(self.clear_btn)
        self.pushButtonb.clicked.connect(self.open_dialog_box)
        self.add_languages()


    def add_languages(self):

        for x in googletrans.LANGUAGES.values():
            self.comboBox.addItem(x.capitalize())
            self.comboBox_2.addItem(x.capitalize())


    def open_dialog_box(self):
        fname = QFileDialog.getOpenFileName(self,'(*.jpg *.png)')
        path = fname[0]
        pixmap = QPixmap(path)

        self.filename.setText(fname[0])
        self.label.setPixmap(QPixmap(pixmap))



    def clear_btn(self):

        self.label.clear()

        self.label.clear()


    def go_back(self):
        widget.setCurrentIndex(2)

a = QtWidgets.QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
loginform = log()
registrationform = regi()
translator = Main()
Profile = Myprofile()
imagetranslation = Imagetranslator()
widget.addWidget(loginform)
widget.addWidget(registrationform)
widget.addWidget(translator)
widget.addWidget(Profile)
widget.addWidget(imagetranslation)
widget.setCurrentIndex(2)


widget.show()
a.exec()
