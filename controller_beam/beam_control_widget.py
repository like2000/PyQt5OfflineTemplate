import pickle

import matplotlib.pyplot as plt
import numpy as np
import pyqtgraph as pg
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from japc_widgets.japc_line_edit import JapcLineEdit
from japc_widgets.japc_toggle_button import JapcToggleButton
from widgets.mpl_widget import MplWidget
from windows.sps_window import SPSWindow


class BcWidget(QTabWidget):

    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)

        self.lsa = self.parent().lsa
        self.initUi()

    def initUi(self):
        self.setTabPosition(QTabWidget.East)
        # self.setTabShape(QTabWidget.Triangular)
        self.parent().rightTabWidget.addTab(self, "Beam control")

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
        mplw = MplWidget(1, 1, nav_bar=False)
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
        layout.addItem(QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Expanding),
                       row, 0)

        row += 1
        layout.addWidget(QLabel("Cavity 1"), row, 1)
        layout.addWidget(QLabel("Cavity 2"), row, 2)

        row += 1
        layout.addWidget(SPSWindow.h_line(), row, 0, 1, 3)

        row += 1
        self.c1_enable = JapcToggleButton(self.lsa)
        self.c2_enable = JapcToggleButton(self.lsa)
        layout.addWidget(QLabel("Cavity active", alignment=Qt.AlignRight), row, 0)
        layout.addWidget(self.c1_enable, row, 1)
        layout.addWidget(self.c2_enable, row, 2)

        row += 1
        self.c1_vmin = JapcLineEdit(self.lsa)
        self.c2_vmin = JapcLineEdit(self.lsa)
        layout.addWidget(QLabel("Vmin", alignment=Qt.AlignRight), row, 0)
        layout.addWidget(self.c1_vmin, row, 1)
        layout.addWidget(self.c2_vmin, row, 2)

        row += 1
        self.c1_vmax = JapcLineEdit(self.lsa)
        self.c2_vmax = JapcLineEdit(self.lsa)
        layout.addWidget(QLabel("Vmax", alignment=Qt.AlignRight), row, 0)
        layout.addWidget(self.c1_vmax, row, 1)
        layout.addWidget(self.c2_vmax, row, 2)

        row += 1
        self.c1_otf = JapcToggleButton(self.lsa, "SPS800.CavityLoop.c1/OneTurnFeedbackPPM#Enable")
        self.c2_otf = JapcToggleButton(self.lsa, "SPS800.CavityLoop.c2/OneTurnFeedbackPPM#Enable")
        layout.addWidget(QLabel("Feedback", alignment=Qt.AlignRight), row, 0)
        layout.addWidget(self.c1_otf, row, 1)
        layout.addWidget(self.c2_otf, row, 2)

        row += 1
        self.c1_polarloop = JapcToggleButton(self.lsa, "SPS800.CavityLoop.c1/PolarLoopPPM#Enable")
        self.c2_polarloop = JapcToggleButton(self.lsa, "SPS800.CavityLoop.c2/PolarLoopPPM#Enable")
        layout.addWidget(QLabel("Polar Loop", alignment=Qt.AlignRight), row, 0)
        layout.addWidget(self.c1_polarloop, row, 1)
        layout.addWidget(self.c2_polarloop, row, 2)

        row += 1
        self.c1_cavityloop = JapcToggleButton(self.lsa, "SPS800.CavityLoop.c1/Operation#Enable")
        self.c2_cavityloop = JapcToggleButton(self.lsa, "SPS800.CavityLoop.c2/Operation#Enable")
        layout.addWidget(QLabel("Cavity Loop", alignment=Qt.AlignRight), row, 0)
        layout.addWidget(self.c1_cavityloop, row, 1)
        layout.addWidget(self.c2_cavityloop, row, 2)

        row += 1
        self.c1_feedforward = JapcToggleButton(self.lsa, "SPS800.CavityLoop.c1/FeedforwardPPM#Enable")
        self.c2_feedforward = JapcToggleButton(self.lsa, "SPS800.CavityLoop.c2/FeedforwardPPM#Enable")
        layout.addWidget(QLabel("Feedforward", alignment=Qt.AlignRight), row, 0)
        layout.addWidget(self.c1_feedforward, row, 1)
        layout.addWidget(self.c2_feedforward, row, 2)

        row += 1
        layout.addItem(QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Expanding),
                       row, 0)

        # FINALIZE LAYOUT
        layout.setHorizontalSpacing(20)
        layout.setVerticalSpacing(10)
        # layout.setColumnStretch(0, 1)
        # layout.setColumnStretch(1, 2)
        # layout.setColumnStretch(2, 1)

        return qwidget
