from PyQt5 import QtWidgets


class Controller800(QtWidgets.QWidget):

    def __init__(self, parent=None):

        super().__init__(parent=parent)

        self.initUi()


    def initUi(self):

        self.parent().tabWidget.addTab(self, "800 MHz")