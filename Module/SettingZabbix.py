import sys
from PyQt5.QtWidgets import QApplication, QDialog, QLineEdit
from PyQt5.QtCore import Qt
from Design.SettingZabbix import Ui_SettingZabbixDialog
from Design import Theme
from Resources import Resources
class SettingsZabbixDialog(QDialog, Ui_SettingZabbixDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setStyleSheet(Theme.load_stylesheet())

        self.btn_submit.clicked.connect(self.accept)

    def getInformation(self):
        index = self.comboBox.currentIndex()
        siteID = self.lineEdit_siteID.text()
    
        return (index, siteID)