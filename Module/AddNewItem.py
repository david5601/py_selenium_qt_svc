import sys
from PyQt5.QtWidgets import QApplication, QDialog
from Design.AddNewItemUI import Ui_AddNewItemDialog
from Design import Theme
from Resources import Resources
class AddNewItemDialog(QDialog, Ui_AddNewItemDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setStyleSheet(Theme.load_stylesheet())

        self.btn_accept.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)

    def getNewItemList(self):
        newItemList = []

        if self.checkBox_onoff.isChecked():
            newItemList.append("Yes")
        else:
            newItemList.append("No")

        newItemList.append(self.lineEdit_unit.text())
        newItemList.append(self.lineEdit_terminal.text())
        if self.lineEdit_ip.text() == '...':
            newItemList.append("")
            newItemList.append("")
        else:
            newItemList.append("Go")
            newItemList.append(self.lineEdit_ip.text())
        newItemList.append(self.lineEdit_mac.text())
        newItemList.append(self.lineEdit_switch.text())
        newItemList.append(self.lineEdit_port.text())
        newItemList.append(self.lineEdit_power.text())
        newItemList.append(self.lineEdit_orion.text())
        newItemList.append(self.lineEdit_zabbix.text())

        return newItemList
