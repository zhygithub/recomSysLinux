# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainUI.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(528, 641)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tb_result_show = QtWidgets.QTextBrowser(self.centralwidget)
        self.tb_result_show.setGeometry(QtCore.QRect(20, 110, 481, 491))
        font = QtGui.QFont()
        font.setFamily("方正细黑一_GBK")
        font.setBold(False)
        font.setWeight(50)
        self.tb_result_show.setFont(font)
        self.tb_result_show.setObjectName("tb_result_show")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(150, 10, 171, 80))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.edt_user_count = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.edt_user_count.setObjectName("edt_user_count")
        self.horizontalLayout.addWidget(self.edt_user_count)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.edt_item_count = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.edt_item_count.setObjectName("edt_item_count")
        self.horizontalLayout_2.addWidget(self.edt_item_count)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(340, 10, 160, 80))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.btn_run = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.btn_run.setObjectName("btn_run")
        self.verticalLayout_2.addWidget(self.btn_run)
        self.btn_save = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.btn_save.setObjectName("btn_save")
        self.verticalLayout_2.addWidget(self.btn_save)
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(20, 10, 111, 80))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.btn_data_source = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.btn_data_source.setObjectName("btn_data_source")
        self.verticalLayout_3.addWidget(self.btn_data_source)
        self.cb_way = QtWidgets.QComboBox(self.verticalLayoutWidget_3)
        self.cb_way.setObjectName("cb_way")
        self.verticalLayout_3.addWidget(self.cb_way)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "欢迎使用基于近邻的 UserBased 推荐系统"))
        self.label.setText(_translate("MainWindow", "相似用户数"))
        self.label_2.setText(_translate("MainWindow", "推荐物品数"))
        self.btn_run.setText(_translate("MainWindow", "运行"))
        self.btn_save.setText(_translate("MainWindow", "保存日志"))
        self.btn_data_source.setText(_translate("MainWindow", "选择数据源"))

