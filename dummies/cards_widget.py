from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets


class CardWidget(QtWidgets.QFrame):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.initUi()

    def initUi(self):
        '''

        :return:
        '''
        self.setFixedHeight(100)
        self.setObjectName("Outer")
        self.setStyleSheet("""
            QFrame {background-color: whitesmoke;}
            QFrame#Outer {border: 2px solid lightgray; border-radius: 8px;}
        """)
        # rgba(64, 64, 64, 1)

        effect = QtWidgets.QGraphicsDropShadowEffect()
        effect.setOffset(2, 2)
        effect.setBlurRadius(15)
        effect.setColor(QtGui.QColor("black"))
        self.setGraphicsEffect(effect)

        self.textArea = QtWidgets.QTextEdit()
        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().addWidget(self.textArea)
        self.textArea.setStyleSheet("""
            background-color: transparent;
        """)

    def sizeHint(self) -> QtCore.QSize:
        return super().sizeHint()
