import sys

from PyQt5 import QtWidgets

from controllers.Controller_200MHz import Controller200
from controllers.Controller_800MHz import Controller800
from controllers.RFBucket import RFBucket
from dummies.cards_model import CardsModel
from dummies.context_model import ContextModel
from dummies.lsa_dummy import LsaDummy
from sps_window import SPSWindow


class MainWindow(SPSWindow):

    def __init__(self):
        super().__init__(geometry=(200, 200, 1200, 800))

        self.lsa = LsaDummy()

        self.dummy_selector()
        model = ContextModel(self.list)
        # model.appendRow(ContextModel.styled_item("LHC1"))
        self.list.setModel(model)
        self.list.horizontalHeader().setStretchLastSection(True)
        # self.list.updateGeometry()
        # self.setItemDelegate(CardsView(self))

        rfbucket = RFBucket(self)
        controller200 = Controller200(self)
        controller800 = Controller800(self)

        self.centralWidget().setSizes((220, 600))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    sys.exit(app.exec_())
