from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

class ColumnWidget(QGroupBox):
    def __init__(self, series: pd.DataFrame):
        super().__init__()
        self.series = series

        self.setTitle(series.name)
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Name: " + series.name))
        layout.addWidget(QLabel("Type: " + series.dtypes.name))
        layout.addWidget(QLabel("Missing: {} ({:.0f}%)".format(series.isnull().sum(), series.isnull().sum() / len(series) * 100.0)))
        if series.dtypes in [np.float, np.int64]:
            f,  ax1 = plt.subplots(1)
            sns.distplot(series.dropna(), bins=10, ax=ax1, kde=(series.dtypes == np.float))
            layout.addWidget(FigureCanvas(f))
        elif series.dtypes == np.object:
            counts = series.value_counts()
            layout.addWidget(QLabel("Distinct: {}".format(len(counts))))
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
