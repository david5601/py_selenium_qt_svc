from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox, QTableWidget, QTableWidgetItem, QDialog, QFileDialog, QMenu
from PyQt5.QtCore import Qt, QUrl, QPoint
from PyQt5.QtGui import QBrush, QColor, QIcon
from Design.py_massAppQt import Ui_MassRebootApp
from Module.AddNewItem import AddNewItemDialog
from Module.SettingNDS import SettingsNDSDialog
from Module.SettingAALogin import SettingsAALoginDialog
from Module.SettingFortigate import SettingsFortigateDialog
from Module.SettingZabbix import SettingsZabbixDialog
from Module.ItemDelegate import ComboBoxDelegate
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from Design import Theme
from Resources import Resources

import sys
import pandas
import csv
import subprocess
import requests
import time
import pyautogui
import webbrowser
import ctypes

FIRSTLOADING = 1
NEWITEMADDING = 2
ITEMDELETING = 3
ITEMCHANGING = 4


currentState = 1

class DashboardWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MassRebootApp()
        self.ui.setupUi(self)  # This initializes the UI defined in Ui_MassRebootApp

        self.setWindowTitle("SVC Dashboard")
        # self.setWindowIcon(QIcon("Resources/Core/Logo.png"))
        self.setStyleSheet(Theme.load_stylesheet())
        global currentState
        currentState = FIRSTLOADING
        self.aaLogin = ""
        self.aaPassword = ""
        self.fortigateLogin = ""
        self.zabbixOrion = 0
        self.siteID = ""

        delegate = ComboBoxDelegate(['Yes', 'No'], self.ui.tableWidget)
        self.ui.tableWidget.setItemDelegateForColumn(0, delegate)
        
        # if isinstance(delegate, ComboBoxDelegate):
        #     delegate.currentIndexChanged.connect(self.changeItemBackground)

        self.ui.tableWidget.setSortingEnabled(True)
        # self.ui.tableWidget.setSelectionMode(QTableWidget.MultiSelection)
        self.ui.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.tableWidget.customContextMenuRequested.connect(self.showContextMenu)

        self.ui.btn_add.clicked.connect(self.AddTableRow)
        self.ui.btn_delete.clicked.connect(self.DeleteTableRow)
        self.ui.btn_import.clicked.connect(self.LoadNewSite)
        self.ui.btn_save.clicked.connect(self.SaveLoadedSite)
        self.ui.btn_setting.clicked.connect(self.showSettingsDialog)
        self.ui.btn_submit.clicked.connect(self.GetDataUsingKey)
        #Redircect in custom url
        self.ui.tableWidget.cellDoubleClicked.connect(self.clickItemOfRedirect)
        self.ui.tableWidget.itemChanged.connect(self.onItemChanged)

        for row in range(self.ui.tableWidget.rowCount()):
            item = self.ui.tableWidget.item(row, 3)
            if item is not None:
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self,
            'Message',
            'Are you sure you want to quit?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()        
        
    def AddTableRow(self):
        global currentState
        dialog = AddNewItemDialog()
        dialog.setWindowTitle("Add New Item")
        if dialog.exec_() == QDialog.Accepted:
            newItemList = dialog.getNewItemList()
            numRows = self.ui.tableWidget.rowCount()
            self.ui.tableWidget.insertRow(numRows)

            for index in range(0, 11):
                if not index == 9 and not index == 10 and not index == 3:
                    newItem = QTableWidgetItem(newItemList[index])
                    if index == 0 and newItemList[index] == "Yes":
                        newItem.setBackground(QBrush(QColor("green")))
                    newItem.setTextAlignment(Qt.AlignCenter)
                    self.ui.tableWidget.setItem(numRows, index, newItem)
                elif index == 3:
                    newItem = QTableWidgetItem(newItemList[index])
                    newItem.setTextAlignment(Qt.AlignCenter)
                    self.ui.tableWidget.setItem(numRows, index, newItem)
                elif index in [9, 10]:
                    newItem = QTableWidgetItem("View")
                    newItem.setTextAlignment(Qt.AlignCenter)
                    newItem.setData(Qt.UserRole, newItemList[index])
                    self.ui.tableWidget.setItem(numRows, index, newItem)
                else:
                    newItem = QTableWidgetItem("" if newItemList[index] == 'nan' or newItemList[index]=='' else newItemList[index].lower())
                    if not index == 4 and not index == 5:
                        newItem.setTextAlignment(Qt.AlignCenter)
                    self.ui.tableWidget.setItem(numRows, index, newItem)
                    # newItem.setData(Qt.UserRole, newItemList[index])
            if currentState == FIRSTLOADING:
                existingTitle = self.windowTitle()
                self.setWindowTitle(existingTitle + "*")
            currentState = NEWITEMADDING
                
                    
    def clickItemOfRedirect(self, row, col):
        if col == 3:
            ip_address = self.ui.tableWidget.item(row, 4).text()
            if not ip_address == "":
                password = "S3cur3tech0624"
                xpath = r'C:\Program Files\TightVNC\tvnviewer.exe'
                process = subprocess.Popen([xpath])
                time.sleep(1)
                # for character in ip_address:
                #     pyautogui.typewrite(character)
                #     time.sleep(0.2)
                pyautogui.typewrite(ip_address)
                pyautogui.press('enter')
                time.sleep(1)
                pyautogui.typewrite(password)
                pyautogui.press('enter')
                time.sleep(1)
            else:
                QMessageBox.critical(self, "Critical", "Can't get the correct IP. Please check the IP address.")
        elif col == 4:
            ip_address = self.ui.tableWidget.item(row, 4).text()
            if not ip_address == "":
                print(ip_address)
                options = Options()
                options.add_experimental_option("detach", True)

                ip_address = self.ui.tableWidget.item(row, col).text()
                
                driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=options)
                driver.get("http://" + ip_address)

                time.sleep(1)
                username_field = driver.find_element(By.NAME, 'user')
                username_field.srend_keys("admin")

                time.sleep(1)
                password_field = driver.find_element(By.NAME, 'pwd')
                password_field.send_keys("S3cur3admin0324")

                time.sleep(1)
                submit_button = driver.find_element(By.XPATH, "//input[@type='submit']")
                submit_button.click()

                time.sleep(3)
            else:
                QMessageBox.critical(self, "Critical", "Can't get the correct IP. Please check the IP address.")
        
        elif col in [9, 10]:
            link = self.ui.tableWidget.item(row, col).data(Qt.UserRole)
            if not link == "":
                webbrowser.open(link)

    def DeleteTableRow(self):
        global currentState
        numRows = self.ui.tableWidget.rowCount()
        currentRow = self.ui.tableWidget.currentRow()
        if not numRows == 0:
            if not currentRow <= -1:
                self.ui.tableWidget.removeRow(currentRow)
                if currentState == FIRSTLOADING:
                    existingTitle = self.windowTitle()
                    self.setWindowTitle(existingTitle + "*")
                currentState = ITEMDELETING
            else:
                QMessageBox.critical(self, "Critical", "Please select the deleting row.", QMessageBox.Yes)
        else:
            QMessageBox.critical(self, "Critical", "Cannot delete the row in table. Please check the rows.", QMessageBox.Yes)
    
    def onItemChanged(self, item):
        global currentState
        if item.text() == "Yes":
            item.setBackground(QBrush(QColor("green")))
        elif item.text() == "No":
            item.setBackground(QBrush(QColor("#19232D")))
        elif item.column() == 4 and not item.text() == "":
            vncItem = QTableWidgetItem("Go")
            vncItem.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget.setItem(item.row(), 3, vncItem)

        if currentState == FIRSTLOADING:
            existingTitle = self.windowTitle()
            self.setWindowTitle(existingTitle + "*")
            currentState = ITEMCHANGING

            print(f"Changed row: {item.row()}, col: {item.column()} to {item.text()}")
    
    def  putItemInTable(self, df):
        column = ['Include', 'Unit', 'Terminal', 'VNC', 'IP', 'MAC', 'Switch', 'Port', 'Power', 'Orion', 'Zabbix']
        df_list = df.columns.tolist()
        print(df_list)
        for row in range(df.shape[0]):
            self.ui.tableWidget.insertRow(row)
            for col in range(len(column)):
                for idx in range(len(df_list)):
                    if df_list[idx] == column[col]:
                        value = str(df.iat[row, idx])
                        
                        if col in [9, 10]:
                            if value == 'nan' or value=='':
                                newItem = QTableWidgetItem("")
                                newItem.setData(Qt.UserRole, "http:\\localhost" )
                            else:
                                newItem = QTableWidgetItem("View")
                                newItem.setData(Qt.UserRole, value)
                            newItem.setTextAlignment(Qt.AlignCenter)
                            self.ui.tableWidget.setItem(row, col, newItem)
                        # elif col == 3:
                        #     newItem = QTableWidgetItem("Go")
                        #     newItem.setTextAlignment(Qt.AlignCenter)
                        #     self.ui.tableWidget.setItem(row, col, newItem)
                        else:
                            item_text = ""
                            
                            if col == 0 and value=="nan":
                                item_text = "No"
                            elif col == 0 and value != "nan":
                                item_text = value
                            elif not col == 0 and value == "nan" and not col == 3:
                                item_text = ""
                            elif not col == 0 and not value == "nan":
                                item_text = value.lower()

                            item = QTableWidgetItem(item_text)
                            if item_text == "Yes":
                                item.setBackground(QBrush(QColor("green")))
                            if not col == 4 and not col == 5:
                                item.setTextAlignment(Qt.AlignCenter)
                            self.ui.tableWidget.setItem(row, col, item)
                        break
                    elif col == 3:
                        if not 'IP' in df.columns:
                            item = QTableWidgetItem("")
                        else:
                            ip_address = df.at[row, 'IP']
                            if ip_address == "" or ip_address == "nan":
                                item = QTableWidgetItem("Go")
                            else:
                                item = QTableWidgetItem("")
                        item.setTextAlignment(Qt.AlignCenter)
                        self.ui.tableWidget.setItem(row, col, item)
                    elif col == 0:
                        item = QTableWidgetItem("No")
                        item.setTextAlignment(Qt.AlignCenter)
                        self.ui.tableWidget.setItem(row, col, item)

                    elif col in [9, 10]:
                        item = QTableWidgetItem("")
                        item.setData(Qt.UserRole, "http:\\localhost")
                        item.setTextAlignment(Qt.AlignCenter)
                        self.ui.tableWidget.setItem(row, col, item)

    def LoadNewSite(self):
        global currentState
        if not currentState == ITEMCHANGING and not currentState == ITEMDELETING and not currentState == NEWITEMADDING:
            fileName, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Microsoft Office Files (*.csv);;All Files (*)")
            print(fileName)
            if fileName:
                df = pandas.read_csv(fileName)
                print(df)
                # print(fileName.split('/')[-1])
                self.ui.tableWidget.clear()
                self.ui.tableWidget.setRowCount(0)
                
                column = ['Include', 'Unit', 'Terminal', 'VNC', 'IP', 'MAC', 'Switch', 'Port', 'Power', 'Orion', 'Zabbix']
                self.ui.tableWidget.setHorizontalHeaderLabels(column)
                self.putItemInTable(df)

                self.setWindowTitle('SVC Dashboard' + " - " + fileName.split('/')[-1])
                currentState = FIRSTLOADING

                # for row in range(self.ui.tableWidget.rowCount()):
                #     item = self.ui.tableWidget.item(row, 3)
                #     if item is not None:
                #         item.setFlags(item.flags() & ~Qt.ItemIsEditable)
        else:
            QMessageBox.warning(self, "Warning", "Changed the some items of Table. Please save with *.csv file.")

    def SaveLoadedSite(self):
        global currentState
        fileName = ""
        if not currentState == FIRSTLOADING:
            fileName, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Microsoft Office Files (*.csv);;All Files (*)")
            print(fileName, _)

        if fileName:
            with open(fileName, 'w', newline='') as file:
                writer = csv.writer(file)
                # Write headers
                headers = [self.ui.tableWidget.horizontalHeaderItem(col).text() for col in range(self.ui.tableWidget.columnCount())]
                writer.writerow(headers)
                # Write data rows
                for row in range(self.ui.tableWidget.rowCount()):
                    rowData = []
                    for col in range(self.ui.tableWidget.columnCount()):
                        item = self.ui.tableWidget.item(row, col)
                        if col in [9, 10]:
                            if not item.data(Qt.UserRole) == "http:\\localhost":
                                rowData.append(item.data(Qt.UserRole))
                            else:
                                rowData.append("")
                        else:
                            item = self.ui.tableWidget.item(row, col)
                            rowData.append(item.text() if item is not None else "")
                        # if not col in [9, 10]:
                            
                        # else:
                        #     rowData.append(item.data(Qt.UserRole))
                    writer.writerow(rowData)
            existingTitle = self.windowTitle()
            existingTitle = existingTitle[:-1]
            self.setWindowTitle(existingTitle)
            currentState = FIRSTLOADING

    def showContextMenu(self, pos: QPoint):
        contextMenu = QMenu(self)
        switchYesAction = contextMenu.addAction('Yes')
        switchNoAction = contextMenu.addAction('No')

        selected_Items = self.showSelectedRows()
        action = contextMenu.exec_(self.ui.tableWidget.mapToGlobal(pos))
        if(action == switchYesAction):
            for row in selected_Items:
                item = QTableWidgetItem("Yes")
                item.setBackground(QBrush(QColor("green")))
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget.setItem(row, 0, item)
        else:
            for row in selected_Items:
                item = QTableWidgetItem("No")
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget.setItem(row, 0, item)
    
    def showSelectedRows(self):
        selected_Items = self.ui.tableWidget.selectedItems()
        selected_rows = set()

        for item in selected_Items:
            selected_rows.add(item.row())
        
        return sorted(selected_rows)
    
    def showSettingsDialog(self):
        if self.ui.comboBox.currentIndex() in [1, 2]:
            settingsDialog = SettingsAALoginDialog()
            settingsDialog.setWindowTitle("Settings AA Login")
            if settingsDialog.exec_() == QDialog.Accepted:
                self.aaLogin, self.aaPassword = settingsDialog.getLoginInfo()
                # print(self.aaLogin, self.aaPassword)
        elif self.ui.comboBox.currentIndex() == 4:
            settingsNDSDialog = SettingsNDSDialog()
            settingsNDSDialog.setWindowTitle("Setting NDS")
            if settingsNDSDialog.exec_() == QDialog.Accepted:
                self.ndsURL = settingsNDSDialog.getNDSIP()
        elif self.ui.comboBox.currentIndex() == 5:
            settingsFortigate = SettingsFortigateDialog()
            settingsFortigate.setWindowTitle("Setting Fortigate")
            if settingsFortigate.exec_() == QDialog.Accepted:
                self.fortigateLogin = settingsFortigate.getLoginInfo()
        elif self.ui.comboBox.currentIndex() == 6:
            settingZabbix = SettingsZabbixDialog()
            settingZabbix.setWindowTitle("Setting Orion & Zabbix")
            if settingZabbix.exec_() == QDialog.Accepted:
                self.zabbixOrion, self.siteID = settingZabbix.getInformation()
                # print(self.zabbixOrion, self.siteID)
            
    
    def fetch_leases(self, url):
        response = requests.post(url)
        response.raise_for_status()
        print(response.text)  # Check for request errors

        return response.text

    def extract_active_leases(self, data):
        lines = data.split('\n')
        
        active_lease_section = False
        active_leases = []

        for line in lines:
            if "Active leases" in line or "----------------------------------" in line:
                active_lease_section = True
                continue
            if active_lease_section:
                if "Inactive or non-responsive leases" in line:
                    break
                if line.strip():  # Skip empty lines
                    active_leases.append(line.strip())

        return active_leases
    
    def updateUsingTerminal(self, update_list):
        for row in update_list:
            elements = row.split('\t')
            ip_address = elements[2]
            mac_address = elements[1]
            terminal = elements[3]
            for tRow in range(self.ui.tableWidget.rowCount()):
                item = self.ui.tableWidget.item(tRow, 2)
                if item and item.text() == terminal:
                    self.ui.tableWidget.setItem(tRow, 4, QTableWidgetItem(ip_address))
                    self.ui.tableWidget.setItem(tRow, 5, QTableWidgetItem(mac_address))
                    break

    def GetDataUsingKey(self):
        options = Options()
        options.add_experimental_option("detach", True)

        if self.ui.comboBox.currentIndex() == 4:
            ip_address = self.ndsURL
            nds ="http://" + ip_address + "/dnsmasq.leases"
            subprocess.Popen(['start', 'msedge', nds], shell=True)
            try:
                data = self.fetch_leases(nds)
                active_leases = self.extract_active_leases(data)
                self.updateUsingTerminal(active_leases)
                # for lease in active_leases:
                #     print(lease)
            except requests.exceptions.RequestException as e:
                print(f"Error fetching data: {e}")
        elif self.ui.comboBox.currentIndex() == 5:
            if not self.fortigateLogin == "":
                fortigate = "https://" + self.fortigateLogin + "/ng/switchctrl/ports"
                driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=options)
                driver.get(fortigate)
                search_filed = driver.find_element(By.ID, '')
                
                # if not self.ui.tableWidget.rowCount() == 0:
                #     for row in self.ui.tableWidget.rowCount():
                #         item = self.ui.tableWidget.item(row, 3).text()
                #         search_filed.clear()
                #         search_filed.send_keys(item)
                #         search_filed.send_keys(Keys.ENTER)
                #         time.sleep(2)
                #         html_content = driver.page_source
                #         print(html_content)
                #         time.sleep(2)        

                item = self.ui.tableWidget.item(0, 5).text()
                search_filed.clear()
                search_filed.send_keys(item)
                search_filed.send_keys(Keys.ENTER)
                time.sleep(2)
                html_content = driver.page_source
                print(html_content)
                time.sleep(2)

            else:
                QMessageBox.warning(self, "Warning", "You didn't set the Username and Password. Please check the login information.")
            
        elif self.ui.comboBox.currentIndex() == 6:
            if not self.siteID == "":
                options = Options()
                options.add_experimental_option("detach", True)
                orion = ""

                if self.zabbixOrion == 0:
                    orion = "https://at-orionpoll01.corp.securustech.net"
                else:
                    orion = "https://mi-orionpoll01.corp.securustech.net"
                
                driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=options)
                driver.get(orion)
                print(orion)
                user_field = driver.find_element(By.ID, "ctl00_BodyContent_Username")
                user_field.send_keys("CORP\A0015611")
                time.sleep(1)
                pass_field = driver.find_element(By.ID, "ctl00_BodyContent_Password")
                pass_field.send_keys("English1111!")
                time.sleep(1)
                submit_button = driver.find_element(By.ID, "ctl00_BodyContent_LoginButton")
                submit_button.click()
                time.sleep(2)
                orion = orion + "/Orion/NetPerfMon/Resources/NodeSearchResults.aspx?Property=Caption&SearchText=" + self.siteID
                print(orion)
                driver.get(orion)
                
                # login_page = driver.page_source
                # print(login_page)
                links = driver.find_elements(By.XPATH, "//table//tr//td//a")
                # print(links)
                for link in links:
                    href = link.get_attribute('href')
                    print(href)
                    text = link.text
                    print(text)
                    orion_terminal = text.split('_')
                    for row in range(self.ui.tableWidget.rowCount()):
                        item = self.ui.tableWidget.item(row, 2)
                        if not len(orion_terminal) == 1 :
                            if orion_terminal[2] == item.text():
                                # url = "https://at-orionpoll01.corp.securustech.net" + href
                                if href.startswith("http://") or href.startswith("https://"):
                                    url = href
                                else:
                                    url = "https://at-orionpoll01.corp.securustech.net" + href
                                # driver.execute_script(f"window.open('{url}', '_blank');")
                                # driver.switch_to.window(driver.window_handles[-1])
                                # driver.get(url)
                                orion_item = QTableWidgetItem("View")
                                orion_item.setTextAlignment(Qt.AlignCenter)
                                # orion_item.setText("View")
                                orion_item.setData(Qt.UserRole, url)
                                self.ui.tableWidget.setItem(row, 9, orion_item)

                for index in range(self.ui.tableWidget.rowCount()):
                    terminal = self.ui.tableWidget.item(index, 2).text()
                    if not terminal == "":
                        zabbix = "http://10.36.133.173/zabbix/zabbix.php?action=search&search=" + terminal
                        # driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=options)
                        # driver.execute_script("window.open('');")
                        # driver.switch_to.window(driver.window_handles[-1])
                        # driver.get(zabbix)
                        item = QTableWidgetItem("View")
                        item.setTextAlignment(Qt.AlignCenter)
                        item.setData(Qt.UserRole, zabbix)
                        self.ui.tableWidget.setItem(index, 10, item)
                    
                        
            # subprocess.Popen(['start', 'msedge', fortigate], shell=True)
        elif self.ui.comboBox.currentIndex() in [1, 2]:
            addresses = []
            # print(self.ui.comboBox.currentIndex())
            if not self.aaLogin == "":
                for tRow in range(self.ui.tableWidget.rowCount()):
                    item = self.ui.tableWidget.item(tRow, 0)
                    if item.text() == "Yes":
                        address = self.ui.tableWidget.item(tRow, 4).text()
                        # print(address)
                        
                        if self.ui.comboBox.currentIndex() == 1 and not address == "":
                            addresses.append(address)
                            url = "http://" + address # + "/index.php?do=displayTelecorrectionsSettings"
                            print("Reboot Browser")
                            print(url)
                            print(self.aaLogin, self.aaPassword)
                            # subprocess.Popen(['start', 'msedge', url], shell=True)
                            driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=options)
                            driver.get(url)
                            
                            time.sleep(1)
                            username_field = driver.find_element(By.NAME, 'user')
                            username_field.send_keys(self.aaLogin)
                            time.sleep(1)
                            password_field = driver.find_element(By.NAME, 'pwd')
                            password_field.send_keys(self.aaPassword)
                            time.sleep(1)
                            submit_button = driver.find_element(By.XPATH, "//input[@type='submit']")
                            submit_button.click()
                            time.sleep(3)
                            driver.get("http://" + address + "/index.php?do=displayTelecorrectionsSettings")
                            time.sleep(3)
                            restart_button = driver.find_element(By.ID, "restartBrowser")
                            restart_button.click()
                            time.sleep(3)
                            driver.quit()

                        elif self.ui.comboBox.currentIndex() == 2 and not address == "":
                            addresses.append(address)
                            url = "http://" + address # + "/index.php?do=displayTelecorrectionsSettings"
                            print("Reboot Terminal")
                            # print(url)
                            # print(self.aaLogin, self.aaPassword)
                            # subprocess.Popen(['start', 'msedge', url], shell=True)
                            driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=options)
                            driver.get(url)
                            
                            time.sleep(1)
                            username_field = driver.find_element(By.NAME, 'user')
                            username_field.send_keys(self.aaLogin)
                            time.sleep(1)
                            password_field = driver.find_element(By.NAME, 'pwd')
                            password_field.send_keys(self.aaPassword)
                            time.sleep(1)
                            submit_button = driver.find_element(By.XPATH, "//input[@type='submit']")
                            submit_button.click()
                            time.sleep(3)
                            driver.get("http://" + address + "/index.php?do=displayTools")
                            time.sleep(1)
                            reboot_button = driver.find_element(By.ID, "rebootAction")
                            reboot_button.click()
                            time.sleep(2)
                            # WebDriverWait(driver, 10).until(EC.alert_is_present())
                            alert1 = driver.switch_to.alert
                            alert1.accept()
                            time.sleep(1)
                            alert2 = driver.switch_to.alert
                            alert2.accept()
                            time.sleep(3)
                            driver.quit()
            else:
                QMessageBox.warning(self, "Warning", "You didn't set the Username and Password. Please check the login information.")
    def changeItemBackground(self, row, col):
        print("Item Changed")
        item = self.ui.tableWidget.item(row, col)
        if item and item.text() == "Yes":
            item.setBackground(QColor("green"))
        else:
            item.setBackground(QColor(""))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # myappid = 'mycompany.myproduct.subproduct.version'  # Arbitrary string
    # ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    window = DashboardWindow()
    window.show()
    sys.exit(app.exec_())