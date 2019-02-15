import sys

from PyQt5 import QtWidgets

from sps_window import SPSWindow
from dummies.lsa_dummy import LsaDummy
from controllers.RFBucket import RFBucket
from controllers.Controller_200MHz import Controller200
from controllers.Controller_800MHz import Controller800


class MainWindow(SPSWindow):

    def __init__(self):

        super().__init__(geometry=(200, 200, 1200, 800))

        self.lsa = LsaDummy()
        rfbucket = RFBucket(self)
        controller200 = Controller200(self)
        controller800 = Controller800(self)

if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    sys.exit(app.exec_())