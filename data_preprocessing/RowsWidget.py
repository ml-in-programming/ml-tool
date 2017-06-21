from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import pandas as pd
import numpy as np


class RowsWidget(QWidget):
    def __init__(self, all_data: pd.DataFrame, wnd):
        super().__init__()
        self.all_data = all_data
        self.wnd = wnd

        layout = QVBoxLayout()

        model = QStandardItemModel()
        for i, row in all_data.iterrows():
            model.appendRow(map(lambda x: QStandardItem(str(x)), row))
        model.setHorizontalHeaderLabels(all_data.columns)
        #model.setHorizontalHeaderLabels(["Value", "Count"])
        #tbl = np.asarray(np.unique(series.dropna(), return_counts=True)).T
        #o = np.argsort(tbl[:, 1])[::-1][:50]
        #model.appendRow([QStandardItem("N/A"), QStandardItem(str(series.isnull().sum()))])
        #for val, cnt in tbl[o]:
        #    model.appendRow([QStandardItem(str(val)), QStandardItem(str(cnt))])

        self.table = QTableView()
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSortingEnabled(True)
        self.table.setModel(model)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        layout.addWidget(self.table)

        btn = QPushButton("Remove rows")
        btn.clicked.connect(self.remove_rows)
        layout.addWidget(btn)

        self.setLayout(layout)
        self.setWindowTitle("Rows")

    def remove_rows(self):
        ids = set()
        for idx in self.table.selectedIndexes():
            ids.add(self.all_data.index[idx.row()])
        self.wnd.data = self.wnd.data[~self.wnd.data.index.isin(ids)]
        self.wnd.update_data()
        self.close()
