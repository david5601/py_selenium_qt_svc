from PyQt5.QtWidgets import QStyledItemDelegate, QComboBox
from PyQt5.QtCore import Qt, pyqtSignal

class ComboBoxDelegate(QStyledItemDelegate):
    # currentIndexChanged = pyqtSignal(int, int)

    def __init__(self, items, parent=None):
        super(ComboBoxDelegate, self).__init__(parent)
        self.items = items
        

    def createEditor(self, parent, option, index):
        combo = QComboBox(parent)
        combo.addItems(self.items)
        # combo.currentIndexChanged.connect(lambda: self.currentIndexChanged.emit(index.row(), index.column()))
        return combo

    def setEditorData(self, editor, index):
        value = index.data(Qt.EditRole)
        editor.setCurrentText(value)

    def setModelData(self, editor, model, index):
        model.setData(index, editor.currentText(), Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)
