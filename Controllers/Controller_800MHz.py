from PyQt5 import QtWidgets

from Widgets.japc_toggle_button import JapcToggleButton


class Controller800(QtWidgets.QWidget):

    def __init__(self, parent=None):

        super().__init__(parent=parent)

        self.lsa = self.parent().lsa
        self.initUi()


    def initUi(self):

        self.parent().tabWidget.addTab(self, "800 MHz")

        self.layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.layout)

        # ASSEMBLE ELEMENTS
        button = JapcToggleButton(self.lsa)
        self.layout.addWidget(button)