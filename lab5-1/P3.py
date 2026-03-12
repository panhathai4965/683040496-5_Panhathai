"""""
Panhathai Suporn
683040496-5
"""""

import sys
from PySide6.QtWidgets import (QApplication, QMainWindow,
                                QVBoxLayout, QWidget, QHBoxLayout,
                                QGridLayout, QFormLayout, QLineEdit,
                                QLabel,QPushButton,QButtonGroup,
                                QRadioButton,QDateEdit,QComboBox,
                                QCheckBox,QTextEdit,QGroupBox) #  GUI

from PySide6.QtCore import Qt, QSize, QDate # 
from PySide6.QtGui import QPixmap, QFont 


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("P3")
        self.setGeometry(100, 100, 280, 500)

        #color: black; 
        #background-color: #F2F2F2; 
        #border: 1px solid #999; 
        #border-radius: 6px; 
        #padding: 10px; 
        #min-width: 40px; 
        #max-height: 40px;

        self.setStyleSheet("""
            QMainWindow {
                background-color: #F2F2F2;
            }
            QLabel {
                color: #000000;
            }
            QLabel#title {
                color: #ffffff;
                background-color: #A73B24;
                padding: 4px;
                border-radius: 3px;
            }
            QLabel#answer {
                color: #343434;
            }
            QPushButton {
                color: black;
                background-color: #F2F2F2;
                border: 1px solid #999;
                border-radius: 3px; 
                padding: 5px; 
            }
            QPushButton:hover {
                background-color: #f5f5f5;
            }
            QPushButton:pressed {
                background-color: #e0e0e0;
            }
            QLineEdit {
                background-color: #ffffff;
                color: #F2F2F2;
                border: 1px solid #666;
                padding: 5px;
                border-radius: 2px;
            }
            QComboBox {
                background-color: #F2F2F2;
                color: black;
                border: 1px solid #666;
                padding: 3px 5px;
                border-radius: 2px;                     
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                color: black;
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 6px solid white;
                margin-right: 5px;
            }
            QComboBox QAbstractItemView {
                background-color: #4a4a4a;
                color: white;
                selection-background-color: #666;
            }
            QGroupBox {
                border: 1px solid #999;
                border-radius: 5px;
                margin-top: 10px;
                background-color: white;
                padding: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 5px;
                color: #000000;
            }
        """)

        central_widget = QWidget() 
        self.setCentralWidget(central_widget) 
        layout = QVBoxLayout(central_widget) 

        layout.setSpacing(5) 
        layout.setContentsMargins(2, 2, 2, 2)  

        title = QLabel("Adult and Child BMI Calculator")
        title.setObjectName("title")
        title.setFont(QFont("Arial", 10, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        layout.addWidget(title)
        layout.addSpacing(10)

          
        group_cal = QHBoxLayout()
        group_cal.addStretch()

        Calculate_BMI_text = QLabel("Calculate BMI for")
        Calculate_BMI_text.setFont(QFont("Arial", 10))
        group_cal.addWidget(Calculate_BMI_text)

        Calculate_BMI = QComboBox()
        Calculate_BMI.addItems(sorted(["Adult Age 20+", "Child Age <20"]))
        Calculate_BMI.setFixedSize(110, 25)
        group_cal.addWidget(Calculate_BMI)

        group_cal.addStretch()
        layout.addLayout(group_cal)
        layout.addSpacing(10)

        
        group_weight = QHBoxLayout()
        group_weight.addStretch()

        weight_text = QLabel("Weight:")
        weight_text.setFont(QFont("Arial", 10))
        group_weight.addWidget(weight_text)

        weight = QLineEdit()
        weight.setFont(QFont("Arial", 10))
        weight.setFixedSize(55, 25)
        group_weight.addWidget(weight)

        weight_unit = QComboBox()
        weight_unit.addItems(sorted(["pounds", "kg"]))
        weight_unit.setCurrentText("pounds")
        weight_unit.setFixedSize(90, 25)
        group_weight.addWidget(weight_unit)

        group_weight.addStretch()
        layout.addLayout(group_weight)
        layout.addSpacing(5)

       
        group_height = QHBoxLayout()
        group_height.addStretch()

        height_text = QLabel("Height:")
        height_text.setFont(QFont("Arial", 10))
        group_height.addWidget(height_text)

        height = QLineEdit()
        height.setFont(QFont("Arial", 10))
        height.setFixedSize(55, 25)
        group_height.addWidget(height)

        height_unit = QComboBox()
        height_unit.addItems(sorted(["feet", "cm"]))
        height_unit.setCurrentText("feet")
        height_unit.setFixedSize(90, 25)
        group_height.addWidget(height_unit)

        group_height.addStretch()
        layout.addLayout(group_height)
        layout.addSpacing(5)

      
        group_inches = QHBoxLayout()
        group_inches.addStretch()

        inches = QLineEdit()
        inches.setFont(QFont("Arial", 10))
        inches.setFixedSize(55, 25)
        group_inches.addWidget(inches)

        inches_text = QLabel("inches")
        inches_text.setFont(QFont("Arial", 10))
        group_inches.addWidget(inches_text)
        group_inches.addSpacing(5)

        group_inches.addStretch()
        layout.addLayout(group_inches)
        layout.addSpacing(10)

     
        group_button = QHBoxLayout()
        
        group_button.addSpacing(5)
        clear_button = QPushButton("Clear")
        clear_button.setFont(QFont("Arial", 10))
        clear_button.setFixedSize(55, 30)
        group_button.addWidget(clear_button)

        group_button.addStretch()

        calculate_button = QPushButton("Calculate")
        calculate_button.setFont(QFont("Arial", 10))
        calculate_button.setMinimumSize(80, 30)
        group_button.addWidget(calculate_button)
        group_button.addSpacing(5)

        layout.addLayout(group_button)
        layout.addSpacing(-10)

       
        answer_group = QGroupBox()
        answer_layout = QVBoxLayout()

        answer_group.setMinimumHeight(280)

        answer_text = QLabel("Answer:")
        answer_text.setObjectName("answer")
        answer_text.setFont(QFont("Arial", 10))
        answer_text.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        answer_layout.addWidget(answer_text)

        bmi_text = QLabel("BMI =")
        bmi_text.setFont(QFont("Arial", 10, QFont.Bold))
        bmi_text.setAlignment(Qt.AlignCenter)
        answer_layout.addWidget(bmi_text)
        answer_layout.addSpacing(10)

        adult_bmi_text = QLabel("Adult BMI")
        adult_bmi_text.setFont(QFont("Arial", 10, QFont.Bold))
        adult_bmi_text.setAlignment(Qt.AlignCenter)
        answer_layout.addWidget(adult_bmi_text)
        answer_layout.addSpacing(5)
        
        grid_bmi = QGridLayout()
        grid_bmi.setSpacing(0) 
        grid_bmi.setAlignment(Qt.AlignCenter)

        bmi_head = QLabel("BMI")
        bmi_head.setFont(QFont("Arial", 10, QFont.Bold))
        bmi_head.setAlignment(Qt.AlignCenter)
        bmi_head.setStyleSheet("background-color: #f0f0f0; border: 1px solid #999; padding: 5px;")
        bmi_head.setMinimumHeight(35)
        bmi_head.setMaximumWidth(80)
        grid_bmi.addWidget(bmi_head, 0, 0)

        status_head = QLabel("Status")
        status_head.setObjectName("head")
        status_head.setFont(QFont("Arial", 10, QFont.Bold))
        status_head.setAlignment(Qt.AlignCenter)
        status_head.setStyleSheet("background-color: #f0f0f0; border: 1px solid #999; padding: 5px;")
        status_head.setMinimumHeight(35)
        status_head.setMaximumWidth(100)
        grid_bmi.addWidget(status_head, 0, 1)

        underweight_bmi = QLabel("≤ 18.4")
        underweight_bmi.setFont(QFont("Arial", 10))
        underweight_bmi.setAlignment(Qt.AlignLeft)
        underweight_bmi.setStyleSheet("background-color: #ffd966; border: 1px solid #999; padding: 5px;")
        underweight_bmi.setMinimumHeight(35)
        underweight_bmi.setMaximumWidth(80)
        grid_bmi.addWidget(underweight_bmi, 1, 0)

        underweight_status = QLabel("Underweight")
        underweight_status.setFont(QFont("Arial", 10))
        underweight_status.setAlignment(Qt.AlignLeft)
        underweight_status.setStyleSheet("background-color: #ffffff; border: 1px solid #999; padding: 5px;")
        underweight_status.setMinimumHeight(35)
        underweight_status.setMaximumWidth(100)
        grid_bmi.addWidget(underweight_status, 1, 1)

        normal_bmi = QLabel("18.5 - 24.9")
        normal_bmi.setFont(QFont("Arial", 10))
        normal_bmi.setAlignment(Qt.AlignLeft)
        normal_bmi.setStyleSheet("background-color: #93c47d; border: 1px solid #999; padding: 5px;")
        normal_bmi.setMinimumHeight(35)
        normal_bmi.setMaximumWidth(80)
        grid_bmi.addWidget(normal_bmi, 2, 0)

        normal_status = QLabel("Normal")
        normal_status.setFont(QFont("Arial", 10))
        normal_status.setAlignment(Qt.AlignLeft)
        normal_status.setStyleSheet("background-color: #ffffff; border: 1px solid #999; padding: 5px;")
        normal_status.setMinimumHeight(35)
        grid_bmi.addWidget(normal_status, 2, 1)

      
        overweight_bmi = QLabel("25.0 - 39.9")
        overweight_bmi.setFont(QFont("Arial", 10))
        overweight_bmi.setAlignment(Qt.AlignLeft)
        overweight_bmi.setStyleSheet("background-color: #f6b26b; border: 1px solid #999; padding: 5px;")
        overweight_bmi.setMinimumHeight(35)
        overweight_bmi.setMaximumWidth(80)
        grid_bmi.addWidget(overweight_bmi, 3, 0)

        overweight_status = QLabel("Overweight")
        overweight_status.setFont(QFont("Arial", 10))
        overweight_status.setAlignment(Qt.AlignLeft)
        overweight_status.setStyleSheet("background-color: #ffffff; border: 1px solid #999; padding: 5px;")
        overweight_status.setMinimumHeight(35)
        grid_bmi.addWidget(overweight_status, 3, 1)

        # Row 4 - Obese
        obese_bmi = QLabel("≥ 40.0")
        obese_bmi.setFont(QFont("Arial", 10))
        obese_bmi.setAlignment(Qt.AlignLeft)
        obese_bmi.setStyleSheet("background-color: #e06666; border: 1px solid #999; padding: 5px;")
        obese_bmi.setMinimumHeight(35)
        obese_bmi.setMaximumWidth(80)
        grid_bmi.addWidget(obese_bmi, 4, 0)

        obese_status = QLabel("Obese")
        obese_status.setFont(QFont("Arial", 10))
        obese_status.setAlignment(Qt.AlignLeft)
        obese_status.setStyleSheet("background-color: #ffffff; border: 1px solid #999; padding: 5px; ")
        obese_status.setMinimumHeight(35)
        grid_bmi.addWidget(obese_status, 4, 1)

        answer_layout.addLayout(grid_bmi)
        answer_group.setLayout(answer_layout)
        layout.addWidget(answer_group)


        layout.addStretch()
def main():
    app = QApplication(sys.argv) 
    window = MainWindow() 
    window.show() 
    sys.exit(app.exec()) 

if __name__ == "__main__":
    main()