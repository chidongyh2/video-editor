# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main2.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import os
from EditorVideo import chen_video
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(582, 203)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(20, 20, 551, 161))
        self.groupBox.setObjectName("groupBox")
        self.account_laybel = QtWidgets.QLabel(self.groupBox)
        self.account_laybel.setGeometry(QtCore.QRect(20, 20, 151, 16))
        self.account_laybel.setObjectName("account_laybel")
        self.btn_LD_link = QtWidgets.QToolButton(self.groupBox)
        self.btn_LD_link.setGeometry(QtCore.QRect(230, 40, 31, 21))
        self.btn_LD_link.setObjectName("btn_LD_link")
        self.LD_link = QtWidgets.QLineEdit(self.groupBox)
        self.LD_link.setGeometry(QtCore.QRect(20, 40, 201, 20))
        self.LD_link.setObjectName("LD_link")
        self.btn_load = QtWidgets.QPushButton(self.groupBox)
        self.btn_load.setGeometry(QtCore.QRect(310, 60, 51, 31))
        self.btn_load.setObjectName("btn_load")
        self.label_success = QtWidgets.QLabel(self.groupBox)
        self.label_success.setGeometry(QtCore.QRect(440, 70, 51, 16))
        self.label_success.setObjectName("label_success")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(375, 70, 61, 16))
        self.label.setObjectName("label")
        self.btn_LD_link_2 = QtWidgets.QToolButton(self.groupBox)
        self.btn_LD_link_2.setGeometry(QtCore.QRect(230, 90, 31, 21))
        self.btn_LD_link_2.setObjectName("btn_LD_link_2")
        self.account_laybel_2 = QtWidgets.QLabel(self.groupBox)
        self.account_laybel_2.setGeometry(QtCore.QRect(20, 70, 151, 16))
        self.account_laybel_2.setObjectName("account_laybel_2")
        self.LD_link_2 = QtWidgets.QLineEdit(self.groupBox)
        self.LD_link_2.setGeometry(QtCore.QRect(20, 90, 201, 20))
        self.LD_link_2.setObjectName("LD_link_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox.setTitle(_translate("MainWindow", "Render"))
        self.account_laybel.setText(_translate("MainWindow", "Link video chính:"))
        self.btn_LD_link.setText(_translate("MainWindow", "..."))
        self.LD_link.setText(_translate("MainWindow", "D:\\anyfolder"))
        self.btn_load.setText(_translate("MainWindow", "Start"))
        self.label_success.setText(_translate("MainWindow", "0"))
        self.label.setText(_translate("MainWindow", "Trạng thái"))
        self.btn_LD_link_2.setText(_translate("MainWindow", "..."))
        self.account_laybel_2.setText(_translate("MainWindow", "Link video phụ:"))
        self.LD_link_2.setText(_translate("MainWindow", "D:\\anyfolder"))
        #add manual
        self.btn_LD_link.clicked.connect(self.FileDialogLD)
        self.btn_LD_link_2.clicked.connect(self.FileDialogLD2)
        self.btn_load.clicked.connect(self.Start)
    
    def FileDialogLD(self):
        self.filepath2 = QtWidgets.QFileDialog()
        self.filepath2.setFileMode(QtWidgets.QFileDialog.FileMode.AnyFile)
        self.filepath2.show()
        if self.filepath2.exec_() == QtWidgets.QDialog.Accepted: 
            folder = self.filepath2.selectedFiles()[0]
            self.LD_link.setText(folder)
            
    def FileDialogLD2(self):
        self.filepath2 = QtWidgets.QFileDialog()
        self.filepath2.setFileMode(QtWidgets.QFileDialog.FileMode.AnyFile)
        self.filepath2.show()
        if self.filepath2.exec_() == QtWidgets.QDialog.Accepted: 
            folder = self.filepath2.selectedFiles()[0]
            self.LD_link_2.setText(folder)
            
    def Start(self):
        try:
            self.label_success.setText(f"<p><span style=\" color:#00aa00;\"> Đang chạy ...</span></p>")
            if len(self.LD_link.text()) <= 1 or not os.path.exists(self.LD_link.text()):
                self.Mesagebox(text="Chọn video chính !")
                return
            if len(self.LD_link_2.text()) <= 1 or not os.path.exists(self.LD_link_2.text()):
                self.Mesagebox(text="Chọn video phu !")
                return
            else:
                videoName = self.LD_link.text().split("/")[len(self.LD_link.text().split("/")) - 1]
                chen_video(self.LD_link.text(), self.LD_link_2.text(), f"video-results/finished_{videoName}")
                self.label_success.setText(f"<p><span style=\" color:#00aa00;\"> Đã xong ! </span></p>")
        except Exception as e:
            print(e)
            self.Mesagebox(text="Load dữ liệu lỗi! Vui lòng kiểm tra lại.")
            
    def Mesagebox(self, title="Thông báo", text=""):
        self.msg = QtWidgets.QMessageBox()
        self.msg.setIcon(QtWidgets.QMessageBox.Warning)
        self.msg.setWindowTitle(title)
        self.msg.setText(text)
        self.msg.show()
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
