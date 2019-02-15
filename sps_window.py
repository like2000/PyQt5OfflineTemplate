from PyQt5 import QtCore
from PyQt5 import QtWidgets


class SPSWindow(QtWidgets.QMainWindow):

    def __init__(self, title="SPS Qt5 Application", geometry=(200, 200, 900, 600),
                 parent=None):
        super().__init__(parent=parent)

        self.initUi(title, geometry)

    def initUi(self, title, geometry):
        """

        :param title:
        :param geometry:
        :return:
        """
        # WINDOW PROPERTIES
        self.setWindowTitle(title)
        self.setGeometry(*geometry)
        with open("res/application_stylesheet.qss", "r") as fh:
            self.setStyleSheet(fh.read())

        # ADD SPLITTER
        splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        self.setCentralWidget(splitter)

        # ADD SUBWIDGETS
        self.configWidget = QtWidgets.QWidget()
        splitter.addWidget(self.configWidget)

        self.tabWidget = QtWidgets.QTabWidget()
        splitter.addWidget(self.tabWidget)

        splitter.setSizes([250, 600])

        self.show()

    def dummySelector(self):
        """

        :return:
        """
        list = QtWidgets.QListView

    def hLine(self):
        line = QtWidgets.QFrame()
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)
        return line
