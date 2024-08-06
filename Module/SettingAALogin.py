import sys
from PyQt5.QtWidgets import QApplication, QDialog, QLineEdit
from PyQt5.QtCore import Qt
from Design.SettingAALogin import Ui_SettingAALoginDialog
from Design import Theme
from Resources import Resources
class SettingsAALoginDialog(QDialog, Ui_SettingAALoginDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setStyleSheet(Theme.load_stylesheet())

        self.checkBox.setChecked(False)
        self.btn_submit.clicked.connect(self.accept)
        self.checkBox.stateChanged.connect(self.toggleEchoMode)
    
    def toggleEchoMode(self, state):
        if state == Qt.Checked:
            self.lineEdit_password.setEchoMode(QLineEdit.Normal)
        else:
            self.lineEdit_password.setEchoMode(QLineEdit.Password)

    def getLoginInfo(self):
        user = self.lineEdit_aa_login.text()
        password = self.lineEdit_password.text()
        return (user, password)