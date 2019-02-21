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

        self.model = LsaModel()
        self.tableView.setModel(self.model)
