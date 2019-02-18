import sys

from PyQt5 import QtWidgets

from controllers.Controller_200MHz import Controller200
from controllers.Controller_800MHz import Controller800
from controllers.RFBucket import RFBucket
from dummies.cards_model import CardsModel
from dummies.lsa_dummy import LsaDummy
from sps_window import SPSWindow


class MainWindow(SPSWindow):

    def __init__(self):
        super().__init__(geometry=(200, 200, 1200, 800))

        self.lsa = LsaDummy()

        self.dummy_selector()
        self.list.setModel(CardsModel(self.list))
        # self.list.updateGeometry()
        # self.setItemDelegate(CardsView(self))

        rfbucket = RFBucket(self)
        controller200 = Controller200(self)
        controller800 = Controller800(self)

        # self.data = pd.DataFrame({
        #     'Hallo': [0, 1, 2],
        #     'Du': [2, 3, 4],
        #     'Dort': [4, 5, 6],
        #     'Kevin': [6, 7, 8]
        # })
        # self.model = CardsModel(self.data)
        # self.cards_list = QtWidgets.QListView()
        # self.table_view.setModel(self.model)
        # # self.table_view.horizontalHeader().setVisible(False)
        # self.table_view.horizontalHeader().setStretchLastSection(True)
        # self.table_view.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        # self.table_view.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        # self.table_view.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        # layout = QtWidgets.QHBoxLayout()
        # self.configWidget.setLayout(layout)
        # layout.addWidget(self.table_view)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    sys.exit(app.exec_())
