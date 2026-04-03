"""
Panhathai Suporn
683040496-5
P2
"""

import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QRadioButton, 
                             QButtonGroup, QComboBox, QTextEdit, QCheckBox, 
                             QPushButton, QDateEdit)
from PyQt6.QtCore import QDate, Qt, QLocale

class StudentRegistrationForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("P2: Student Registration")
        self.setMaximumSize(400,600)
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Title
        title = QLabel("Student Registration Form")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        main_layout.addWidget(title)
        
        main_layout.addSpacing(20)
        
        # Full Name
        name_label = QLabel("Full Name:")
        main_layout.addWidget(name_label)
        self.name_edit = QLineEdit()
        main_layout.addWidget(self.name_edit)
        
        main_layout.addSpacing(20)
        
        # Email
        email_label = QLabel("Email:")
        main_layout.addWidget(email_label)
        self.email_edit = QLineEdit()
        main_layout.addWidget(self.email_edit)
        
        main_layout.addSpacing(20)
        
        # Phone
        phone_label = QLabel("Phone:")
        main_layout.addWidget(phone_label)
        self.phone_edit = QLineEdit()
        main_layout.addWidget(self.phone_edit)
        
        main_layout.addSpacing(20)
        
        # Date of Birth
        dob_label = QLabel("Date of Birth (dd/MM/yyyy):")
        main_layout.addWidget(dob_label)
        
        # Create calendar field
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)  # Shows calendar dropdown
        self.date_edit.setDisplayFormat("dd/MM/yyyy")  # Format like "01/01/2000"
        self.date_edit.setDate(QDate(2000, 1, 1))  # Set default date to January 1, 2000
        
        # Force Arabic numerals (0-9) instead of Thai numerals
        self.date_edit.setLocale(QLocale(QLocale.Language.Thai, QLocale.Country.Thailand))
        
        main_layout.addWidget(self.date_edit)
        
        main_layout.addSpacing(20)
        
        # Gender
        gender_label = QLabel("Gender:")
        main_layout.addWidget(gender_label)
        
        # Button group ensures only one can be selected
        self.gender_group = QButtonGroup()
        
        gender_layout = QHBoxLayout()
        
        self.male_radio = QRadioButton("Male")
        self.female_radio = QRadioButton("Female")
        self.nonbinary_radio = QRadioButton("Non-binary")
        self.prefer_not_radio = QRadioButton("Prefer not to say")
        
        self.gender_group.addButton(self.male_radio)
        self.gender_group.addButton(self.female_radio)
        self.gender_group.addButton(self.nonbinary_radio)
        self.gender_group.addButton(self.prefer_not_radio)
        
        gender_layout.addWidget(self.male_radio)
        gender_layout.addWidget(self.female_radio)
        gender_layout.addWidget(self.nonbinary_radio)
        gender_layout.addWidget(self.prefer_not_radio)
        
        main_layout.addLayout(gender_layout)
        
        main_layout.addSpacing(20)
        
        # Program
        program_label = QLabel("Program:")
        main_layout.addWidget(program_label)
        
        self.program_combo = QComboBox()
        self.program_combo.addItem("Select your program")
        self.program_combo.addItem("Computer Engineering")
        self.program_combo.addItem("Digital Media Engineering")
        self.program_combo.addItem("Environmental Engineering")
        self.program_combo.addItem("Electrical Engineering")
        self.program_combo.addItem("Semiconductor Engineering")
        self.program_combo.addItem("Mechanical Engineering")
        self.program_combo.addItem("Industrial Engineering")
        self.program_combo.addItem("Logistic Engineering")
        self.program_combo.addItem("Power Engineering")
        self.program_combo.addItem("Electronic Engineering")
        self.program_combo.addItem("Telecommunication Engineering")
        self.program_combo.addItem("Agricultural Engineering")
        self.program_combo.addItem("Civil Engineering")
        self.program_combo.addItem("ARIS")
        main_layout.addWidget(self.program_combo)
        
        main_layout.addSpacing(20)
        
        # Tell us about yourself
        about_label = QLabel("Tell us a little bit about yourself:")
        main_layout.addWidget(about_label)
        
        self.about_text = QTextEdit()
        self.about_text.setMaximumHeight(100) # Set max height to 100
        main_layout.addWidget(self.about_text)
        
        main_layout.addSpacing(20)
        
        # Terms and conditions checkbox
        self.terms_checkbox = QCheckBox("I accept the terms and conditions.")
        main_layout.addWidget(self.terms_checkbox)
        
        main_layout.addSpacing(20)
        
        # Submit button
        self.submit_button = QPushButton("Submit Registration")
        main_layout.addWidget(self.submit_button)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StudentRegistrationForm()
    window.show()
    sys.exit(app.exec())