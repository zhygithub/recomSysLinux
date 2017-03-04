from PyQt5 import QtWidgets,QtCore
from ui.mainUI import Ui_MainWindow
from usercf import UserBasedCF
from itemcf import ItemBasedCF
import os
import time


class taskThread(QtCore.QThread):
    workSignal = QtCore.pyqtSignal(str)
    workEndSignal = QtCore.pyqtSignal()



    def __init__(self,file_name, user_count, item_count, way_index, parent=None):
        super(taskThread, self).__init__(parent)
        self.user_count = user_count
        self.item_count = item_count
        self.file_name = file_name
        self.way_index = way_index

    def run(self):
        if self.way_index == 1:
            UserCF = UserBasedCF(int(self.user_count), int(self.item_count), self.workSignal)
            UserCF.generate_data_set(self.file_name)
            UserCF.calc_user_sim()
            UserCF.evaluate()
        elif self.way_index == 0:
            ItemCF = ItemBasedCF(int(self.user_count), int(self.item_count), self.workSignal)
            ItemCF.generate_data_set(self.file_name)
            ItemCF.calc_item_sim()
            ItemCF.evaluate()

        self.workEndSignal.emit()


class MainPanel(QtWidgets.QWidget,Ui_MainWindow):

    file_name = ''
    sign_running = False

    content = str()
    lase_content = ""

    ways = ["ItemCF","UserCF"]

    now_way_index = 0
    last_way_index = 0

    def __init__(self):
        super(MainPanel,self).__init__()
        self.setupUi(self)
        self.btn_data_source.clicked.connect(self.select_data)
        self.btn_run.clicked.connect(self.run)
        self.btn_save.clicked.connect(self.save)
        self.cb_way.addItems(self.ways)
        self.cb_way.currentIndexChanged.connect(self.ways_change)


    def ways_change(self, index):
        self.now_way_index = index


    def select_data(self):
        if self.sign_running:
            # 提示
            self.info("有任务正在运行，请等待")

        else :
            self.file_name, filetype = QtWidgets.QFileDialog.getOpenFileName(self,
                                                                             "选取文件",
                                                                             "C:/",
                                                                             "All Files (*);;Text Files (*.txt)")
    def run(self):
        if self.sign_running:
            # 提示
            self.info("有任务正在运行，请等待")

        else:
            if self.file_name == '':
                print("please select data source")
            elif os.path.exists(self.file_name):
                user_count = self.edt_user_count.text()
                item_count = self.edt_item_count.text()
                if user_count.isdigit() and item_count.isdigit():
                    self.content = ''
                    self.task = taskThread(self.file_name, int(user_count), int(item_count), self.now_way_index)
                    self.task.workSignal.connect(self.printResult)
                    self.task.workEndSignal.connect(self.workEnd)
                    self.task.start()
                    self.btn_run.setText("运行中...")
                    self.btn_run.setEnabled(False)
                    self.cb_way.setEnabled(False)
                    self.sign_running = True
                else:
                    print("请以数字的格式输入相似用户数和推荐物品数")

            else:
                print("没有那个文件或目录:" + self.file_name)

    def info(self, info):
        QtWidgets.QMessageBox.information(self,  # 使用infomation信息框
                                "温馨提示",
                                info,
                                          QtWidgets.QMessageBox.Yes)

    def save(self):
        if self.sign_running:
            # 提示
            self.info("有任务正在运行，请等待")

        else:
            ISFORMAT = "%Y-%m-%d_%H:%M:%S"
            timeName = time.strftime(ISFORMAT, time.localtime())
            data_name =self.ways[self.last_way_index] +"_"+  timeName + ".txt"

            pwd = os.getcwd()
            pwd = pwd[0:-2]
            with open(pwd + "log/" + data_name, "wt") as file:
                file.write(self.content)


    def printResult(self,text):
        self.content = self.content + "\n" + text
        self.tb_result_show.append(text)
        print(text)

    def workEnd(self):
        self.last_way_index = self.now_way_index
        self.cb_way.setEnabled(True)
        self.sign_running = False
        self.btn_run.setText("运行")
        self.btn_run.setEnabled(True)


if __name__ == "__main__":
    import sys

    app=QtWidgets.QApplication(sys.argv)
    myshow=MainPanel()
    myshow.show()
    sys.exit(app.exec_())