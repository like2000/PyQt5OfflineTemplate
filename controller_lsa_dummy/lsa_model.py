import typing

import pandas as pd
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class LsaModel(QAbstractTableModel):

    def __init__(self, parent: QObject = None) -> None:
        super().__init__(parent)

        self.data_table = pd.DataFrame(columns=["Context", "User", "Type"])
        self.data_table['Context'] = range(0, 3)
        self.data_table['User'] = range(3, 6)
        self.data_table['Type'] = range(6, 9)
        # self.data_table.loc[1, :] = ['1', '2', '3']
        print(self.data_table.iloc[0, 1])

    def insertRow(self, row: int, parent: QModelIndex = ...) -> bool:
        return super().insertRow(row, parent)

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        i, j, = index.row(), index.column()

        if (role == Qt.FontRole):
            font = QFont("Nimbus Sans", 11, QFont.Bold)
            return font
        # elif (role == Qt.SizeHintRole):
        #     size = QSize(10, cw.height() + 20)
        #     return size
        elif role == Qt.DisplayRole:
            # i = index.row()
            # r, g, b, a = self.color_scheme[i]
            # cw.setStyleSheet(f"""
            #            QFrame {{background-color: rgba({r}, {g}, {b}, {a});}}
            #            QFrame#Outer {{border: 2px solid lightgray; border-radius: 8px;}}
            #        """)
            # cw.textArea.setHtml(self.datatable.to_html())
            return f'{self.data_table.iloc[i, j]}'
        else:
            return QVariant()

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return len(self.data_table.columns)

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self.data_table.index)
