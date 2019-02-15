import sys

from PyQt5 import QtWidgets


class NewWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):

        super().__init__(parent)

        print(dir(self))


class Second(QtWidgets.QMainWindow):

    def __init__(self, parent=None):

        super(Second, self).__init__(parent)


class First(QtWidgets.QMainWindow):

    def __init__(self, parent=None):

        super(First, self).__init__(parent)
        self.pushButton = QtWidgets.QPushButton("Click me...")

        self.setCentralWidget(self.pushButton)

        self.pushButton.clicked.connect(self.on_pushButton_clicked)
        self.dialog = Second(self)

        self.show()

    def on_pushButton_clicked(self):
        self.dialog.show()


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    win = First()
    sys.exit(app.exec_())