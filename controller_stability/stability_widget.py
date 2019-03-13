import matplotlib.pyplot as plt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from japc_widgets.japc_toggle_button import JapcToggleButton
from widgets.mpl_widget import MplWidget
from windows.sps_window import SPSWindow


class StabilityWidget(QTabWidget):

    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)

        self.lsa = self.parent().lsa
        self.initUi()

    def initUi(self):
        self.setTabPosition(QTabWidget.East)
        # self.setTabShape(QTabWidget.Triangular)
        self.parent().rightTabWidget.addTab(self, "Beam stabilization")

        self.addTab(self.statusTab(), "Status")
        self.addTab(self.voltageTab(), "Voltages")
        self.setCurrentIndex(0)

    def voltageTab(self):
        qwidget = QWidget()
        layout = QGridLayout()
        qwidget.setLayout(layout)

        # ASSEMBLE ELEMENTS
        row = -1
        # self.layout.addWidget(QH)

        row += 1
        layout.addItem(QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Fixed),
                       row, 0)

        row += 1
        mplw = MplWidget(1, 1, nav_bar=False, sharex=True)
        mplw.fig.clf()
        grid = plt.GridSpec(2, 2, wspace=0.4, hspace=0.3)
        ax1 = mplw.fig.add_subplot(grid[0, :])
        ax2 = mplw.fig.add_subplot(grid[1, 0])
        ax3 = mplw.fig.add_subplot(grid[1, 1])
        mplw.fig.tight_layout()
        layout.addWidget(mplw, row, 0, 1, 4)

        row += 1
        layout.addItem(QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Fixed),
                       row, 0)

        return qwidget

    def statusTab(self):
        qwidget = QWidget()
        layout = QGridLayout()
        qwidget.setLayout(layout)

        # ASSEMBLE ELEMENTS
        row = -1
        # self.layout.addWidget(QH)

        row += 1
        label = QLabel("Beam Control Status", alignment=Qt.AlignHCenter)
        label.setStyleSheet("""font-size: 20px;""")
        layout.addWidget(label, row, 0, 1, 4)

        row += 1
        layout.addItem(QSpacerItem(10, 20, QSizePolicy.Expanding, QSizePolicy.Fixed), row, 0)

        row += 1
        layout.addWidget(QLabel("Enable"), row, 1)
        layout.addWidget(QLabel("Start trigger"), row, 2)
        layout.addWidget(QLabel("Stop trigger"), row, 3)

        row += 1
        layout.addWidget(SPSWindow.h_line(), row, 0, 1, 4)

        row += 1
        layout.addWidget(QLabel("200 MHz RF Control", alignment=Qt.AlignRight | Qt.AlignVCenter), row, 0)
        layout.addWidget(JapcToggleButton(self.lsa), row, 1)
        select = QComboBox()
        select.addItems([f"{(i+1)*1000 + 15}" for i in range(8)])
        layout.addWidget(select, row, 2)
        select = QComboBox()
        select.addItems([f"{(i+1)*2000 + 15}" for i in range(8)])
        layout.addWidget(select, row, 3)

        row += 1
        layout.addWidget(QLabel("Phase Loop Control", alignment=Qt.AlignRight | Qt.AlignVCenter), row, 0)
        layout.addWidget(JapcToggleButton(self.lsa), row, 1)
        layout.addWidget(QComboBox(), row, 2)
        layout.addWidget(QComboBox(), row, 3)

        row += 1
        layout.addWidget(QLabel("Synchro Loop Control", alignment=Qt.AlignRight | Qt.AlignVCenter), row, 0)
        layout.addWidget(JapcToggleButton(self.lsa), row, 1)
        layout.addWidget(QComboBox(), row, 2)
        layout.addWidget(QComboBox(), row, 3)

        row += 1
        layout.addWidget(QLabel("Radial Loop Control", alignment=Qt.AlignRight | Qt.AlignVCenter), row, 0)
        layout.addWidget(JapcToggleButton(self.lsa), row, 1)
        layout.addWidget(QComboBox(), row, 2)
        layout.addWidget(QComboBox(), row, 3)

        row += 1
        layout.addWidget(QLabel("Longitudinal Damper Control", alignment=Qt.AlignRight | Qt.AlignVCenter), row, 0)
        layout.addWidget(JapcToggleButton(self.lsa), row, 1)
        layout.addWidget(QComboBox(), row, 2)
        layout.addWidget(QComboBox(), row, 3)

        row += 1
        layout.addWidget(SPSWindow.h_line(), row, 0, 1, 4)

        row += 1
        layout.addItem(QSpacerItem(10, 20, QSizePolicy.Expanding, QSizePolicy.Expanding), row, 0)

        row += 1
        label = QLabel("Filling Pattern Control", alignment=Qt.AlignHCenter)
        label.setStyleSheet("""font-size: 20px;""")
        layout.addWidget(label, row, 0, 1, 4)

        row += 1
        layout.addItem(QSpacerItem(10, 20, QSizePolicy.Expanding, QSizePolicy.Fixed), row, 0)

        row += 1
        layout.addWidget(SPSWindow.h_line(), row, 0, 1, 4)

        row += 1
        select = QComboBox()
        select.addItems([f"{i+1}" for i in range (4)])
        layout.addWidget(QLabel("Number of injections"), row, 0)
        layout.addWidget(select, row, 1)

        row += 1
        select = QComboBox()
        select.addItems([f"{72}" for i in range (4)])
        layout.addWidget(QLabel("Bunches per injection"), row, 0)
        layout.addWidget(select, row, 1)

        row += 1
        layout.addWidget(QLabel("Filling scheme"), row, 0)
        select = QComboBox()
        select.addItems(["25NS", "50NS", "5NS", "8b4e"])
        layout.addWidget(QLabel("Filling pattern"), row, 0)
        layout.addWidget(select, row, 1)

        row += 1
        layout.addItem(QSpacerItem(10, 20, QSizePolicy.Expanding, QSizePolicy.Fixed), row, 0)

        # row += 1
        # self.c1_enable = JapcToggleButton(self.lsa)
        # self.c2_enable = JapcToggleButton(self.lsa)
        # layout.addWidget(QLabel("Cavity active", alignment=Qt.AlignRight), row, 0)
        # layout.addWidget(self.c1_enable, row, 1)
        # layout.addWidget(self.c2_enable, row, 2)
        #
        # row += 1
        # self.c1_vmin = JapcLineEdit(self.lsa)
        # self.c2_vmin = JapcLineEdit(self.lsa)
        # layout.addWidget(QLabel("Vmin", alignment=Qt.AlignRight), row, 0)
        # layout.addWidget(self.c1_vmin, row, 1)
        # layout.addWidget(self.c2_vmin, row, 2)
        #
        # row += 1
        # self.c1_vmax = JapcLineEdit(self.lsa)
        # self.c2_vmax = JapcLineEdit(self.lsa)
        # layout.addWidget(QLabel("Vmax", alignment=Qt.AlignRight), row, 0)
        # layout.addWidget(self.c1_vmax, row, 1)
        # layout.addWidget(self.c2_vmax, row, 2)
        #
        # row += 1
        # self.c1_otf = JapcToggleButton(self.lsa, "SPS800.CavityLoop.c1/OneTurnFeedbackPPM#Enable")
        # self.c2_otf = JapcToggleButton(self.lsa, "SPS800.CavityLoop.c2/OneTurnFeedbackPPM#Enable")
        # layout.addWidget(QLabel("Feedback", alignment=Qt.AlignRight), row, 0)
        # layout.addWidget(self.c1_otf, row, 1)
        # layout.addWidget(self.c2_otf, row, 2)
        #
        # row += 1
        # self.c1_polarloop = JapcToggleButton(self.lsa, "SPS800.CavityLoop.c1/PolarLoopPPM#Enable")
        # self.c2_polarloop = JapcToggleButton(self.lsa, "SPS800.CavityLoop.c2/PolarLoopPPM#Enable")
        # layout.addWidget(QLabel("Polar Loop", alignment=Qt.AlignRight), row, 0)
        # layout.addWidget(self.c1_polarloop, row, 1)
        # layout.addWidget(self.c2_polarloop, row, 2)

        row += 1
        layout.addItem(QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Expanding),
                       row, 0)

        # FINALIZE LAYOUT
        layout.setHorizontalSpacing(20)
        layout.setVerticalSpacing(10)
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 1)
        layout.setColumnStretch(2, 1)
        layout.setColumnStretch(3, 1)

        return qwidget
