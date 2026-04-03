"""""
Panhathai Suporn
683040496-5
P1
"""""

from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QLabel, QLineEdit, QPushButton,
                               QTableWidget, QTableWidgetItem, QSpinBox, QComboBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
import sys
import os

student_path = os.path.join(os.path.dirname(__file__), "students.txt")
with open(student_path, "r", encoding="utf-8") as student:
    student_dict = {}
    for i in student:
        id, name = i.split(",")
        student_dict[id.strip()] = name.strip()

class InventoryApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("P1: Student scores and grades")
        self.setGeometry(100, 100, 1100, 600)
        self.setStyleSheet("""
            QPushButton {
                background-color: #4a9eda;
                color: white;
                font-weight: bold;
                padding: 7px;
                font-size: 14px;
            }
            QPushButton:hover { background-color: #357ab8; }
            QHeaderView::section {
                background-color: #4a9eda;
                color: white;
                font-weight: bold;
                padding: 5px;
            }
        """)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        input_layout = QHBoxLayout()
        student_id_label = QLabel("Student ID:")
        self.student_id = QComboBox()
        self.student_id.setPlaceholderText("Enter Student ID")
        self.student_id.addItems(student_dict.keys())
        self.student_id.currentTextChanged.connect(self.on_id_changed)
        input_layout.addWidget(student_id_label)
        input_layout.addWidget(self.student_id)
        student_name = QLabel("Student Name:")
        self.student_name_input = QLineEdit()
        input_layout.addWidget(student_name)
        input_layout.addWidget(self.student_name_input)
        math = QLabel("Math:")
        self.math = QSpinBox()
        self.math.setMinimum(0)
        self.math.setMaximum(100)
        self.math.setValue(0)
        input_layout.addWidget(math)
        input_layout.addWidget(self.math)
        science = QLabel("Science:")
        self.science = QSpinBox()
        self.science.setMinimum(0)
        self.science.setMaximum(100)
        self.science.setValue(0)
        input_layout.addWidget(science)
        input_layout.addWidget(self.science)
        English = QLabel("English:")
        self.english = QSpinBox()
        self.english.setMinimum(0)
        self.english.setMaximum(100)
        self.english.setValue(0)
        input_layout.addWidget(English)
        input_layout.addWidget(self.english)
        input_layout.addStretch()
        main_layout.addLayout(input_layout)
        self.table = QTableWidget(0, 8)
        self.table.setHorizontalHeaderLabels(
            ["Student ID", "Name", "Math", "Science", "English", "Total", "Average", "Grade"]
        )
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        main_layout.addWidget(self.table)
        button_layout = QHBoxLayout()
        main_layout.addLayout(button_layout)
        add_button = QPushButton("Add Student")
        add_button.clicked.connect(self.add_student)
        button_layout.addWidget(add_button)
        reset_button = QPushButton("Reset input")
        reset_button.clicked.connect(self.reset_input)
        button_layout.addWidget(reset_button)
        clear_button = QPushButton("Clear All")
        clear_button.clicked.connect(self.clear_all)
        button_layout.addWidget(clear_button)
        
    def on_id_changed(self, text):
        if text in student_dict:
            self.student_name_input.setText(student_dict[text])
        else:
            self.student_name_input.clear()
    def get_grade(self, average):
        if average >= 80: return "A"
        elif average >= 75: return "B"
        elif average >= 65: return "C"
        elif average >= 50: return "D"
        else: return "F"
    def get_grade_color(self, grade):
        return {
            "A": QColor("#90EE90"),
            "B": QColor("#ADD8E6"),
            "C": QColor("#FFFFE0"),
            "D": QColor("#FFD580"),
            "F": QColor("#FFB6B6"),
        }.get(grade, QColor("white"))
    def add_student(self):
        sid = self.student_id.currentText()
        name = self.student_name_input.text().strip()
        if not sid or not name:
            return
        math = self.math.value()
        science = self.science.value()
        english = self.english.value()
        total = math + science + english
        average = total / 3
        grade = self.get_grade(average)
        color = self.get_grade_color(grade)
        row = self.table.rowCount()
        self.table.insertRow(row)
        for col, val in enumerate([sid, name, math, science, english, total, f"{average:.2f}", grade]):
            item = QTableWidgetItem(str(val))
            item.setTextAlignment(Qt.AlignCenter)
            if col == 7:
                item.setBackground(color)
            self.table.setItem(row, col, item)
        self.table.sortItems(0, Qt.AscendingOrder)
    def reset_input(self):
        self.student_id.setCurrentIndex(-1)
        self.student_name_input.clear()
        self.math.setValue(0)
        self.science.setValue(0)
        self.english.setValue(0)
    def clear_all(self):
        self.table.setRowCount(0)
        self.reset_input()
def main():
    app = QApplication(sys.argv)
    window = InventoryApp()
    window.show()
    sys.exit(app.exec())
if __name__ == "__main__":
    main()