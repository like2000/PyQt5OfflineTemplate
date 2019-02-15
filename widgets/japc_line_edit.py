import jpype
import numpy as np
from collections import deque
from abc import abstractmethod

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class JapcLineEdit(QLineEdit):

    def __init__(self, lsa, parameter=None, offset=lambda: 0, getter=None, setter=None, fromLSA=True,
                 dtype=int, **kwargs):

        super(JapcLineEdit, self).__init__(**kwargs)

        self.lsa = lsa.lsa
        self.japc = lsa.japc
        self.parameter = parameter

        if parameter:
            self.setToolTip(('\n').join(str(self.parameter).strip('[]').split(', ')))
            self.update_parameter(parameter, fromLSA)

        # TODO - think about how to do this better...
        # this is not a function call and is copied fix at instantiation - maybe due to the evaluation!
        self.offset = offset

        if getter is not None:
            self.getter = getter
        else:
            self.getter = self._getter
        if setter is not None:
            self.setter = setter
        else:
            self.setter = self._setter

        self.dtype = dtype
        self.is_changed = False
        self.trim_value = deque(maxlen=2)

        # self.setFixedSize(90, 35)
        self.setFont(QFont("Nimbus Sans", pointSize=11, weight=QFont.Bold))
        # self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.textEdited.connect(self.italize_text)
        self.editingFinished.connect(self.normalize_text)


    def update_parameter(self, parameter, fromLSA=True):
        self.parameter = parameter
        # print(parameter)
        self.japc.add_subscribe(parameter, fromLSA=False)
        self.japc.newDataReceived.connect(self.update_value)


    def update_changed(self, value):
        self.trim_value.append(float(value))
        self.is_changed = False


    def set_changed(self):
        self.is_changed = True


    def normalize_text(self):
        self.setStyleSheet("""color: white; font-style: normal""")
        self.set_changed()


    def italize_text(self):
        self.setStyleSheet("""color: khaki; font-style: italic; font-weight: normal""")


    def _getter(self):

        if type(self.parameter) is list:
            try:
                coarse, fine = self.parameter
                v_coarse = self.japc.parameters_dict[coarse]
                v_fine = self.japc.parameters_dict[fine] * 1e-4
                value = v_coarse + v_fine + self.offset()
                self.setText("{:g}".format(np.round(value, decimals=4)))
            except ValueError:
                key = self.parameter[0]
                value = self.japc.parameters_dict[key] + self.offset()
                self.setText("{:d}".format(value))
        else:
            value = self.japc.parameters_dict[self.parameter]

        return value


    def _setter(self, value):

        # if value is None:
        #     value = self.text()

        if self.dtype == int:
            value = int(value)
        elif self.dtype == float:
            value = float(value)
        else:
            raise ValueError("Unknown type {:s}".format(type))

        value = value - self.offset()

        return value


    @pyqtSlot(str)
    def update_value(self, parameter):
        if parameter in self.parameter:
            try:
                value = self.getter()
            except TypeError:
                value = self.getter

            self.setText("{:g}".format(value))

            # print(self.parameter, self.japc.user, self.offset())
            # if "SX.RF2-5-8/Delay#delay" in self.parameter:
            #     print(self.parameter, self.japc.user, self.offset())

            self.update_changed(value)


    @abstractmethod
    def lsa_set_value(self):

        value = self.setter(self.text())

        if type(self.parameter) is list:
            parameter = self.parameter
        else:
            parameter = list([self.parameter])

        try:
            intg, frac = divmod(value, 1)
            intg, frac = int(intg), int(frac * 1e4)
            self.lsa.trim_settings(parameter[1], frac)
            self.lsa.trim_settings(parameter[0], intg)
        except IndexError:
            self.lsa.trim_settings(parameter[0], value)

        # print("\nSetting {:s} to {:g}!".format(parameter, value))

        # try:
        #     self.lsa.trim_settings(parameter, value)
        # except jpype.JavaException:
        #     try:
        #         print("rmi://virtual_sps/" + parameter, value)
        #         self.japc.japc.setParam("rmi://virtual_sps/" + parameter, value)
        #     except jpype.JavaException:
        # message = QMessageBox.warning(self, "Trim failed warning",
        #                               "Trim of parameter {:s} failed!".format(parameter))

        # self.trim_value.append(value)
        # self.is_changed = False

        # # TODO: Hack if you are not subscribed - otherwise remove...! Or remove above.
        # self.update_changed(value)
        # # ===========================================


    @abstractmethod
    def lsa_revert_value(self):
        value = self.trim_value[0]

        # # TODO: Also only needed if not subscribed...
        # self.setText("{:g}".format(value))
        # self.update_changed("{:g}".format(value))
        # # ===========================================

        value = self.setter(value)

        if type(self.parameter) is list:
            parameter = self.parameter
        else:
            parameter = list([self.parameter])

        try:
            intg, frac = divmod(value, 1)
            intg, frac = int(intg), int(frac * 1e4)
            self.lsa.trim_settings(parameter[0], intg, comment="Revert trim from YaRFT")
            self.lsa.trim_settings(parameter[1], frac, comment="Revert trim from YaRFT")
        except IndexError:
            # print(parameter, value)
            self.lsa.trim_settings(parameter[0], value ,comment="Revert trim from YaRFT")