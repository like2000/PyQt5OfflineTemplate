from PyQt5 import QtCore


class Lsa:
    pass


class Japc(QtCore.QThread):
    newDataReceived = QtCore.pyqtSignal(str)

    def add_subscribe(self, parameter, **kwargs):
        print(parameter)


class LsaDummy():

    def __init__(self):
        self.lsa = Lsa()
        self.japc = Japc()
