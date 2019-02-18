from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets

import pickle
import numpy as np
import pyqtgraph as pg
import matplotlib.pyplot as plt
from pyqtgraph.widgets.MatplotlibWidget import MatplotlibWidget as mpl

from sps_window import SPSWindow
from widgets.japc_line_edit import JapcLineEdit
from widgets.japc_toggle_button import JapcToggleButton


class Controller800(QtWidgets.QTabWidget):

    def __init__(self, parent=None):

        super().__init__(parent=parent)

        self.lsa = self.parent().lsa
        self.initUi()

    def initUi(self):

        self.setTabPosition(QtWidgets.QTabWidget.East)
        # self.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.parent().tabWidget.addTab(self, "800 MHz")

        self.addTab(self.statusTab(), "Status")
        self.addTab(self.functionsTab(), "Functions")
        self.addTab(self.voltageTab(), "Voltages")
        self.addTab(self.combFilterTab(), "Comb Filter")
        self.setCurrentIndex(2)

    def voltageTab(self):
        qwidget = QtWidgets.QWidget()
        layout = QtWidgets.QGridLayout()
        qwidget.setLayout(layout)

        # ASSEMBLE ELEMENTS
        row = -1
        # self.layout.addWidget(QtWidgets.QH)

        row += 1
        layout.addItem(QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed),
                       row, 0)

        row += 1
        grid = plt.GridSpec(2, 2, wspace=0.4, hspace=0.3)

        mw = mpl()
        fig = mw.getFigure()
        ax1 = fig.add_subplot(grid[0, :])
        ax2 = fig.add_subplot(grid[1, 0])
        ax3 = fig.add_subplot(grid[1, 1])
        fig.tight_layout()
        # tb = mw.toolbar
        # tb.
        layout.addWidget(mw, row, 0, 1, 4)

        row += 1
        layout.addItem(QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed),
                       row, 0)

        return qwidget

    def statusTab(self):

        qwidget = QtWidgets.QWidget()
        layout = QtWidgets.QGridLayout()
        qwidget.setLayout(layout)

        # ASSEMBLE ELEMENTS
        row = -1
        # self.layout.addWidget(QtWidgets.QH)

        row += 1
        layout.addItem(QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding), row, 0)

        row += 1
        layout.addWidget(QtWidgets.QLabel("Cavity 1"), row, 1)
        layout.addWidget(QtWidgets.QLabel("Cavity 2"), row, 3)

        row += 1
        layout.addWidget(SPSWindow.h_line(), row, 0, 1, 4)

        row += 1
        self.c1_enable = JapcToggleButton(self.lsa)
        self.c2_enable = JapcToggleButton(self.lsa)
        layout.addWidget(QtWidgets.QLabel("Cavity active", alignment=QtCore.Qt.AlignRight), row, 0)
        layout.addWidget(self.c1_enable, row, 1)
        layout.addWidget(self.c2_enable, row, 3)

        row += 1
        self.c1_vmin = JapcLineEdit(self.lsa)
        self.c2_vmin = JapcLineEdit(self.lsa)
        layout.addWidget(QtWidgets.QLabel("Vmin", alignment=QtCore.Qt.AlignRight), row, 0)
        layout.addWidget(self.c1_vmin, row, 1)
        layout.addWidget(self.c2_vmin, row, 3)

        row += 1
        self.c1_vmax = JapcLineEdit(self.lsa)
        self.c2_vmax = JapcLineEdit(self.lsa)
        layout.addWidget(QtWidgets.QLabel("Vmax", alignment=QtCore.Qt.AlignRight), row, 0)
        layout.addWidget(self.c1_vmax, row, 1)
        layout.addWidget(self.c2_vmax, row, 3)

        row += 1
        self.c1_polarloop = JapcToggleButton(self.lsa, "SPS800.CavityLoop.c1/PolarLoopPPM#Enable")
        self.c2_polarloop = JapcToggleButton(self.lsa, "SPS800.CavityLoop.c2/PolarLoopPPM#Enable")
        layout.addWidget(QtWidgets.QLabel("Polar Loop", alignment=QtCore.Qt.AlignRight), row, 0)
        layout.addWidget(self.c1_polarloop, row, 1)
        layout.addWidget(self.c2_polarloop, row, 3)

        row += 1
        self.c1_cavityloop = JapcToggleButton(self.lsa, "SPS800.CavityLoop.c1/Operation#Enable")
        self.c2_cavityloop = JapcToggleButton(self.lsa, "SPS800.CavityLoop.c2/Operation#Enable")
        layout.addWidget(QtWidgets.QLabel("Cavity Loop", alignment=QtCore.Qt.AlignRight), row, 0)
        layout.addWidget(self.c1_cavityloop, row, 1)
        layout.addWidget(self.c2_cavityloop, row, 3)

        row += 1
        self.c1_otf = JapcToggleButton(self.lsa, "SPS800.CavityLoop.c1/OneTurnFeedbackPPM#Enable")
        self.c2_otf = JapcToggleButton(self.lsa, "SPS800.CavityLoop.c2/OneTurnFeedbackPPM#Enable")
        layout.addWidget(QtWidgets.QLabel("Feedback", alignment=QtCore.Qt.AlignRight), row, 0)
        layout.addWidget(self.c1_otf, row, 1)
        layout.addWidget(self.c2_otf, row, 3)

        row += 1
        self.c1_feedforward = JapcToggleButton(self.lsa, "SPS800.CavityLoop.c1/FeedforwardPPM#Enable")
        self.c2_feedforward = JapcToggleButton(self.lsa, "SPS800.CavityLoop.c2/FeedforwardPPM#Enable")
        layout.addWidget(QtWidgets.QLabel("Feedforward", alignment=QtCore.Qt.AlignRight), row, 0)
        layout.addWidget(self.c1_feedforward, row, 1)
        layout.addWidget(self.c2_feedforward, row, 3)

        row += 1
        layout.addItem(QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding),
                       row, 0)

        # FINALIZE LAYOUT
        layout.setHorizontalSpacing(40)
        layout.setVerticalSpacing(10)
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 1)
        layout.setColumnStretch(2, 1)
        layout.setColumnStretch(3, 1)

        return qwidget

    def functionsTab(self):

        qwidget = QtWidgets.QWidget()
        layout = QtWidgets.QGridLayout()
        qwidget.setLayout(layout)

        # READ SETTINGS
        data = pickle.load(open('settings/lsa_values.pkl', 'rb'), encoding='latin1')
        # with open() as fh:
        print(data.keys())

        # ASSEMBLE ELEMENTS
        row = -1

        x = np.linspace(0, 20*np.pi, 1000)
        y = np.sin(x)

        row += 1
        pw1 = pg.PlotWidget(title="Momentum [GeV/c]")
        ax1 = pg.PlotDataItem(
            data['t_mom'], data['val_mom'], pen=pg.mkPen(color='r', width=2)) #, symbolPen=None, symbolBrush=pg.mkBrush(color='r'), symbolSize=6)
        pw1.addItem(ax1)
        layout.addWidget(pw1, row, 0, 1, 1)

        row += 1
        pw1 = pg.PlotWidget(title="Frequency program - 200 MHz")
        ax1 = pg.PlotDataItem(
            data['t_freq'], data['val_freq'], pen=pg.mkPen(color='y', width=2))
        pw1.addItem(ax1)
        layout.addWidget(pw1, row, 0, 1, 1)

        row += 1
        ww = QtWidgets.QTextEdit()
        layout.addWidget(ww, row, 0, 1, 1)
        # ww.setHtml("""
        # <style> {font-size: 200pt;} </style>
        # <ul>
        # <li> Eta </li>
        # <li> Radial steering as correction </li>
        # <li> Synchrotron frequency </li>
        # </ul>
        # """)
        # ww.setText("""
        # * Eta\n
        # * Radial steering correction\n
        # * Synchrotron frequency""")
        # font = QtGui.QFont('helvetica', 30, QtGui.QFont.Bold)
        # ww.setFont(font)
        # ww.setFontPointSize(80)
        # ww.setMinimumHeight(200)

        # qwidget = pg.PlotWidget(title="Functions")
        # ax1 = pg.PlotDataItem(
        #     x, y, pen=pg.mkPen(color='r', width=2),
        #     symbol='s', symbolPen=None, symbolBrush=pg.mkBrush(color='r'), symbolSize=6)
        # qwidget.addItem(ax1)

        # row += 1
        # layout.addWidget(QtWidgets.QLabel("Cavity 1"), row, 1)
        # layout.addWidget(QtWidgets.QLabel("Cavity 2"), row, 3)
        #
        # row += 1
        # self.c1_enable = JapcToggleButton(self.lsa)
        # self.c2_enable = JapcToggleButton(self.lsa)
        # layout.addWidget(QtWidgets.QLabel("Cavity active", alignment=QtCore.Qt.AlignRight), row, 0)
        # layout.addWidget(self.c1_enable, row, 1)
        # layout.addWidget(self.c2_enable, row, 3)
        #
        # row += 1
        # self.c1_vmin = JapcLineEdit(self.lsa)
        # self.c2_vmin = JapcLineEdit(self.lsa)
        # layout.addWidget(QtWidgets.QLabel("Vmin", alignment=QtCore.Qt.AlignRight), row, 0)
        # layout.addWidget(self.c1_vmin, row, 1)
        # layout.addWidget(self.c2_vmin, row, 3)
        #
        # row += 1
        # self.c1_vmax = JapcLineEdit(self.lsa)
        # self.c2_vmax = JapcLineEdit(self.lsa)
        # layout.addWidget(QtWidgets.QLabel("Vmax", alignment=QtCore.Qt.AlignRight), row, 0)
        # layout.addWidget(self.c1_vmax, row, 1)
        # layout.addWidget(self.c2_vmax, row, 3)
        #
        # row += 1
        # self.c1_polarloop = JapcToggleButton(self.lsa, "SPS800.CavityLoop.c1/PolarLoopPPM#Enable")
        # self.c2_polarloop = JapcToggleButton(self.lsa, "SPS800.CavityLoop.c2/PolarLoopPPM#Enable")
        # layout.addWidget(QtWidgets.QLabel("Polar Loop", alignment=QtCore.Qt.AlignRight), row, 0)
        # layout.addWidget(self.c1_polarloop, row, 1)
        # layout.addWidget(self.c2_polarloop, row, 3)
        #
        # row += 1
        # self.c1_cavityloop = JapcToggleButton(self.lsa, "SPS800.CavityLoop.c1/Operation#Enable")
        # self.c2_cavityloop = JapcToggleButton(self.lsa, "SPS800.CavityLoop.c2/Operation#Enable")
        # layout.addWidget(QtWidgets.QLabel("Cavity Loop", alignment=QtCore.Qt.AlignRight), row, 0)
        # layout.addWidget(self.c1_cavityloop, row, 1)
        # layout.addWidget(self.c2_cavityloop, row, 3)
        #
        # row += 1
        # self.c1_otf = JapcToggleButton(self.lsa, "SPS800.CavityLoop.c1/OneTurnFeedbackPPM#Enable")
        # self.c2_otf = JapcToggleButton(self.lsa, "SPS800.CavityLoop.c2/OneTurnFeedbackPPM#Enable")
        # layout.addWidget(QtWidgets.QLabel("One turn feedback", alignment=QtCore.Qt.AlignRight), row, 0)
        # layout.addWidget(self.c1_otf, row, 1)
        # layout.addWidget(self.c2_otf, row, 3)
        #
        # row += 1
        # self.c1_feedforward = JapcToggleButton(self.lsa, "SPS800.CavityLoop.c1/FeedforwardPPM#Enable")
        # self.c2_feedforward = JapcToggleButton(self.lsa, "SPS800.CavityLoop.c2/FeedforwardPPM#Enable")
        # layout.addWidget(QtWidgets.QLabel("Feedforward", alignment=QtCore.Qt.AlignRight), row, 0)
        # layout.addWidget(self.c1_feedforward, row, 1)
        # layout.addWidget(self.c2_feedforward, row, 3)
        #
        # # FINALIZE LAYOUT
        # layout.setHorizontalSpacing(40)
        # layout.setVerticalSpacing(10)
        # layout.setColumnStretch(0, 1)
        # layout.setColumnStretch(1, 1)
        # layout.setColumnStretch(2, 1)
        # layout.setColumnStretch(3, 1)

        return qwidget

    def combFilterTab(self):

        qwidget = QtWidgets.QWidget()
        layout = QtWidgets.QGridLayout()
        qwidget.setLayout(layout)

        policy = QtWidgets.QSizePolicy.Expanding

        # ASSEMBLE ELEMENTS
        row = -1
        row += 1
        layout.addItem(QtWidgets.QSpacerItem(10, 10, policy, policy),
                       row, 0)

        row += 1
        layout.addWidget(QtWidgets.QLabel(""), row, 0)
        layout.addWidget(QtWidgets.QLabel("Feedback frev"), row, 1)
        layout.addWidget(QtWidgets.QLabel("Feedback 1 x ws"), row, 2)
        layout.addWidget(QtWidgets.QLabel("Feedback 2 x ws"), row, 3)

        # # row += 1
        # # layout.addWidget(self.parent().parent().parent().parent().hLine(), row, 0, 1, 4)

        row += 1
        layout.addWidget(QtWidgets.QLabel("Gain"), row, 0)
        self.feedback_frev_gain = JapcLineEdit(self.lsa, "TWC800_COMB_FREV_GAIN")
        self.feedback_ws1_gain = JapcLineEdit(self.lsa, "TWC800_COMB_SYSB_GAIN")
        self.feedback_ws2_gain = JapcLineEdit(self.lsa, "TWC800_COMB_SYSB2_GAIN")
        layout.addWidget(self.feedback_frev_gain, row, 1)
        layout.addWidget(self.feedback_ws1_gain, row, 2)
        layout.addWidget(self.feedback_ws2_gain, row, 3)

        row += 1
        layout.addWidget(QtWidgets.QLabel("Bandwidth [Hz]"), row, 0)
        self.feedback_frev_bw = JapcLineEdit(self.lsa, "TWC800_COMB_FREV_BW")
        self.feedback_ws1_bw = JapcLineEdit(self.lsa, "TWC800_COMB_SYSB_BW")
        self.feedback_ws2_bw = JapcLineEdit(self.lsa, "TWC800_COMB_SYSB2_BW")
        layout.addWidget(self.feedback_frev_bw, row, 1)
        layout.addWidget(self.feedback_ws1_bw, row, 2)
        layout.addWidget(self.feedback_ws2_bw, row, 3)

        row += 1
        layout.addItem(QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding),
                       row, 0)

        row += 1
        mw = mpl()
        fig = mw.getFigure()
        ax1 = fig.subplots(1, 1)
        fig.tight_layout()
        layout.addWidget(mw, row, 0, 1, 4)

        row += 1
        layout.addItem(QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding),
                       row, 0)

        # FINALIZE LAYOUT
        layout.setHorizontalSpacing(40)
        layout.setVerticalSpacing(10)
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 1)
        layout.setColumnStretch(2, 1)
        layout.setColumnStretch(3, 1)

        return qwidget