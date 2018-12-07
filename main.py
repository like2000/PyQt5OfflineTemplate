import sys

from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets

from Controllers.Controller_800MHz import Controller800


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):

        super().__init__()

        self.initUi()


    def initUi(self):

        # WINDOW PROPERTIES
        self.setWindowTitle("PyQt5 Offline Blueprint")
        self.setGeometry(100, 100,800, 600)

        # ADD SPLITTER
        splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        self.setCentralWidget(splitter)

        # ADD LAYOUTS TO SPLITTERS
        self.leftSplit = QtWidgets.QWidget()
        splitter.addWidget(self.leftSplit)

        self.tabWidget = QtWidgets.QTabWidget()
        splitter.addWidget(self.tabWidget)


        # ASSEMBLE TABS
        controller800 = Controller800(self)


        splitter.setSizes([200, 600])

        self.show()


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    sys.exit(app.exec_())