import pickle

import numpy as np
import pyqtgraph as pg
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from scipy.constants import pi
from scipy.interpolate import interp1d

from controller_rf.rf_bucket import RfBucket
from widgets.mpl_widget import MplWidget


class RfWidget(QTabWidget):

    def __init__(self, parent: QWidget = None, rows: int = 1, cols: int = 1) -> None:
        super().__init__(parent=parent)

        self.rf_bucket = RfBucket(C=6911, gamma_tr=18, p0=26e9)
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
        t_mom, val_mom = data['t_mom'], data['val_mom']

        # Top plot
        # ========
        interp = interp1d(data['t_mom'], data['val_mom'] * 1e9)
        momentum = interp
        interp = interp1d(data['t_volt'], data['val_volt'] * 1e6)
        voltage = interp

        tt = np.linspace(t_mom.min(), t_mom.max(), 500)
        val = momentum(tt)
        mplw.axes[0].plot(tt, val)
        marker = mplw.axes[0].axvline(0, c='k', lw=1)

        # Bottom plot
        # ===========
        self.rf_bucket.V = 4.5e6
        self.rf_bucket.h = 4620
        self.rf_bucket.phi = 0
        self.rf_bucket.phi_s = 0
        xx = np.linspace(-pi, pi, 200)
        yy = np.linspace(-self.rf_bucket.dp(xx).max() * 1.1, self.rf_bucket.dp(xx).max() * 1.1)
        XX, YY = np.meshgrid(xx, yy)
        conts = [mplw.axes[1].contourf(XX, YY, self.rf_bucket.H(XX, YY), levels=20, cmap='YlGnBu', alpha=0.8)]
        lines = mplw.axes[1].plot(xx, -self.rf_bucket.dp(xx),
                                  xx, +self.rf_bucket.dp(xx), c='purple', lw=2)
        # mplw.axes[1].set_ylim(-self.rf_bucket.dp(xx).max()*1.1, self.rf_bucket.dp(xx).max()*1.1)

        # Slider
        # ======
        def update(pos):
            marker.set_xdata(pos)

            self.rf_bucket.p0 = momentum(pos)
            self.rf_bucket.V = voltage(pos)
            lines[0].set_ydata(-self.rf_bucket.dp(xx))
            lines[1].set_ydata(+self.rf_bucket.dp(xx))
            for tp in conts[0].collections:
                tp.remove()
            conts[0] = mplw.axes[1].contourf(XX, YY, self.rf_bucket.H(XX, YY), levels=20, cmap='YlGnBu', alpha=0.8)
            # conts.set_data(XX, YY, self.rf_bucket.H(XX, YY))
            # mplw.axes[1].cla()
            # yy = np.linspace(-self.rf_bucket.dp(xx).max() * 1.1, self.rf_bucket.dp(xx).max() * 1.1)
            # XX, YY = np.meshgrid(xx, yy)
            # conts = mplw.axes[1].contourf(XX, YY, self.rf_bucket.H(XX, YY), levels=20, cmap='YlGnBu')
            # lines = mplw.axes[1].plot(xx, -self.rf_bucket.dp(xx),
            #                           xx, +self.rf_bucket.dp(xx), c='purple', lw=2)

            mplw.fig.canvas.draw()
            mplw.fig.canvas.flush_events()

        slider = QSlider(Qt.Horizontal)
        slider.setSingleStep(1000)
        slider.setTickPosition(QSlider.TicksBothSides)
        slider.setRange(data['t_mom'].min(), data['t_mom'].max())
        slider.sliderMoved.connect(lambda pos: update(pos))
        qwidget.addWidget(slider)

        return qwidget

    def getPlots(self):
        pass

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

        return qwidget
