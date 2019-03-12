import sys
import typing

import pandas as pd
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class LsaModel(QAbstractTableModel):

    def __init__(self, parent: QObject = None) -> None:
        super().__init__(parent)

        # db = QFontDatabase()
        # families = db.families()
        # print(families)
        # sys.exit(-1)

        self.data_table = pd.DataFrame(columns=["Context", "User", "State"])
        # self.data_table['Context'] = range(0, 3)
        # self.data_table['User'] = range(3, 6)
        # self.data_table['Type'] = range(6, 9)
        self.data_table.loc[len(self.data_table), :] = ["LHCBCMS_3Inj_Q20_2018_V1", "LHC1", "ACTIVE"]
        self.data_table.loc[len(self.data_table), :] = ["LHCBCMS_3Inj_Q20_2018_V1_8b4e", "LHC3", "ACTIVE"]
        self.data_table.loc[len(self.data_table), :] = ["SFT_PRO_MTE_L4780_2018_V1", "SFTPRO2", "RESIDENT"]
        self.data_table.loc[len(self.data_table), :] = ["LHC_ION_1Inj_Nominal_Pb82_Q26_2018_V2", "LHCION4", "RESIDENT"]
        self.data_table.loc[len(self.data_table), :] = ["SFT_PRO_MTE_L4780_2018_V1", "SFTPRO2", "RESIDENT"]
        self.data_table.loc[len(self.data_table), :] = ["AWAKE_1Inj_FB60_FT850_Q20_2018_V1", "AWAKE", "OPERATIONAL"]

        print(self.data_table.iloc[0, 1])

    def insertRow(self, row: int, parent: QModelIndex = ...) -> bool:
        return super().insertRow(row, parent)

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        i, j, = index.row(), index.column()
        state = self.data_table.iloc[i, 2]

        if (role == Qt.FontRole):
            font = QFont("Helvetica", 10, QFont.Black)
            return font
        # elif (role == Qt.SizeHintRole):
        #     size = QSize(10, cw.height() + 20)
        #     return size
        elif role == Qt.DisplayRole:
            return f'{self.data_table.iloc[i, j]}'
        elif (role == Qt.BackgroundRole):
            if state=="OPERATIONAL":
                return QBrush(QColor("white"))
            else:
                return QBrush(QColor("black"))
        # elif (role == Qt.BackgroundRole and val in self.existing_context):
        #     return QBrush(QColor("white"))
        elif (role == Qt.ForegroundRole):
            if j == 0:
                if state == "ACTIVE":
                    return QColor("lime")
                elif state == "RESIDENT":
                    return QColor("yellow")
                elif state == "OPERTIONAL":
                    return QColor("black")
            if j == 1:
                if state == "OPERATIONAL":
                    return QColor("black")
                else:
                    return QColor("white")
        else:
            return QVariant()

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return 2 # len(self.data_table.columns)

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self.data_table.index)
