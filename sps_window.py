from PyQt5 import QtCore
from PyQt5 import QtWidgets


class SPSWindow(QtWidgets.QMainWindow):

    def __init__(self, title="SPS Qt5 Application", geometry=(200, 200, 900, 600),
                 parent=None):
        super().__init__(parent=parent)

        self.init_ui(title, geometry)

    def init_ui(self, title, geometry):
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
        self.stateWidget = QtWidgets.QWidget()
        splitter.addWidget(self.stateWidget)

        self.tabWidget = QtWidgets.QTabWidget()
        splitter.addWidget(self.tabWidget)

        splitter.setSizes((300, 600))

        self.show()

    def dummy_selector(self):
        """

        :return:
        """
        self.list = QtWidgets.QListView()
        self.list.setStyleSheet(
            "QListView {padding: 8;}"
            "QListView::item {margin: 8;}"
            "QListview::item:selected {background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #369, stop:1 #147); color: white;}")

        self.stateWidget.setLayout(QtWidgets.QVBoxLayout())
        self.stateWidget.layout().addWidget(self.list)

    @staticmethod
    def h_line():
        line = QtWidgets.QFrame()
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)
        return line
