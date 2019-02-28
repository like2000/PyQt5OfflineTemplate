from PyQt5.QtWidgets import *

from controller_lsa_dummy.lsa_model import LsaModel


class LsaWidget(QFrame):

    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)

        self.initUi()

    def initUi(self):
        self.tableView = QTableView()
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.tableView)

        self.tableView.setShowGrid(False)
        self.tableView.verticalHeader().hide()
        self.tableView.horizontalHeader().hide()
        self.tableView.setSelectionBehavior(QTableView.SelectRows)
        self.tableView.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView.setStyleSheet(
            "QListView {padding: 8;}"
            "QListView::item {margin: 8;}"
            "QListview::item:selected {background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #369, stop:1 #147); color: white;}")

        self.model = LsaModel()
        self.tableView.setModel(self.model)
