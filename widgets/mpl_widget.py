import matplotlib

matplotlib.use('QT5Agg')
import matplotlib.pyplot as plt

from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

import seaborn as sns

sns.set(context='notebook', style='darkgrid',  # palette='tab10',
        font='serif', font_scale=1, color_codes=True,
        rc={'axes.edgecolor': '0.4',
            'axes.linewidth': 1.5,
            'axes.facecolor': 'whitesmoke',
            'figure.facecolor': 'whitesmoke',
            'figure.edgecolor': 'red',
            'figure.subplot.top': 0.90,  # the top of the subplots of the figure
            'figure.subplot.left': 0.15,  # the left side of the subplots of the figure
            'figure.subplot.right': 0.90,  # the right side of the subplots of the figure
            'figure.subplot.bottom': 0.10,  # the bottom of the subplots of the figure
            'figure.subplot.wspace': 0.20,  # the amount of width reserved for blank space between subplots,
            'figure.subplot.hspace': 0.20,
            'grid.color': '0.8',
            'font.family': 'sans-serif',
            'font.sans-serif': 'helvetica',
            'lines.linewidth': 1.5,
            'lines.markersize': 4,
            'lines.markeredgewidth': 0.1,
            'savefig.transparent': False,
            })


class MplCanvas(Canvas):

    def __init__(self, rows, columns):
        fig, axes = plt.subplots(rows, columns)

        # fig = Figure()
        # ax1 = fig.add_subplot(211)
        # ax2 = fig.add_subplot(212)

        Canvas.__init__(self, fig)
        Canvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        Canvas.updateGeometry(self)


class MplWidget(QtWidgets.QGraphicsView):

    def __init__(self, rows=1, columns=1, nav_bar=True, parent=None):
        QtWidgets.QWidget.__init__(self, parent)  # Inherit from QWidget
        # super(MplWidget, self).__init__(parent)
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        self.canvas = MplCanvas(rows, columns)
        self.navBar = NavigationToolbar(self.canvas, self)
        layout.addWidget(self.canvas)
        if nav_bar:
            layout.addWidget(self.navBar)

        self.fig = self.canvas.figure
        self.axes = self.canvas.figure.axes

        # self.bgcolor = parent.palette().color(QPalette.Window)
        # self.fgcolor = parent.palette().color(QPalette.WindowText)
        # self.fig.set_facecolor((self.bgcolor.red() / 255.0,
        #                         self.bgcolor.green() / 255.0,
        #                         self.bgcolor.blue() / 255.0,
        #                         1.0))

    # self.l1, = self.ax1.plot([0, 1], [0, 1], 'bo-')
    # self.l2, = self.ax2.plot([0, 1], [0, 1], 'ro-')

    #     dynamic_canvas = Canvas(Figure(tight_layout=True))
    #     dynamic_canvas.figure.add_subplot(111)
    #     layout.addWidget(dynamic_canvas)
    #     layout.addWidget(NavigationToolbar(dynamic_canvas, self))
    #     # self.addToolBar(QtCore.Qt.BottomToolBarArea,
    #     #                 NavigationToolbar(dynamic_canvas, self))
    #
    #     self._static_ax = static_canvas.figure.subplots()
    #     t = np.linspace(0, 10, 501)
    #     self._static_ax.plot(t, np.tan(t), ".")
    #
    #     self._dynamic_ax = dynamic_canvas.figure.subplots()
    #     self._timer = dynamic_canvas.new_timer(
    #         100, [(self._update_canvas, (), {})])
    #     self._timer.start()
    #
    # def _update_canvas(self):
    #     self._dynamic_ax.clear()
    #     t = np.linspace(0, 10, 101)
    #     # Shift the sinusoid as a function of time.
    #     self._dynamic_ax.plot(t, np.sin(t + time.time()))
    #     self._dynamic_ax.figure.canvas.draw()
