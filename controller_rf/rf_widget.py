import pickle

import numpy as np
import pyqtgraph as pg
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from scipy.interpolate import interp1d

from widgets.mpl_widget import MplWidget


class RfWidget(QTabWidget):

    def __init__(self, parent: QWidget = None, rows: int = 1, cols: int = 1) -> None:
        super().__init__(parent=parent)

        self.lsa = self.parent().lsa
        self.rows = rows
        self.cols = cols
        self.initUi()

    def initUi(self):
        self.setTabPosition(QTabWidget.East)
        # self.setTabShape(QTabWidget.Triangular)
        self.parent().rightTabWidget.addTab(self, "RF Bucket")

        self.addTab(self.statusTab(), "Status")
        # self.addTab(self.functionsTab(), "Functions")
        # self.setCurrentIndex(2)

    def statusTab(self):
        qwidget = QSplitter(Qt.Vertical)

        mplw = MplWidget(self.rows, self.cols)
        qwidget.addWidget(mplw)

        # READ SETTINGS
        with open('settings/lsa_values.pkl', 'rb') as fh:
            data = pickle.load(fh, encoding='latin1')

        interp = interp1d(data['t_mom'], data['val_mom'] * 1e9)
        momentum = interp
        tt = np.linspace(data['t_mom'].min(), data['t_mom'].max(),500)
        val = momentum(tt)
        mplw.axes[0].plot(tt, val)

        qwidget.addWidget(QSlider(Qt.Horizontal))

        return qwidget

    def functionsTab(self):
        qwidget = QWidget()
        layout = QGridLayout()
        qwidget.setLayout(layout)

        # READ SETTINGS
        data = pickle.load(open('settings/lsa_values.pkl', 'rb'), encoding='latin1')
        # with open() as fh:
        print(data.keys())

        # ASSEMBLE ELEMENTS
        row = -1

        x = np.linspace(0, 20 * np.pi, 1000)
        y = np.sin(x)

        row += 1
        pw1 = pg.PlotWidget(title="Momentum [GeV/c]")
        ax1 = pg.PlotDataItem(
            data['t_mom'], data['val_mom'],
            pen=pg.mkPen(color='r', width=2))  # , symbolPen=None, symbolBrush=pg.mkBrush(color='r'), symbolSize=6)
        pw1.addItem(ax1)
        layout.addWidget(pw1, row, 0, 1, 1)

        row += 1
        pw1 = pg.PlotWidget(title="Frequency program - 200 MHz")
        ax1 = pg.PlotDataItem(
            data['t_freq'], data['val_freq'], pen=pg.mkPen(color='y', width=2))
        pw1.addItem(ax1)
        layout.addWidget(pw1, row, 0, 1, 1)

        row += 1
        ww = QTextEdit()
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

        return qwidget
