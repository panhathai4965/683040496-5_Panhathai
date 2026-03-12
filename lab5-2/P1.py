"""
Panhathai Suporn
683040496-5
"""

import sys
from PySide6.QtWidgets import (QApplication, QMainWindow,
                             QVBoxLayout, QHBoxLayout, QFormLayout, QGridLayout, QWidget, QLabel, QLineEdit)
from PySide6.QtWidgets import QPushButton, QComboBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QDoubleValidator

kg = "kilograms"
lb = "pounds"
cm = "centimeters"
m = "meters"
ft = "feet"
adult = "Adults 20+"
child = "Children and Teenagers (5-19)"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("P1: BMI Calculator")
        self.setGeometry(100, 100, 300, 450)

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Add header
        header = QLabel("Adult and Child BMI Calculator")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet("""
            background-color: #A52A2A;
            color: white;
            padding: 10px;
            font-weight: bold;
            font-size: 13px;
        """)
        main_layout.addWidget(header)

        # Create an input section object
        self.input_section = InputSection()
        main_layout.addWidget(self.input_section)
        
        # create an output section object
        self.output_section = OutputSection()
        main_layout.addWidget(self.output_section)

        # connect signals from clicking submit and clear buttons
        self.input_section.submit_button.clicked.connect(
            lambda: self.input_section.submit_reg(self.output_section)
        )
        self.input_section.clear_button.clicked.connect(
            lambda: self.input_section.clear_form(self.output_section)
        )


class OutputSection(QWidget):
    def __init__(self):
        super().__init__()

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet("OutputSection { background-color: #FAF0E6; }")

        self.layout = QVBoxLayout(self)
        
        # BMI Label
        bmi_label = QLabel("Your BMI")
        bmi_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        bmi_label.setStyleSheet("color: black;")
        self.layout.addWidget(bmi_label)
        
        # BMI Value
        self.bmi_text = QLabel("0.00")
        self.bmi_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.bmi_text.setStyleSheet("color: #6666FF; font-size: 32px; font-weight: bold;")
        self.layout.addWidget(self.bmi_text)
        
        # Adult table container
        self.adult_table = self.show_adult_table()
        self.adult_table.hide()
        self.layout.addWidget(self.adult_table)
        
        # Child links container
        self.child_table = self.show_child_link()
        self.child_table.hide()
        self.layout.addWidget(self.child_table)
        
        self.layout.addStretch()

    def show_adult_table(self):
        container = QWidget()
        table_layout = QGridLayout(container)
        table_layout.setSpacing(5)

        # Headers
        label = QLabel("BMI")
        label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("color: black;")
        table_layout.addWidget(label, 0, 0)
        
        label = QLabel("Condition")
        label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("color: black;")
        table_layout.addWidget(label, 0, 1)
        
        # Data rows
        bmi_ranges = ["< 18.5", "18.5 - 25.0", "25.1 - 30.0", "> 30.0"]
        conditions = ["Thin", "Normal", "Overweight", "Obese"]
        
        for i, (bmi_range, condition) in enumerate(zip(bmi_ranges, conditions), start=1):
            bmi_label = QLabel(bmi_range)
            bmi_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            bmi_label.setStyleSheet("color: black;")
            table_layout.addWidget(bmi_label, i, 0)
            
            cond_label = QLabel(condition)
            cond_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
            cond_label.setStyleSheet("color: black;")
            table_layout.addWidget(cond_label, i, 1)
        
        return container

    def show_child_link(self):
        container = QWidget()
        child_layout = QVBoxLayout(container)
        
        # Message
        message = QLabel("For child's BMI interpretation, please click one of the following links.")
        message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        message.setWordWrap(True)
        message.setStyleSheet("color: black;")
        child_layout.addWidget(message)

        # Links
        link_layout = QHBoxLayout()
        boy_link = QLabel('<a href="https://cdn.who.int/media/docs/default-source/child-growth/growth-reference-5-19-years/bmi-for-age-(5-19-years)/cht-bmifa-boys-z-5-19years.pdf?sfvrsn=4007e921_4">BMI graph for BOYS</a>')
        girl_link = QLabel('<a href="https://cdn.who.int/media/docs/default-source/child-growth/growth-reference-5-19-years/bmi-for-age-(5-19-years)/cht-bmifa-girls-z-5-19years.pdf?sfvrsn=c708a56b_4">BMI graph for GIRLS</a>')
        boy_link.setOpenExternalLinks(True)
        girl_link.setOpenExternalLinks(True)
        boy_link.setAlignment(Qt.AlignmentFlag.AlignCenter)
        girl_link.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        link_layout.addWidget(boy_link)
        link_layout.addWidget(girl_link)
        child_layout.addLayout(link_layout)

        return container
        

    def update_results(self, bmi, age_group):
        # Update BMI value
        self.bmi_text.setText(f"{bmi:.2f}")
        
        # Show appropriate table based on age group
        if age_group == adult:
            self.adult_table.show()
            self.child_table.hide()
        else:
            self.adult_table.hide()
            self.child_table.show()
    
    def clear_result(self):
        self.bmi_text.setText("0.00")
        self.adult_table.hide()
        self.child_table.hide()


class InputSection(QWidget):

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)
        
        # Age group selection
        age_layout = QHBoxLayout()
        age_label = QLabel("BMI age group:")
        age_label.setFixedWidth(95)
        self.age_combo = QComboBox()
        self.age_combo.addItems([adult, child])
        age_layout.addWidget(age_label)
        age_layout.addWidget(self.age_combo)
        self.layout.addLayout(age_layout)
        
        # Weight input
        weight_layout = QHBoxLayout()
        weight_label = QLabel("Weight:")
        weight_label.setFixedWidth(95)
        self.weight_input = QLineEdit()
        # Set input weight 0 - 999.99
        weight_validator = QDoubleValidator(0.0, 999.99, 2)
        weight_validator.setNotation(QDoubleValidator.Notation.StandardNotation)
        self.weight_input.setValidator(weight_validator)
        self.weight_unit = QComboBox()
        self.weight_unit.addItems([kg, lb])
        self.weight_unit.setFixedWidth(100)
        weight_layout.addWidget(weight_label)
        weight_layout.addWidget(self.weight_input)
        weight_layout.addWidget(self.weight_unit)
        self.layout.addLayout(weight_layout)
        
        # Height input
        height_layout = QHBoxLayout()
        height_label = QLabel("Height:")
        height_label.setFixedWidth(95)
        self.height_input = QLineEdit()
        # ตั้งค่าให้รับเฉพาะตัวเลขบวก (0.0 ถึง 999.99)
        height_validator = QDoubleValidator(0.0, 999.99, 2)
        height_validator.setNotation(QDoubleValidator.Notation.StandardNotation)
        self.height_input.setValidator(height_validator)
        self.height_unit = QComboBox()
        self.height_unit.addItems([cm, m, ft])
        self.height_unit.setFixedWidth(100)
        height_layout.addWidget(height_label)
        height_layout.addWidget(self.height_input)
        height_layout.addWidget(self.height_unit)
        self.layout.addLayout(height_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.clear_button = QPushButton("clear")
        self.submit_button = QPushButton("Submit Registration")
        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.submit_button)
        self.layout.addLayout(button_layout)

    def clear_form(self, output_section):
        # clear input form
        self.weight_input.clear()
        self.height_input.clear()
        self.age_combo.setCurrentIndex(0)
        self.weight_unit.setCurrentIndex(0)
        self.height_unit.setCurrentIndex(0)

        # clear output section
        output_section.clear_result()

    def submit_reg(self, output_section):
        try:
            # Calculate BMI
            bmi = self.calculate_BMI()
            
            # Get age group
            age_group = self.age_combo.currentText()
            
            # Update output section
            output_section.update_results(bmi, age_group)
            
        except ValueError:
            # If invalid input, show 0.00
            output_section.clear_result()

    def calculate_BMI(self):
        # Get input values
        weight = float(self.weight_input.text())
        height = float(self.height_input.text())
        
        # Convert weight to kilograms if needed
        if self.weight_unit.currentText() == lb:
            weight = weight * 0.453592  # pounds to kg
        
        # Convert height to meters if needed
        if self.height_unit.currentText() == cm:
            height = height / 100  # cm to meters
        elif self.height_unit.currentText() == ft:
            height = height * 0.3048  # feet to meters
        # If already in meters, no conversion needed
        
        # Calculate BMI: weight (kg) / height (m)^2
        bmi = weight / (height ** 2)
        
        return bmi


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()