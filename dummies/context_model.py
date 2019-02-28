import pandas as pd

from PyQt5.QtCore import *
from PyQt5.QtGui import *


class ContextModel(QStandardItemModel):

    def __init__(self, parent=None, *args):
        super().__init__(parent=parent)

        self.data_table = pd.DataFrame(columns=["Context", "User", "State"])

        self.data_table.loc[len(self.data_table), :] = ["LHCBCMS_3Inj_Q20_2018_V1", "LHC1", "ACTIVE"]
        self.data_table.loc[len(self.data_table), :] = ["LHCBCMS_3Inj_Q20_2018_V1_8b4e", "LHC3", "ACTIVE"]
        self.data_table.loc[len(self.data_table), :] = ["SFT_PRO_MTE_L4780_2018_V1", "SFTPRO2", "RESIDENT"]
        self.data_table.loc[len(self.data_table), :] = ["LHC_ION_1Inj_Nominal_Pb82_Q26_2018_V2", "LHCION4", "RESIDENT"]
        self.data_table.loc[len(self.data_table), :] = ["SFT_PRO_MTE_L4780_2018_V1", "SFTPRO2", "RESIDENT"]
        self.data_table.loc[len(self.data_table), :] = ["AWAKE_1Inj_FB60_FT850_Q20_2018_V1", "AWAKE", "OPERATIONAL"]

    @staticmethod
    def styled_item(text="", foreground='black', background='white'):
        item = QStandardItem(text)
        item.setBackground(QColor(background))
        item.setForeground(QColor(foreground))
        item.setFont(QFont("Roboto", pointSize=10, weight=QFont.Bold))

        return item

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self.data_table.index)

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return len(self.data_table.columns)

    def data(self, index, role=Qt.DisplayRole):
        # print(index, role)
        # i, j = index.row(), index.column()
        # val = self.data_table.iloc[i, j]
        # print(i, j, val)
        if index.isValid():
            if (role == Qt.FontRole):
                font = QFont("Nimbus Sans", 11, QFont.Bold)
                return font
            #     # elif (role == Qt.SizeHintRole):
            #     #     size = QSize(10, 10)
            #     #     return size
            elif (role == Qt.DisplayRole):
                #         print(f'{val}')
                return 'Hello!'
            elif (role == Qt.BackgroundRole):
                return QBrush(QColor("black"))
            # elif (role == Qt.BackgroundRole and val in self.existing_context):
            #     return QBrush(QColor("white"))
            elif (role == Qt.ForegroundRole):
                return QColor("limegreen")
            # elif (role == Qt.ForegroundRole and val in self.resident_context):
            #     return QColor("orange")
            # elif (role == Qt.ForegroundRole and val in self.existing_context):
            #     return QColor("black")
        else:
            return QVariant()

    def appendRow(self, items: list) -> None:

        end = len(self.data_table.index)
        self.data_table.loc[end, :] = items
        self.layoutChanged.emit()
        # self.dataChanged.emit(QModelIndex(), QModelIndex())

    # def insertRow(self, row: int, parent: QModelIndex = ...) -> bool:
    #
    #     self.beginInsertRows(QModelIndex(), row, row-1)
    #     self.data_table.insert(row, {"Context": "", "User": "", "Type": ""})
    #     self.endInsertRows()
    #
    #     return True

    # def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> typing.Any:
    #     # if orientation == Qt.Horizontal and role == Qt.DisplayRole:
    #     #     return self.items_list[section]
    #     # if orientation == Qt.Vertical and role == Qt.DisplayRole:
    #     #     return self.items_list[section]
    #     return None
#
#     def headerData(self, section, orientation, role=Qt.DisplayRole):
#         """ Set the headers to be displayed. """
#         if role != Qt.DisplayRole:
#             return None
#
#         if orientation == Qt.Horizontal:
#             if section == 0:
#                 return "Name"
#             elif section == 1:
#                 return "Address"
#
#         return None

#     def flags(self, index):
#         """ Set the item flags at the given index. Seems like we're
#             implementing this function just to see how it's done, as we
#             manually adjust each tableView to have NoEditTriggers.
#         """
#         if not index.isValid():
#             return Qt.ItemIsEnabled
#         return Qt.ItemFlags(QAbstractTableModel.flags(self, index) |
#                             Qt.ItemIsEditable)
