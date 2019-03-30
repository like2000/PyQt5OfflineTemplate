import matplotlib.pyplot as plt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from japc_widgets.japc_line_edit import JapcLineEdit
from japc_widgets.japc_toggle_button import JapcToggleButton
from widgets.mpl_widget import MplWidget
from windows.sps_window import SPSWindow


class NAdiabaticWidget(QTabWidget):

    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)

        self.lsa = self.parent().lsa
        self.initUi()

    def initUi(self):
        self.setTabPosition(QTabWidget.East)
        # self.setTabShape(QTabWidget.Triangular)
        self.parent().centralWidget().addTab(self, "Non-adiabatic processes")

        self.addTab(self.rotationTab(), "Bunch rotation")
        self.addTab(self.debunchingTab(), "Debunching")
        self.addTab(self.transitionTab(), "Transition")
        self.setCurrentIndex(0)

    def debunchingTab(self):
        qwidget = QWidget()

        return qwidget

    def transitionTab(self):
        qwidget = QWidget()

        return qwidget

    def rotationTab(self):
        qwidget = QWidget()
        parent_layout = QVBoxLayout()
        qwidget.setLayout(parent_layout)

        grid_layout = QGridLayout()
        layout = QVBoxLayout()
        parent_layout.addLayout(grid_layout)
        parent_layout.addLayout(layout)

        # GRID LAYOUT - CONTROLS
        # ======================
        v_spacing = 20
        row = -1
        # self.layout.addWidget(QH)

        row += 1
        label = QLabel("Phase jump (FT)", alignment=Qt.AlignHCenter)
        label.setStyleSheet("""font-size: 20px;""")
        grid_layout.addWidget(label, row, 0, 1, 2)
        grid_layout.addWidget(JapcToggleButton(self.lsa), row, 2)
        row += 1
        grid_layout.addWidget(SPSWindow.h_line(), row, 0, 1, 4)

        row += 1
        grid_layout.addWidget(QLabel("Start phase jump", alignment=Qt.AlignRight | Qt.AlignVCenter), row, 0)
        grid_layout.addWidget(JapcToggleButton(self.lsa), row, 1)
        grid_layout.addWidget(JapcLineEdit(self.lsa), row, 2)

        row += 1
        grid_layout.addWidget(QLabel("Jump to stable phase - delay from start", alignment=Qt.AlignRight | Qt.AlignVCenter), row, 0)
        grid_layout.addWidget(JapcToggleButton(self.lsa), row, 1)
        grid_layout.addWidget(JapcLineEdit(self.lsa), row, 2)

        row += 1
        grid_layout.addWidget(QLabel("Main RF off - delay from start", alignment=Qt.AlignRight | Qt.AlignVCenter), row, 0)
        grid_layout.addWidget(JapcToggleButton(self.lsa), row, 1)
        grid_layout.addWidget(JapcLineEdit(self.lsa), row, 2)

        row += 1
        grid_layout.addItem(QSpacerItem(10, v_spacing, QSizePolicy.Expanding, QSizePolicy.Fixed), row, 0)
        # ===============================================================================================

        row += 1
        label = QLabel("Non-adiabatic voltage step (AWAKE)", alignment=Qt.AlignHCenter)
        label.setStyleSheet("""font-size: 20px;""")
        grid_layout.addWidget(label, row, 0, 1, 2)
        grid_layout.addWidget(JapcToggleButton(self.lsa), row, 2)
        row += 1
        grid_layout.addWidget(SPSWindow.h_line(), row, 0, 1, 4)

        row += 1
        grid_layout.addWidget(QLabel("Total voltage 200 MHz", alignment=Qt.AlignRight | Qt.AlignVCenter), row,
                              0)
        # grid_layout.addWidget(JapcToggleButton(self.lsa), row, 1)
        grid_layout.addWidget(JapcLineEdit(self.lsa), row, 2)

        row += 1
        grid_layout.addItem(QSpacerItem(10, v_spacing, QSizePolicy.Expanding, QSizePolicy.Fixed), row, 0)
        # ===============================================================================================

        grid_layout.setHorizontalSpacing(20)

        # VBOX LAYOUT DIAGNOSTICS
        # =======================
        mplw = MplWidget(2, 1, nav_bar=False, sharex=True)
        ax1, ax2= mplw.axes

        ax1.set_ylabel("Peak detected")
        ax2.set_ylabel("Bunch length")
        ax2.set_xlabel("Time [ms]")

        mplw.fig.tight_layout()
        layout.addWidget(mplw)

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
