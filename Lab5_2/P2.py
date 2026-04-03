"""
Panhathai Suporn
683040496-5
P2
"""

import sys
from PySide6.QtWidgets import (QApplication, QMainWindow,
                             QVBoxLayout, QWidget, QHBoxLayout,
                             QGridLayout, QFormLayout, QLineEdit,
                             QSpinBox, QPushButton, QLabel, QTextEdit)

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QFont
import math

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Calculator")
        self.setCentralWidget(CalculatorLayout())
        self.resize(300, 500)


class CalculatorLayout(QWidget):
    def __init__(self):
        super().__init__()
        layout = QGridLayout()

        text = QLabel("Standard")
        text.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(text, 0, 1)

        self.display = QLineEdit()
        self.display.setAlignment(Qt.AlignRight)
        self.display.setText("0")
        self.display.setFont(QFont("Arial", 40))
        layout.addWidget(self.display, 1, 0, 2, 4)

        self.setStyleSheet("""
            QPushButton {
                min-width: 60px;
                min-height: 35px;
                font-size: 16px;
            }
        """)

        # function buttons
        button_manu = QPushButton("☰")
        button_percent = QPushButton("%")
        button_percent.clicked.connect(lambda: self.op("%"))
        button_CE = QPushButton("CE")
        button_C = QPushButton("C")
        button_C.clicked.connect(self.reset_zero)
        button_back = QPushButton("⌫")
        button_back.clicked.connect(self.back_spec)
        button_inv = QPushButton("1/x")
        button_inv.clicked.connect(self.divis_x)
        button_square = QPushButton("x²")
        button_square.clicked.connect(self.square_x)
        button_sqrt = QPushButton("√x")
        button_sqrt.clicked.connect(self.sqrt)
        layout.addWidget(button_manu, 0,  0)
        layout.addWidget(button_percent, 3, 0)
        layout.addWidget(button_CE, 3, 1)
        layout.addWidget(button_C, 3, 2)
        layout.addWidget(button_back, 3, 3)
        layout.addWidget(button_inv, 4, 0)
        layout.addWidget(button_square, 4, 1)
        layout.addWidget(button_sqrt, 4, 2)

        # Number buttons with signal connections
        button1 = QPushButton("1")
        button1.clicked.connect(lambda: self.append_value("1"))
        button2 = QPushButton("2")
        button2.clicked.connect(lambda: self.append_value("2"))
        button3 = QPushButton("3")
        button3.clicked.connect(lambda: self.append_value("3"))
        button4 = QPushButton("4")
        button4.clicked.connect(lambda: self.append_value("4"))
        button5 = QPushButton("5")
        button5.clicked.connect(lambda: self.append_value("5"))
        button6 = QPushButton("6")
        button6.clicked.connect(lambda: self.append_value("6"))
        button7 = QPushButton("7")
        button7.clicked.connect(lambda: self.append_value("7"))
        button8 = QPushButton("8")
        button8.clicked.connect(lambda: self.append_value("8"))
        button9 = QPushButton("9")
        button9.clicked.connect(lambda: self.append_value("9"))
        button0 = QPushButton("0")
        button0.clicked.connect(lambda: self.append_value("0"))
        layout.addWidget(button1, 7, 0)
        layout.addWidget(button2, 7, 1)
        layout.addWidget(button3, 7, 2)
        layout.addWidget(button4, 6, 0)
        layout.addWidget(button5, 6, 1)
        layout.addWidget(button6, 6, 2)
        layout.addWidget(button7, 5, 0)  # row 0, col 0
        layout.addWidget(button8, 5, 1)  # row 0, col 1
        layout.addWidget(button9, 5, 2)  # row 0, col 2
        layout.addWidget(button0, 8, 1)

        # Other function buttons
        button_dot = QPushButton(".")
        button_dot.clicked.connect(lambda: self.append_value("."))
        button_divide = QPushButton("/")
        button_divide.clicked.connect(lambda: self.op("/"))
        button_multiply = QPushButton("x")
        button_multiply.clicked.connect(lambda: self.op("x"))
        button_subtract = QPushButton("-")
        button_subtract.clicked.connect(lambda: self.op("-"))
        button_plus = QPushButton("+")
        button_plus.clicked.connect(lambda: self.op("+"))
        button_equals = QPushButton("=")
        button_equals.clicked.connect(self.calculate)
        button_plus_minus = QPushButton("+/-")
        button_plus_minus.clicked.connect(self.plus_minus)
        layout.addWidget(button_dot, 8, 2) 
        layout.addWidget(button_divide, 4, 3)
        layout.addWidget(button_multiply, 5, 3) 
        layout.addWidget(button_subtract, 6, 3) 
        layout.addWidget(button_plus, 7, 3) 
        layout.addWidget(button_equals, 8, 3)  
        layout.addWidget(button_plus_minus, 8, 0)

        # Spacing and margins
        layout.setSpacing(0)
        layout.setContentsMargins(5, 5, 5, 5)

        # Column/Row stretch
        #layout.setColumnStretch(0, 1)  # First column stretches more
        #layout.setRowStretch(1, 2)     # Second row stretches more
        self.setLayout(layout)

    def append_value(self, value):
        current_text = self.display.text()
        if current_text == "0":
            self.display.setText(value)
        else:
            self.display.setText(current_text + value)

    def reset_zero(self):
        self.current_display = "0"
        self.display.setText(self.current_display)
    
    def back_spec(self):
        current_text = self.display.text()
        if len(current_text) > 1:
            self.display.setText(current_text[:-1])
        else:
            self.display.setText("0")

    def op(self, operator):
        current_text = self.display.text()
        if current_text[-1] in "+-x/":
            current_text = current_text[:-1]
        self.display.setText(current_text +""+operator+"")
    
    def calculate(self):
        expression = self.display.text()
        expression.split()
        try:
            a, op, b = expression.partition(next((c for c in expression if c in "+-x/%"), None))
        except ValueError:
            a, op = expression
            b = a

        if "." in a:
            a = float(a)
        else:
            a = int(a)
        if "." in b:
            b = float(b)
        else:
            b = int(b)
        
        result = 0

        """if op == "+":
            result = a + b
        elif op == "-":
            result = a - b
        elif op == "x":
            result = a * b
        elif op == "/":
            try:
                result = a // b
            except ZeroDivisionError as e:
                result = f"{e}"
        elif op == "%":
            try:
                result = a // b
            except ZeroDivisionError as e:
                result = f"{e}" """
        if op == "/":
            try:
                result = a // b
            except ZeroDivisionError as e:
                result = f"{e}"
        elif op == "%":
            try:
                result = a / b
            except ZeroDivisionError as e:
                result = f"{e}"
        elif op == "x":
            result = a * b
        else:
            result = eval(expression)
        self.display.setText(str(result))
        return self.display.setText(str(result))
    
    def divis_x(self):
        x = self.display.text()
        x.split()
        if "." in x:
            x = float(x)
        else:
            x = int(x)
        result = 1 / x
        return self.display.setText(str(result))
    
    def square_x(self):
        x = self.display.text()
        x.split()
        if "." in x:
            x = float(x)
        else:
            x = int(x)
        result = x**2
        return self.display.setText(str(result))
    
    def sqrt(self):
        x = self.display.text()
        x.split()
        if "." in x:
            x = float(x)
        else:
            x = int(x)
        result = math.sqrt(x)
        return self.display.setText(str(result))
    
    def plus_minus(self):
        x = self.display.text()
        x.split()
        if "." in x:
            x = float(x)
        else:
            x = int(x)
        result = x * -1
        return self.display.setText(str(result))

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())