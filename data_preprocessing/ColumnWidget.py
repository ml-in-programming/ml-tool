from typing import Optional
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from ColumnValuesWidget import ColumnValuesWidget


class ColumnWidget(QGroupBox):
    def __init__(self, series: pd.Series, all_data: pd.DataFrame, wnd):
        super().__init__()
        self.series = series
        self.all_data = all_data
        self.wnd = wnd

        self.setTitle(series.name)
        layout = QVBoxLayout()
        #layout.addWidget(QLabel("Name: " + series.name))
        if series.dtypes.name == "object":
            layout.addWidget(QLabel("Type: string"))
        elif series.dtypes.name == "int64":
            layout.addWidget(QLabel("Type: integer"))
        elif series.dtypes.name == "float64":
            layout.addWidget(QLabel("Type: real number"))
        else:
            layout.addWidget(QLabel("Type: unknown"))

        missing = series.isnull().sum()
        if missing:
            missingLabel = QLabel("Missing values: {} ({:.0f}%)".format(missing, missing / len(series) * 100.0))
            missingLabel.setStyleSheet("color: red")

            missingButton = QPushButton("Remove missing values")
            missingButton.clicked.connect(self.remove_missing)

            missingLayout = QHBoxLayout()
            missingLayout.addWidget(missingLabel)
            missingLayout.addWidget(missingButton)
            layout.addLayout(missingLayout)
        else:
            layout.addWidget(QLabel("All values are present"))

        btn = QPushButton("View values")
        btn.clicked.connect(self.view_values)
        layout.addWidget(btn)

        if series.dtypes in [np.float, np.int64]:
            f,  ax1 = plt.subplots(1)
            sns.distplot(series.dropna(), bins=10, ax=ax1, kde=(series.dtypes == np.float))
            layout.addWidget(FigureCanvas(f))
        elif series.dtypes == np.object:
            counts = series.value_counts()
            layout.addWidget(QLabel("Distinct values: {}".format(len(counts))))
            if len(counts) > 6:
                total = counts[6:].sum()
                counts = counts[:6]
                counts["Other"] = total
            na = series.isnull().sum()
            if na:
                counts["N/A"] = na

            f,  ax1 = plt.subplots(1)
            sns.barplot(x=counts.index, y=counts, ax=ax1)
            layout.addWidget(FigureCanvas(f))

        self.setLayout(layout)
        self.setMinimumHeight(400)

    def view_values(self, checked: Optional[bool]):
        self.viewer = ColumnValuesWidget(self.series, self.all_data, self.wnd)
        self.viewer.show()

    def remove_missing(self, checked: Optional[bool]):
        self.wnd.data = self.wnd.data[~self.series.isnull()]
        self.wnd.update()
