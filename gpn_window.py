from PyQt5 import QtCore
from PyQt5 import QtWidgets


class GPNWindow(QtWidgets.QMainWindow):

    def __init__(self, title="GPN Qt5 Application", parent=None):

        super().__init__(parent=parent)

        self.init_ui(title)

    def init_ui(self, title):
        pass
