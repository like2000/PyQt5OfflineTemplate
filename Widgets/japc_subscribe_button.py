from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class JapcSubscribeButton(QPushButton):

    def __init__(self, lsa, parameter=None, fromLSA=True, text_on="Active", text_off="Off", parent=None, **kwargs):
        super(JapcSubscribeButton, self).__init__(parent=parent, **kwargs)

        self.lsa = lsa.lsa
        self.japc = lsa.japc
        self.parameter = parameter

        if parameter is not None:
            self.japc.add_subscribe(parameter, fromLSA)
            self.japc.newDataReceived.connect(self.update_value)

        # self.setEnabled(False)

        self.text_on = text_on
        self.text_off = text_off

        self.setCheckable(True)
        self.setStyleSheet("""
            QPushButton {
                color: white;
                border: none;
                background: none;
                font-size: 12px;
                font-weight: bold;
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                 stop: 0 lightcoral, stop: 0.32 rgba(63, 63, 63, 255),
                                 stop: 0.33 rgba(31, 31, 31, 255), stop: 0.55 rgba(31, 31, 31, 255), 
                                 stop: 1 red);
            }
            QPushButton:checked, QPushButton:pressed {
                border: none;
                background: none;
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                 stop: 0 lightgreen, stop: 0.32 rgba(63, 63, 63, 255),
                                 stop: 0.33 rgba(31, 31, 31, 255), stop: 0.55 rgba(31, 31, 31, 255), 
                                 stop: 1 green);
            }
        """)
        # self.setStyleSheet("""
        #     QPushButton {
        #         color: white;
        #         border: none;
        #         background: none;
        #         font-size: 12px;
        #         font-weight: bold;
        #         background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
        #                          stop: 0 dimgray, stop: 0.35 lightgray,
        #                          stop: 0.36 dimgray, stop: 1.0 black);
        #         opacity: 0.2;
        #     }
        # """)
        # self.setStyleSheet("""
        #     QPushButton {
        #         color: white;
        #         border: none;
        #         background: none;
        #         font-size: 12px;
        #         font-weight: bold;
        #         background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
        #                          stop: 0 red, stop: 0.35 lightcoral,
        #                          stop: 0.36 red, stop: 1.0 darkred);
        #     }
        #     QPushButton:checked, QPushButton:pressed {
        #         border: none;
        #         background: none;
        #         background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
        #                          stop: 0 forestgreen, stop: 0.35 lightgreen,
        #                          stop: 0.36 forestgreen, stop: 1.0 darkgreen);
        #     }
        # """)
        self.setFixedSize(100, 40)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        self.toggled.connect(self.toggle)
        # self.clicked.connect(self.lsa_set_value)


    def toggle(self, checked):
        if checked:
            glow = QGraphicsDropShadowEffect()
            glow.setOffset(0, 0)
            glow.setBlurRadius(10)
            glow.setColor(QColor("green"))
            self.setGraphicsEffect(glow)
            self.setText(self.text_on)

            self.japc.run()
        else:
            # glow = QGraphicsDropShadowEffect()
            # glow.setOffset(0, 0)
            # glow.setBlurRadius(30)
            # glow.setColor(QColor("red"))
            # self.setGraphicsEffect(glow)
            self.setGraphicsEffect(None)
            self.setText(self.text_off)

            self.japc.exit()


    def update_subscribe(self):
        self.setChecked(True)
        self.toggle(self.isChecked())
        import time; time.sleep(1)
        self.setChecked(False)
        self.toggle(self.isChecked())