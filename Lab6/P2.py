"""
Panhathai Suporn
683040496-5
P2
Weather Log Tracker
"""

import sys, os
import json
import pandas as pd

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QGridLayout,
    QPushButton, QTableWidget, QTableWidgetItem,
    QLabel, QFileDialog, QTextEdit,
    QSplitter, QGroupBox, QComboBox,
    QDoubleSpinBox, QMessageBox, QDateEdit,
    QHeaderView,
)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QFont, QColor

from P2_style import CONDITION_COLORS
from P2_data_manip import (write_csv, write_json, 
                    read_csv, read_json, show_chart,
                    build_stats)
from P2_data_manip import (REQUIRED_COLS, CONDITIONS, 
                           CITIES)


# ══════════════════════════════════════════════════════════════════════════
#  UI — do not modify anything below this line
# ══════════════════════════════════════════════════════════════════════════

class WeatherTracker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🌦  Weather Log Tracker")
        self.setMinimumSize(1100, 700)
        self.df = pd.DataFrame()
        self._chart_widget = None
        self._build_ui()
        self._check_sample()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root_layout = QVBoxLayout(central)

        splitter = QSplitter(Qt.Horizontal)
        root_layout.addWidget(splitter)

        # ── left panel ───────────────────────────────────────────────────
        left = QWidget(); left.setMaximumWidth(280)
        ll = QVBoxLayout(left); ll.setSpacing(10)

        title = QLabel("🌦  Weather Log Tracker")
        title.setFont(QFont("Georgia", 12, QFont.Bold))
        ll.addWidget(title)

        fg = QGroupBox("File I/O")
        fl = QVBoxLayout(fg)
        self.btn_read_csv   = QPushButton("📂 Read CSV")
        self.btn_read_json  = QPushButton("📂 Read JSON")
        self.btn_write_csv  = QPushButton("💾 Save as CSV")
        self.btn_write_json = QPushButton("💾 Save as JSON")
        for b in [self.btn_read_csv, self.btn_read_json,
                  self.btn_write_csv, self.btn_write_json]:
            fl.addWidget(b)
        ll.addWidget(fg)

        addg = QGroupBox("Add Record")
        addl = QGridLayout(addg)
        self.in_date = QDateEdit(QDate.currentDate())
        self.in_date.setDisplayFormat("yyyy-MM-dd")
        self.in_city = QComboBox(); self.in_city.addItems(CITIES)
        self.in_temp = QDoubleSpinBox()
        self.in_temp.setRange(-10, 50); self.in_temp.setValue(30)
        self.in_hum  = QDoubleSpinBox()
        self.in_hum.setRange(0, 100);   self.in_hum.setValue(70)
        self.in_rain = QDoubleSpinBox()
        self.in_rain.setRange(0, 500);  self.in_rain.setValue(0)
        self.in_cond = QComboBox(); self.in_cond.addItems(CONDITIONS)
        for r, (lbl, w) in enumerate([
            ("Date", self.in_date), ("City", self.in_city),
            ("Temp °C", self.in_temp), ("Humidity %", self.in_hum),
            ("Rainfall mm", self.in_rain), ("Condition", self.in_cond),
        ]):
            addl.addWidget(QLabel(lbl), r, 0)
            addl.addWidget(w, r, 1)
        self.btn_add = QPushButton("➕ Add Record")
        addl.addWidget(self.btn_add, 6, 0, 1, 2)
        ll.addWidget(addg)

        chartg = QGroupBox("Chart")
        chartl = QVBoxLayout(chartg)
        self.btn_chart = QPushButton("📊 Show Rainfall Histogram")
        chartl.addWidget(self.btn_chart)
        ll.addWidget(chartg)

        ll.addStretch()
        self.status = QLabel("Ready — load a file to begin.")
        self.status.setWordWrap(True)
        ll.addWidget(self.status)
        splitter.addWidget(left)

        # ── right panel ──────────────────────────────────────────────────
        right_splitter = QSplitter(Qt.Vertical)

        # top: table + stats
        top_widget = QWidget()
        top_layout = QVBoxLayout(top_widget)

        self.table = QTableWidget()
        self.table.setAlternatingRowColors(True)
        top_layout.addWidget(self.table, stretch=2)

        stats_lbl = QLabel("📈  Statistics")
        stats_lbl.setFont(QFont("Georgia", 11, QFont.Bold))
        top_layout.addWidget(stats_lbl)

        self.stats_container = QWidget()
        self.stats_layout = QVBoxLayout(self.stats_container)
        self.stats_layout.setContentsMargins(0, 0, 0, 0)
        stats_placeholder = QLabel("(load a file to see statistics)")
        stats_placeholder.setAlignment(Qt.AlignCenter)
        stats_placeholder.setStyleSheet("color: gray;")
        self.stats_layout.addWidget(stats_placeholder)
        self.stats_container.setMinimumHeight(160)
        self.stats_container.setMaximumHeight(200)
        top_layout.addWidget(self.stats_container, stretch=1)
        right_splitter.addWidget(top_widget)

        # bottom: chart area
        self.chart_container = QWidget()
        self.chart_layout = QVBoxLayout(self.chart_container)
        chart_placeholder = QLabel("📊  Chart will appear here after clicking 'Show Chart'")
        chart_placeholder.setAlignment(Qt.AlignCenter)
        chart_placeholder.setStyleSheet("color: gray;")
        self.chart_layout.addWidget(chart_placeholder)
        right_splitter.addWidget(self.chart_container)

        right_splitter.setSizes([420, 260])
        splitter.addWidget(right_splitter)
        splitter.setSizes([280, 820])

        self.btn_read_csv.clicked.connect(self._on_read_csv)
        self.btn_read_json.clicked.connect(self._on_read_json)
        self.btn_write_csv.clicked.connect(self._on_write_csv)
        self.btn_write_json.clicked.connect(self._on_write_json)
        self.btn_add.clicked.connect(self._on_add)
        self.btn_chart.clicked.connect(self._on_chart)

    def _check_sample(self):
        if os.path.exists("weather_data.csv"):
            self.status.setText("Ready — click 'Read CSV' to load weather_data.csv")
        else:
            self.status.setText("⚠️  weather_data.csv not found — place it in the same folder.")
    
    def _display(self, df: pd.DataFrame):
        if df.empty:
            self.table.setRowCount(0)
            self.table.setColumnCount(0)
            placeholder = QLabel("No data.")
            placeholder.setAlignment(Qt.AlignCenter)
            self._set_stats(placeholder)
            return
        
        cols = list(df.columns)
        self.table.setColumnCount(len(cols))
        self.table.setHorizontalHeaderLabels(cols)
        self.table.setRowCount(len(df))
        for ri, (_, row) in enumerate(df.iterrows()):
            color = CONDITION_COLORS.get(str(row.get("condition", "")))
            for ci, col in enumerate(cols):
                item = QTableWidgetItem(str(row[col]))
                item.setTextAlignment(Qt.AlignCenter)
                if color:
                    item.setBackground(color)
                self.table.setItem(ri, ci, item)
        self.table.resizeColumnsToContents()

        try:
            # replace this with a function that gets the stat table
            stat_table = build_stats(self.df)
            
            self._set_stats(stat_table)
        except NotImplementedError:
            placeholder = QLabel("(complete TODO 5 to see statistics)")
            placeholder.setAlignment(Qt.AlignCenter)
            placeholder.setStyleSheet("color: gray;")
            self._set_stats(placeholder)

    def _set_stats(self, widget):
        """Replace the stats area with a new QTableWidget."""
        while self.stats_layout.count():
            item = self.stats_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self.stats_layout.addWidget(widget)

    def _set_chart(self, widget):
        """Replace the chart area with a new pyqtgraph PlotWidget."""
        while self.chart_layout.count():
            item = self.chart_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self.chart_layout.addWidget(widget)
        self._chart_widget = widget

    def _on_read_csv(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open CSV", "", "CSV Files (*.csv)")
        if not path: return

        try:
            # replace this with calling a function to get a data frame
            self.df = read_csv(path)
            
            self._display(self.df)
            self.status.setText(f"✅ Loaded {len(self.df)} rows")
        except NotImplementedError:
            self.status.setText("⚠️  Complete TODO 1 first!")
        except Exception as e:
            QMessageBox.critical(self, "Read Error", str(e))

    def _on_read_json(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open JSON", "", "JSON Files (*.json)")
        if not path: return

        try:
            # replace this with calling a function to get a data frame
            self.df = read_json(path)

            self._display(self.df)
            self.status.setText(f"✅ Loaded {len(self.df)} rows")
        except NotImplementedError:
            self.status.setText("⚠️  Complete TODO 2 first!")
        except Exception as e:
            QMessageBox.critical(self, "Read Error", str(e))

    def _on_write_csv(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save CSV", "weather_log.csv", "CSV Files (*.csv)")
        if not path: return

        try:
            # call a function to write a csv file
            write_csv(self.df, path)

            self.status.setText(f"✅ Saved CSV")
        except NotImplementedError:
            self.status.setText("⚠️  Complete TODO 3 first!")
        except Exception as e:
            QMessageBox.critical(self, "Save Error", str(e))

    def _on_write_json(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save JSON", "weather_log.json", "JSON Files (*.json)")
        if not path: return

        try:
            # call a function to write a json file
            write_json(self.df, path)
            
            self.status.setText(f"✅ Saved JSON: {path}")
        except NotImplementedError:
            self.status.setText("⚠️  Complete TODO 4 first!")
        except Exception as e:
            QMessageBox.critical(self, "Save Error", str(e))

    def _on_add(self):
        
        # get data in all input fields and put into the record
        # before putting it into a DF
        record = {
            'date': self.in_date.date().toString("yyyy-MM-dd"),
            'city': self.in_city.currentText(),
            'temp_c': self.in_temp.value(),
            'humidity': self.in_hum.value(),
            'rainfall_mm': self.in_rain.value(),
            'condition': self.in_cond.currentText()
        }

        # put the record into a DF
        new_row = pd.DataFrame([record])

        # concat the new row to the current DF
        self.df = pd.concat([self.df, new_row], ignore_index=True)
        
        self._display(self.df)
        self.status.setText(f"✅ Added: {record['date']} – {record['city']}")

    def _on_chart(self):
        
        try:
            # replace this with calling a function to create a graph widget
            widget = show_chart(self.df, "Rainfall Histogram")

            self._set_chart(widget)
            self.status.setText("✅ Showing: Rainfall Histogram")
        except NotImplementedError:
            self.status.setText("⚠️  Complete TODO 6 first!")
        except Exception as e:
            QMessageBox.critical(self, "Chart Error", str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = WeatherTracker()
    window.show()
    sys.exit(app.exec())
