from collections import deque
from abc import abstractmethod

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class JapcToggleButtonLogic(QPushButton):

    def __init__(self, lsa, parameter=None, fromLSA=True, text_on="Enabled", text_off="Disabled", parent=None, **kwargs):
        super(JapcToggleButtonLogic, self).__init__(parent=parent, **kwargs)

        self.lsa = lsa.lsa
        self.japc = lsa.japc

        if parameter is not None:
            if type(parameter) is list:
                self.parameter = parameter
            else:
                self.parameter = [parameter]

            self.setToolTip(('\n').join(str(self.parameter).strip('[]').split(', ')))
            self.update_parameter(parameter, fromLSA)

        self.text_on = text_on
        self.text_off = text_off

        self.is_changed = False
        self.trim_value = deque(maxlen=2)

        self.setCheckable(True)
        self.setText("Inactive")
        self.setStyleSheet("""
            QPushButton {
                border: none;
                background: none;
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                 stop: 0 lightgray, stop: 0.32 rgba(63, 63, 63, 255),
                                 stop: 0.33 rgba(31, 31, 31, 255), stop: 0.60 rgba(31, 31, 31, 255), 
                                 stop: 1 dimgray);}
        """)

        self.setFixedSize(80, 30)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        self.toggled.connect(self.toggle)
        self.clicked.connect(self.set_changed)


    def update_parameter(self, parameter, fromLSA=True):

        if type(parameter) is list:
            self.parameter = parameter
        else:
            self.parameter = [parameter]
        self.japc.add_subscribe(parameter, fromLSA=False)
        self.japc.newDataReceived.connect(self.update_value)


    def update_changed(self, value):
        self.trim_value.append(value)
        self.is_changed = False


    def set_changed(self):
        self.is_changed = True


    def toggle(self, checked):
        if checked:
            glow = QGraphicsDropShadowEffect()
            glow.setOffset(0, 0)
            glow.setBlurRadius(10)
            glow.setColor(QColor("green"))
            self.setGraphicsEffect(glow)
            self.setText(self.text_on)
            self.setStyleSheet("""
                QPushButton {
                    color: white;
                    border: none;
                    background: none;
                    font-size: 11px;
                    font-weight: bold;
                    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 lightgreen, stop: 0.32 rgba(63, 63, 63, 255),
                                      stop: 0.33 rgba(31, 31, 31, 255), stop: 0.60 rgba(31, 31, 31, 255), 
                                      stop: 1 green);}
            """)
        else:
            self.setGraphicsEffect(None)
            self.setText(self.text_off)
            self.setStyleSheet("""
                QPushButton {
                    color: white;
                    border: none;
                    background: none;
                    font-size: 11px;
                    font-weight: bold;
                    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 lightcoral, stop: 0.32 rgba(63, 63, 63, 255),
                                      stop: 0.33 rgba(31, 31, 31, 255), stop: 0.60 rgba(31, 31, 31, 255), 
                                      stop: 1 red);}
            """)


    @pyqtSlot(str)
    def update_value(self, parameter):

        if parameter in self.parameter:
            value = [self.japc.parameters_dict[p] for p in self.parameter]

            # # Handle all the various type of returns
            # # ======================================
            # # print(parameter, value)
            # if type(value) is list:
            #     state = [v[1] for v in value]
            #     value = [v[0] for v in value]
            #     value = all(value)
            # elif type(value) is tuple:
            #     value = value[0]
            value = all(value)  # [0]

            self.setChecked(value)
            self.toggle(self.isChecked())
            self.update_changed(self.isChecked())


    @abstractmethod
    def lsa_set_value(self):

        if self.parameter:
            value = int(self.isChecked())

            for p in self.parameter:
                self.lsa.trim_settings(p, value)


    @abstractmethod
    def lsa_revert_value(self):
        value = int(self.trim_value[0])

        for p in self.parameter:
            self.lsa.trim_settings(p, value, self.lsa.comment)

        self.setChecked(value)
        self.toggle(self.isChecked())