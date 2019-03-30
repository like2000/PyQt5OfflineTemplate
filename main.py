import sys

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

from controller_200.f200_widget import F200Widget
from controller_800.f800_widget import F800Widget
from controller_beam.beam_control_widget import BcWidget
from controller_lsa_dummy.lsa_widget import LsaWidget
from controller_non_adiabatic.non_adiabatic_widget import NAdiabaticWidget
from controller_rf.rf_widget import RfWidget
from controller_stability.stability_widget import StabilityWidget
from controller_timings.timings_widget import TimingsWidget
from dummies.lsa_dummy import LsaDummy


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.lsa = LsaDummy()

        # Build general
        self.setGeometry(200, 200, 1200, 800)
        self.setWindowTitle("YaRFT - V0.1")
        with open("res/application_stylesheet.qss", "r") as fh:
            self.setStyleSheet(fh.read())

        # Toolbar
        exitAct = QtWidgets.QAction(QtGui.QIcon.fromTheme("window-close"), 'Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.triggered.connect(QtWidgets.qApp.quit)

        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exitAct)

        # Build center area
        self.setCentralWidget(QtWidgets.QTabWidget())

        # Build left dock
        self.lsaDock = QtWidgets.QDockWidget("LSA Selector")
        self.lsaDock.setWidget(QtWidgets.QFrame())
        self.lsaDock.widget().setLayout(QtWidgets.QVBoxLayout())
        self.lsaDock.widget().layout().addWidget(LsaWidget())
        self.lsaDock.widget().layout().addWidget(TimingsWidget())
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.lsaDock)

        # Decorate center area
        beamcontrol = BcWidget(self)
        rfbucket = RfWidget(self, 2, 1)
        controller200 = F200Widget(self)
        controller800 = F800Widget(self)
        processes = NAdiabaticWidget(self)
        stability = StabilityWidget(self)
        self.centralWidget().setCurrentIndex(4)

        self.show()


# class MainWindow(SPSWindow):
#
#     def __init__(self):
#         super().__init__(geometry=(200, 200, 1300, 800))
#
#         self.lsa = LsaDummy()
#
#         lsa_dummy = LsaWidget()
#         timing = TimingsWidget()
#         self.leftTabWidget.setLayout(QtWidgets.QVBoxLayout())
#         self.leftTabWidget.layout().addWidget(lsa_dummy)
#         self.leftTabWidget.layout().addWidget(timing)
#
#         # self.create_dummy_selector()
#         # self.list.setModel(ContextModel(self.list))
#         # self.list.verticalHeader().hide()
#         # self.list.horizontalHeader().setStretchLastSection(True)
#         # # self.list.updateGeometry()
#         # # self.setItemDelegate(CardsView(self))
#         #
#         # model = self.list.model()
#         # # model.data_table.loc[len(model.data_table), :] = ["LHCBCMS_3Inj_Q20_2018_V1", "LHC1", "Operational"]
#         # # model.data_table.loc[len(model.data_table), :] = ["LHCBCMS_3Inj_Q20_2018_V1", "LHC1", "Operational"]
#         # # model.appendRow(["LHCBCMS_3Inj_Q20_2018_V1", "LHC1", "Operational"])
#         # print(model.data_table)
#         # # model.appendRow(ContextModel.styled_item(["LHCBCMS_3Inj_Q20_2018_V1", "LHC1", "Operational"]))
#
#         beamcontrol = BcWidget(self)
#         rfbucket = RfWidget(self, 2, 1)
#         controller200 = F200Widget(self)
#         controller800 = F800Widget(self)
#         processes = NAdiabaticWidget(self)
#         stability = StabilityWidget(self)
#         self.rightTabWidget.setCurrentIndex(4)
#
#         self.centralWidget().setSizes((300, 600))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    sys.exit(app.exec_())
