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
        self.wnd = wnd

        self.setTitle(series.name)
        layout = QVBoxLayout()

        if series.dtypes == np.object:
            layout.addWidget(QLabel("Type: string"))
        elif series.dtypes == np.int64:
            layout.addWidget(QLabel("Type: integer"))
        elif series.dtypes == np.float64:
            layout.addWidget(QLabel("Type: real number"))
        else:
            layout.addWidget(QLabel("Type: unknown"))

        self.missingLabel = QLabel()
        self.missingButton = QPushButton("Remove missing values")
        self.missingButton.clicked.connect(self.remove_missing)
        missingLayout = QHBoxLayout()
        missingLayout.addWidget(self.missingLabel)
        missingLayout.addWidget(self.missingButton)

        meaningLayout = QHBoxLayout()
        meaningLayout.addWidget(QLabel("Meaning:"))
        self.meaningComboBox = QComboBox()
        if series.dtypes == np.object:
            self.meaningComboBox.addItem("several independent categories")
        elif series.dtypes in [np.int64, np.float64]:
            self.meaningComboBox.addItem("a continuous value")
            if len(series.value_counts()) < 40:
                self.meaningComboBox.addItem("several independent categories")
        self.meaningComboBox.addItem("none, should be ignored")
        layout.addLayout(missingLayout)
        meaningLayout.addWidget(self.meaningComboBox)
        layout.addLayout(meaningLayout)

        btn = QPushButton("View values")
        btn.clicked.connect(self.view_values)
        layout.addWidget(btn)

        f, self.ax1 = plt.subplots(1)
        self.distinctValuesLabel = QLabel()
        layout.addWidget(self.distinctValuesLabel)
        self.figureCanvas = FigureCanvas(f)
        layout.addWidget(self.figureCanvas)

        self.setLayout(layout)
        self.setMinimumHeight(400)
        self.update_data(series, all_data)

    def update_data(self, series: pd.Series, all_data: pd.DataFrame):
        assert self.series.dtypes == series.dtypes
        self.series = series
        self.all_data = all_data

        missing = series.isnull().sum()
        if missing:
            self.missingLabel.setText("Missing values: {} ({:.0f}%)".format(missing, missing / len(series) * 100.0))
            self.missingLabel.setStyleSheet("color: red")
            self.missingButton.show()
        else:
            self.missingLabel.setText("All values are present")
            self.missingLabel.setStyleSheet("")
            self.missingButton.hide()

        if series.dtypes in [np.float, np.int64]:
            self.ax1.cla()
            sns.distplot(series.dropna(), bins=10, ax=self.ax1, kde=(series.dtypes == np.float))
            self.distinctValuesLabel.hide()
            self.figureCanvas.show()
        elif series.dtypes == np.object:
            counts = series.value_counts()
            self.distinctValuesLabel.setText("Distinct values: {}".format(len(counts)))
            self.distinctValuesLabel.show()
            if len(counts) > 6:
                total = counts[6:].sum()
                counts = counts[:6]
                counts["Other"] = total
            na = series.isnull().sum()
            if na:
                counts["N/A"] = na

            self.ax1.cla()
            sns.barplot(x=counts.index, y=counts, ax=self.ax1)
            self.figureCanvas.draw()
            self.figureCanvas.show()

    def view_values(self, checked: Optional[bool]):
        self.viewer = ColumnValuesWidget(self.series, self.all_data, self.wnd)
        self.viewer.show()

    def remove_missing(self, checked: Optional[bool]):
        self.wnd.data = self.wnd.data[~self.series.isnull()]
        self.wnd.update_data()

    def meaning(self):
        return self.meaningComboBox.currentText()