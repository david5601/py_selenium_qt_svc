import sys
from PyQt5.QtWidgets import QApplication, QDialog, QLineEdit
from PyQt5.QtCore import Qt
from Design.SettingNDS import Ui_SettingNDS
from Design import Theme
from Resources import Resources
class SettingsNDSDialog(QDialog, Ui_SettingNDS):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setStyleSheet(Theme.load_stylesheet())

        # self.checkBox.setChecked(False)
        self.btn_submit.clicked.connect(self.accept)
        # self.checkBox.stateChanged.connect(self.toggleEchoMode)
    
    # def toggleEchoMode(self, state):
    #     if state == Qt.Checked:
    #         self.lineEdit_password.setEchoMode(QLineEdit.Normal)
    #     else:
    #         self.lineEdit_password.setEchoMode(QLineEdit.Password)

    def getNDSIP(self):
        nds_address = self.lineEdit_nds.text()
        return nds_address