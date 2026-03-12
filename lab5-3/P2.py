"""
Panhathai Suporn
683040496-5
P2
"""
import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QFormLayout,
                               QHBoxLayout, QLabel, QComboBox, QLineEdit, QPushButton,
                               QFrame, QSpinBox, QColorDialog, QFileDialog, QToolBar, QStyle, QMessageBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QAction, QIcon, QPixmap, QPainter
from PySide6.QtCharts import (
    QChart, QChartView, QBarSet,
    QBarSeries, QBarCategoryAxis, QValueAxis
)

class Chart(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Monthly Sales Data Chart")
        self.resize(900, 600)

        self.data = {}

        self.months = ["Jan", "Feb", "Mar", "Apr", "May",
                    "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        
        self.categories = ["Electronics", "Clothing", "Food", "Others"]

        self.InitUI()

    def InitUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()

        input_layout = QHBoxLayout()

        self.month_combo = QComboBox()
        self.month_combo.addItems(self.months)
        input_layout.addWidget(QLabel("Month:"))
        input_layout.addWidget(self.month_combo)

        self.amount_input = QSpinBox()
        self.amount_input.setRange(1,999999)
        self.amount_input.setValue(10000)
        input_layout.addWidget(QLabel("Sales Amount (à¸¿)"))
        input_layout.addWidget(self.amount_input)

        self.categories_combo = QComboBox()
        self.categories_combo.addItems(self.categories)
        input_layout.addWidget(QLabel("Categories:"))
        input_layout.addWidget(self.categories_combo)

        main_layout.addLayout(input_layout)

        button_layout = QHBoxLayout()

        self.import_button = QPushButton("Import Data")
        self.import_button.clicked.connect(self.import_data)
        button_layout.addWidget(QLabel("Import Data"))
        button_layout.addWidget(self.import_button)

        self.add_button = QPushButton("Add Data")
        self.add_button.clicked.connect(self.add_data)
        button_layout.addWidget(self.add_button)

        self.clear_button = QPushButton("Clear Chart")
        self.clear_button.clicked.connect(self.clear_chart)
        button_layout.addWidget(self.clear_button)

        main_layout.addLayout(button_layout)

        self.chart = QChart()
        self.chart.setTitle("Monthly Sales by Product Category")

        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)

        main_layout.addWidget(self.chart_view)

        central_widget.setLayout(main_layout)

        self.update_chart()

    def import_data(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select a File",          # Window title
            "",                       # Default directory ("" = current)
            "All Files (*);;Text Files (*.txt);;CSV Files (*.csv)"
        )

        try:
            with open(file_path, "r") as file:
                self.data.clear()
                for line in file:
                    month, category, amount = line.strip().split(",")
                    self.data[(month, category)] = float(amount)

            QMessageBox.information(self, "Success", "Data imported successfully!")
            self.update_chart()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Invalid file format!\n{e}")

    def add_data(self):
        month = self.month_combo.currentText()
        category = self.categories_combo.currentText()
        amount_text = self.amount_input.value()

        
        amount = float(amount_text)

        self.data[(month, category)] = amount

        self.update_chart()

    def clear_chart(self):
        self.data.clear()
        self.update_chart()

    def update_chart(self):
        self.chart.removeAllSeries()

        for axis in self.chart.axes():
            self.chart.removeAxis(axis)

        series = QBarSeries()

        for category in self.categories:
            bar_set = QBarSet(category)

            for month in self.months:
                Value = self.data.get((month, category), 0)
                bar_set.append(Value)

            series.append(bar_set)

        self.chart.addSeries(series)

        axis_x = QBarCategoryAxis()
        axis_x.append(self.months)
        self.chart.addAxis(axis_x, Qt.AlignBottom)
        series.attachAxis(axis_x)

        # Y-axis 
        axis_y = QValueAxis()
        axis_y.setTitleText("Sales Amount")
        self.chart.addAxis(axis_y, Qt.AlignLeft)
        series.attachAxis(axis_y)

        self.chart.setTitle("Monthly Sales Report")
        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignBottom)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Chart()
    window.show()
    sys.exit(app.exec())