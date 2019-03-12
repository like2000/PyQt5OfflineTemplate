import sys

from PyQt5 import QtWidgets

from controller_800.f800_widget import F800Widget
from controller_lsa_dummy.lsa_widget import LsaWidget
from controller_rf.rf_widget import RfWidget
from controller_timings.timings_widget import TimingsWidget
from controllers.Controller_200MHz import Controller200
from dummies.lsa_dummy import LsaDummy
from windows.sps_window import SPSWindow


class MainWindow(SPSWindow):

    def __init__(self):
        super().__init__(geometry=(200, 200, 1300, 800))

        self.lsa = LsaDummy()

        lsa_dummy = LsaWidget()
        timing = TimingsWidget()
        self.leftTabWidget.setLayout(QtWidgets.QVBoxLayout())
        self.leftTabWidget.layout().addWidget(lsa_dummy)
        self.leftTabWidget.layout().addWidget(timing)

        # self.create_dummy_selector()
        # self.list.setModel(ContextModel(self.list))
        # self.list.verticalHeader().hide()
        # self.list.horizontalHeader().setStretchLastSection(True)
        # # self.list.updateGeometry()
        # # self.setItemDelegate(CardsView(self))
        #
        # model = self.list.model()
        # # model.data_table.loc[len(model.data_table), :] = ["LHCBCMS_3Inj_Q20_2018_V1", "LHC1", "Operational"]
        # # model.data_table.loc[len(model.data_table), :] = ["LHCBCMS_3Inj_Q20_2018_V1", "LHC1", "Operational"]
        # # model.appendRow(["LHCBCMS_3Inj_Q20_2018_V1", "LHC1", "Operational"])
        # print(model.data_table)
        # # model.appendRow(ContextModel.styled_item(["LHCBCMS_3Inj_Q20_2018_V1", "LHC1", "Operational"]))

        rfbucket = RfWidget(self, 2, 1)
        controller200 = Controller200(self)
        controller800 = F800Widget(self)

        self.centralWidget().setSizes((300, 600))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    sys.exit(app.exec_())
