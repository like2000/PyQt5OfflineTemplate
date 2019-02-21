import typing

import pandas as pd

from PyQt5.QtCore import *


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
        return QVariant()

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return len(self.data_table.columns)

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self.data_table.index)


