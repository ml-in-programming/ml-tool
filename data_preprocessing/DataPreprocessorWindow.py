from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
import pandas as pd
from ColumnWidget import ColumnWidget
import os.path

class DataPreprocessorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Data preprocessor")

        loadData = QAction("Load", self)
        loadData.triggered.connect(self.load_data_dialog)
        self.menuBar().addAction(loadData)

        saveData = QAction("Save", self)
        saveData.triggered.connect(self.save_data)
        self.menuBar().addAction(saveData)

        filename = QApplication.arguments()[1]
        if filename:
            self.load_data(filename)

    def load_data_dialog(self):
        filename, ext = QFileDialog.getOpenFileName(self, "Choose non-preprocessed data", None, "*.csv")
        if filename:
            self.load_data(filename)

    def load_data(self, filename):
        self.data = pd.read_csv(filename)
        self.filename = filename
        self.columns = []
        self.layout = QGridLayout()
        for i, col in enumerate(self.data.columns):
            columnWidget = ColumnWidget(self.data[col], self.data, self)
            self.columns.append(columnWidget)
            self.layout.addWidget(columnWidget, i // 2, i % 2)
        widget = QWidget()
        widget.setLayout(self.layout)
        area = QScrollArea()
        area.setWidget(widget)
        area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        area.setWidgetResizable(True)
        self.setCentralWidget(area)
        self.update_data()

    def update_data(self):
        for i, col in enumerate(self.data.columns):
            self.columns[i].update_data(self.data[col], self.data)

    def save_data(self):
        result = pd.DataFrame()
        for i, col in enumerate(self.data.columns):
            meaning = self.columns[i].meaning()
            if meaning == "a continuous value":
                result = pd.concat([result, self.data[col]], axis=1)
            elif meaning == "several independent categories":
                result = pd.concat([result, pd.get_dummies(self.data[col], prefix=col)], axis=1)
            elif meaning == "none, should be ignored":
                pass
            else:
                print("BUG: unknown column meaning: '{}'".format(meaning))

        name, ext = os.path.splitext(self.filename)
        result.to_csv(name + "-processed" + ext, index=False)
