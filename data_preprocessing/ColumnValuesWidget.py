from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import pandas as pd
import numpy as np
from RowsWidget import RowsWidget

class ColumnValuesWidget(QWidget):
    def __init__(self, series: pd.Series, all_data: pd.DataFrame):
        super().__init__()
        self.series = series
        self.all_data = all_data

        layout = QVBoxLayout()

        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(["Value", "Count"])
        tbl = np.asarray(np.unique(series.dropna(), return_counts=True)).T
        o = np.argsort(tbl[:, 1])[::-1][:50]
        model.appendRow([QStandardItem("N/A"), QStandardItem(str(series.isnull().sum()))])
        for val, cnt in tbl[o]:
            model.appendRow([QStandardItem(str(val)), QStandardItem(str(cnt))])

        self.table = QTableView()
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSortingEnabled(True)
        self.table.setModel(model)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        layout.addWidget(self.table)

        btn = QPushButton("Show corresponding values")
        btn.clicked.connect(self.show_values)
        layout.addWidget(btn)

        self.setLayout(layout)
        self.setWindowTitle("Some window")

    def show_values(self):
        vals = []
        model = self.table.model()
        for idx in self.table.selectedIndexes():
            if idx.column() == 0:
                vals.append(self.series.dtype.type(model.data(idx)))
        self.rows_widget = RowsWidget(self.all_data[self.all_data[self.series.name].isin(vals)])
        self.rows_widget.show()
