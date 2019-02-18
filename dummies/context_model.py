import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from dummies.cards_widget import CardWidget


class ContextModel(QAbstractListModel):

    def __init__(self, parent=None, *args):

        super().__init__(parent=parent)

        self.items_list = [CardWidget() for i in range(10)]

        self.datatable = pd.DataFrame({
            'Days': [1, 2, 3, 4],
            'Exercise': ["one", "two", "three", "four"]
        })

        alpha = 0.4
        self.color_scheme = [plt.cm.rainbow(i) for i in np.linspace(0, 1, 10)]
        self.color_scheme = [list(c[:-1]) + [alpha] for c in self.color_scheme]
        self.color_scheme = map(lambda x: np.int_(np.array(x) * 255), self.color_scheme)
        self.color_scheme = list(self.color_scheme)

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self.items_list)

    def data(self, index, role=Qt.DisplayRole):

        parent = self.parent()
        cw = self.items_list[index.row()]
        if not parent.indexWidget(index):
            parent.setIndexWidget(index, cw)

        if (role == Qt.FontRole):
            font = QFont("Nimbus Sans", 11, QFont.Bold)
            return font
        elif (role == Qt.SizeHintRole):
            size = QSize(10, cw.height() + 20)
            return size
        elif role == Qt.DisplayRole:
            i = index.row()
            r, g, b, a = self.color_scheme[i]
            cw.setStyleSheet(f"""
                QFrame {{background-color: rgba({r}, {g}, {b}, {a});}}
                QFrame#Outer {{border: 2px solid lightgray; border-radius: 8px;}}
            """)
            cw.textArea.setHtml(self.datatable.to_html())
            # return f'{self.items_list[i]}'
        # elif role == Qt.BackgroundRole:
        #     return QBrush(QColor(*self.color_scheme[index.row()]))
        # elif (role == Qt.ForegroundRole and index.column() == 0):
        #     return QColor("orange")
        # elif (role == Qt.ForegroundRole and index.column() == 1):
        #     return QColor("limegreen")
        else:
            return QVariant()

    # def headerData(self, rowcol, orientation, role):
    #     if orientation == Qt.Horizontal and role == Qt.DisplayRole:
    #         return self.datatable.columns[rowcol]
    #     if orientation == Qt.Vertical and role == Qt.DisplayRole:
    #         return self.datatable.index[rowcol]
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
#     def rowCount(self, index=QModelIndex()):
#         """ Returns the number of rows the model holds. """
#         return len(self.addresses)
#
#     def columnCount(self, index=QModelIndex()):
#         """ Returns the number of columns the model holds. """
#         return 2
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
