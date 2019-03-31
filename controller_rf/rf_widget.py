import pickle
import time

import matplotlib.pyplot as plt
import numpy as np
import pyqtgraph as pg
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from scipy.constants import c, e, m_p
from scipy.constants import pi
from scipy.interpolate import interp1d

from controller_rf.new_rf_bucket import RfBucket
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
        self.parent().centralWidget().addTab(self, "RF Bucket")

        self.addTab(self.statusTab(), "Status")
        # self.addTab(self.functionsTab(), "Functions")
        # self.setCurrentIndex(2)

    def statusTab(self):
        qwidget = QFrame()
        qwidget.setLayout(QVBoxLayout())

        # READ SETTINGS
        # =============
        with open('settings/lsa_values.pkl', 'rb') as fh:
            data = pickle.load(fh, encoding='latin1')
        t_mom, val_mom = data['t_mom'], data['val_mom']
        t0 = 0  # 1.015

        interp = interp1d(data['t_mom'] - t0, data['val_mom'] * 1e9)
        momentum = interp
        interp = interp1d(data['t_volt'] - t0, data['val_volt'] * 1e6)
        voltage = interp
        interp = interp1d(data['t_BDot'] - t0, data['val_BDot'])
        bdot = interp
        interp = interp1d(data['t_BA'], data['val_BA'])
        BA = interp

        mass = m_p * c ** 2 / e

        def eta(time):
            p0 = momentum(time)
            gamma = np.sqrt(1 + (p0 / mass) ** 2)
            return 18. ** -2 - gamma ** -2

        # RF Bucket
        # =========
        self.rf_bucket = RfBucket(momentum=momentum, bdot=bdot, voltage=voltage, eta=eta, ratio=0.0)

        # Top plot
        # ========
        tt = np.linspace(t_mom.min(), t_mom.max(), 40)
        area = [self.rf_bucket.update_parameters(t).get_emittance() for t in tt]

        mplw_top = MplWidget(2, 2, nav_bar=False)
        mplw_top.fig.tight_layout()
        qwidget.layout().addWidget(mplw_top)

        mplw_top.axes[0].plot(tt, momentum(tt) * 1e-9)
        mplw_top.axes[1].plot(tt, voltage(tt) * 1e-6)
        mplw_top.axes[2].plot(tt, bdot(tt))
        mplw_top.axes[3].plot(tt, BA(tt), c='orange')
        mplw_top.axes[3].plot(tt, area)
        mplw_top.axes[0].set_ylabel("Momentum [GeV/c]")
        mplw_top.axes[1].set_ylabel("Voltage [MV]")
        mplw_top.axes[2].set_ylabel("BDot [?]")
        mplw_top.axes[3].set_ylabel("Bucket area [eV s]")
        marker = [ax.axvline(0, c='k', lw=1) for ax in mplw_top.axes]

        # Bottom plot
        # ===========
        mplw = MplWidget(1, 1)
        qwidget.layout().addWidget(mplw)

        mplw.axes[0].set_facecolor(plt.cm.YlGnBu(256))
        mplw.axes[0].patch.set_alpha(0.4)

        sampling = 200
        xx = np.linspace(-pi, pi, sampling)
        yy = np.linspace(-self.rf_bucket.dp(xx).max() * 1.1, self.rf_bucket.dp(xx).max() * 1.1, sampling)
        XX, YY = np.meshgrid(xx, yy)
        conts = [mplw.axes[0].contourf(XX, YY, np.log(np.abs(self.rf_bucket.H(XX, YY))), levels=20, cmap='YlGnBu',
                                       alpha=0.8)]
        equil = [
            mplw.axes[0].contour(XX, YY, self.rf_bucket.H(XX, YY) - self.rf_bucket.H(pi, 0), levels=[0], cmap='YlGnBu',
                                 alpha=0.8)]

        # lines = mplw.axes[0].plot(xx, -self.rf_bucket.dp(xx),
        #                           xx, +self.rf_bucket.dp(xx), c='purple', lw=2)

        # Slider
        # ======
        def update(pos):
            [m.set_xdata(pos) for m in marker]

            self.rf_bucket.update_parameters(pos)

            yy = np.linspace(-self.rf_bucket.dp(xx).max() * 1.1, self.rf_bucket.dp(xx).max() * 1.1, sampling)
            XX, YY = np.meshgrid(xx, yy)
            mplw.axes[0].set_ylim(yy[0], yy[-1])

            # lines[0].set_ydata(np.ma.masked_equal(-self.rf_bucket.dp(xx), 0))
            # lines[1].set_ydata(np.ma.masked_equal(+self.rf_bucket.dp(xx), 0))
            for tp in conts[0].collections + equil[0].collections:
                tp.remove()
            conts[0] = mplw.axes[0].contourf(XX, YY, np.log(np.abs(self.rf_bucket.H(XX, YY))), levels=20, cmap='YlGnBu',
                                             alpha=0.8)
            equil[0] = mplw.axes[0].contour(XX, YY, self.rf_bucket.H(XX, YY) - self.rf_bucket.H(pi, 0), levels=[0],
                                            cmap='YlGnBu', alpha=0.8)

            for mw in [mplw_top, mplw]:
                # mw.axes[1].relim()
                # mw.axes[1].autoscale_view(True, True, True)
                mw.fig.canvas.draw()
                mw.fig.canvas.flush_events()
                mw.fig.canvas.draw()
                mw.fig.canvas.flush_events()

        slider = QSlider(Qt.Horizontal)
        slider.setRange(0, 100)
        slider.setTickPosition(QSlider.TicksBothSides)
        # slider.setRange(data['t_mom'].min(), data['t_mom'].max())
        slider.sliderMoved.connect(lambda pos: update(pos * data['t_mom'].max() / 100))
        slider.valueChanged.connect(lambda pos: update(pos * data['t_mom'].max() / 100))
        qwidget.layout().addWidget(slider)

        # Button
        # ======
        def play():
            for i in range(0, 100, 2):
                slider.setValue(i)
                time.sleep(0.05)
                print(i)

        startButton = QPushButton("Play")
        qwidget.layout().addWidget(startButton)
        startButton.clicked.connect(play)

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
