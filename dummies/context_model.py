import pandas as pd
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class ContextModel(QStandardItemModel):

    def __init__(self, parent=None, *args):
        super().__init__(parent=parent)

        self.data_table = pd.DataFrame(columns=["Context", "User", "Type"])
        print(len(self.data_table.columns))

    @staticmethod
    def styled_item(text="", foreground='black', background='white'):
        item = QStandardItem(text)
        item.setBackground(QColor(background))
        item.setForeground(QColor(foreground))
        item.setFont(QFont("Roboto", pointSize=10, weight=QFont.Bold))

        return item

    #     self.active_context = ["LHC", "SFT", "AWAKE", "HiRadMat"]
    #     self.resident_context = ["LHC2", "SFT1"]
    #     self.existing_context = ["LHCION", "SFTION", "Coast"]
    #
    #     self.items_list = self.active_context + self.resident_context + self.existing_context

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self.data_table.index)

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return len(self.data_table.columns)

    # def data(self, index, role=Qt.DisplayRole):
    #     i, j = index.row(), index.column()
    #     # val = self.data_table.iloc[i, j]
    #     if (role == Qt.FontRole):
    #         font = QFont("Nimbus Sans", 11, QFont.Bold)
    #         return font
    #     # elif (role == Qt.SizeHintRole):
    #     #     size = QSize(10, 10)
    #     #     return size
    #     # elif role == Qt.DisplayRole:
    #     #     return f'{val}'
    #     # elif (role == Qt.BackgroundRole and val not in self.existing_context):
    #     #     return QBrush(QColor("black"))
    #     # elif (role == Qt.BackgroundRole and val in self.existing_context):
    #     #     return QBrush(QColor("white"))
    #     # elif (role == Qt.ForegroundRole and val in self.active_context):
    #     #     return QColor("limegreen")
    #     # elif (role == Qt.ForegroundRole and val in self.resident_context):
    #     #     return QColor("orange")
    #     # elif (role == Qt.ForegroundRole and val in self.existing_context):
    #     #     return QColor("black")
    #     else:
    #         return QVariant()

    # def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> typing.Any:
    #     # if orientation == Qt.Horizontal and role == Qt.DisplayRole:
    #     #     return self.items_list[section]
    #     # if orientation == Qt.Vertical and role == Qt.DisplayRole:
    #     #     return self.items_list[section]
    #     return None

# class TableModel2(QAbstractTableModel):
#
#     def __init__(self, addresses=None, parent=None):
#         super(TableModel2, self).__init__(parent)
#
#         if addresses is None:
#             self.addresses = []
#         else:
#             self.addresses = addresses
#
#     def data(self, index, role=Qt.DisplayRole):
#         """ Depending on the index and role given, return data. If not
#             returning data, return None (PySide equivalent of QT's
#             "invalid QVariant").
#         """
#         if not index.isValid():
#             return None
#
#         if not 0 <= index.row() < len(self.addresses):
#             return None
#
#         if role == Qt.DisplayRole:
#             name = self.addresses[index.row()]["name"]
#             address = self.addresses[index.row()]["address"]
#
#             if index.column() == 0:
#                 return name
#             elif index.column() == 1:
#                 return address
#
#         return None
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
#
#     def insertRows(self, position, rows=1, index=QModelIndex()):
#         """ Insert a row into the model. """
#         self.beginInsertRows(QModelIndex(), position, position + rows - 1)
#
#         for row in range(rows):
#             self.addresses.insert(position + row, {"name": "", "address": ""})
#
#         self.endInsertRows()
#         return True
#
#     def removeRows(self, position, rows=1, index=QModelIndex()):
#         """ Remove a row from the model. """
#         self.beginRemoveRows(QModelIndex(), position, position + rows - 1)
#
#         del self.addresses[position:position + rows]
#
#         self.endRemoveRows()
#         return True
#
#     def setData(self, index, value, role=Qt.EditRole):
#         """ Adjust the data (set it to <value>) depending on the given
#             index and role.
#         """
#         if role != Qt.EditRole:
#             return False
#
#         if index.isValid() and 0 <= index.row() < len(self.addresses):
#             address = self.addresses[index.row()]
#             if index.column() == 0:
#                 address["name"] = value
#             elif index.column() == 1:
#                 address["address"] = value
#             else:
#                 return False
#
#             self.dataChanged.emit(index, index)
#             return True
#
#         return False
#
#     def flags(self, index):
#         """ Set the item flags at the given index. Seems like we're
#             implementing this function just to see how it's done, as we
#             manually adjust each tableView to have NoEditTriggers.
#         """
#         if not index.isValid():
#             return Qt.ItemIsEnabled
#         return Qt.ItemFlags(QAbstractTableModel.flags(self, index) |
#                             Qt.ItemIsEditable)
