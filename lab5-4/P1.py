from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QFormLayout,
                               QHBoxLayout, QLabel, QComboBox, QLineEdit, QPushButton,
                               QFrame, QSpinBox, QColorDialog, QFileDialog, QToolBar)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QAction, QIcon, QPixmap
import sys, os
import pyperclip # อย่าลืม pip install pyperclip

default_color = "#B0E0E6"

class PersonalCard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("P1: Personal Info Card")
        self.setMinimumSize(400, 600)

        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout(central_widget)

        # 1. Input Section
        self.input_container = QWidget()
        self.input_layout = QFormLayout(self.input_container)
        self.input_layout.setVerticalSpacing(12)
        self.create_form()
        self.main_layout.addWidget(self.input_container)

        # Separator Line
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        line.setStyleSheet("background-color: #cccccc;")
        self.main_layout.addWidget(line)

        # 2. Output Section (Display Card)
        self.bg_widget = QWidget()
        self.output_layout = QVBoxLayout(self.bg_widget)
        self.create_display()
        self.main_layout.addWidget(self.bg_widget)

        # Components
        self.create_menu()
        self.create_toolbar()

        # Status Bar initial message
        self.statusBar().showMessage("Fill in your details and click generate")

    def create_form(self):
        # Full name: แสดง "First name and Lastname"
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("First name and Lastname")
        
        # Age: ตั้งค่าเริ่มต้นเป็น 25
        self.age_input = QSpinBox()
        self.age_input.setRange(1, 120)
        self.age_input.setValue(25)
        
        # Email: แสดง "username@domain.name"
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("username@domain.name")
        
        # Position: แสดง "Choose your position"
        self.position_input = QComboBox()
        self.position_input.addItems(["Teaching Staff", "Supporting Staff", "Student", "Visitor"])
        self.position_input.setCurrentIndex(-1) # ไม่เลือกค่าเริ่มต้น เพื่อให้ Placeholder แสดง
        self.position_input.setPlaceholderText("Choose your position")

        # Color Picker Row
        color_row = QWidget()
        color_layout = QHBoxLayout(color_row)
        color_layout.setContentsMargins(0, 0, 0, 0)
        self.fav_color = QColor(default_color)
        self.color_swatch = QLabel()
        self.color_swatch.setFixedSize(22, 22)
        self.color_swatch.setStyleSheet(f"background-color: {self.fav_color.name()}; border: 1px solid #888;")
        
        color_button = QPushButton("Pick New Color")
        color_button.clicked.connect(self.pick_color)
        
        color_layout.addWidget(self.color_swatch)
        color_layout.addWidget(color_button)
        color_layout.addStretch()

        # Add to Form
        self.input_layout.addRow("Full name:", self.name_input)
        self.input_layout.addRow("Age:", self.age_input)
        self.input_layout.addRow("Email:", self.email_input)
        self.input_layout.addRow("Position:", self.position_input)
        self.input_layout.addRow("Your favorite color:", color_row)

    def create_display(self):
        self.bg_widget.setObjectName("cardDisplay")
        self.bg_widget.setStyleSheet(f"background-color: {default_color}; border-radius: 6px;")

        self.name_label = QLabel("Your name here")
        self.name_label.setStyleSheet("font-size: 18pt; font-weight: bold; border: none;")
        
        self.age_label = QLabel("(Age)")
        self.age_label.setStyleSheet("border: none;")
        
        self.position_label = QLabel("Your position here")
        self.position_label.setStyleSheet("font-size: 14pt; border: none;")
        
        email_container = QHBoxLayout()
        self.email_icon = QLabel()
        # ตรวจสอบว่ามีไฟล์ mail.png หรือไม่ ถ้าไม่มีจะข้ามไป
        if os.path.exists("mail.png"):
            self.email_icon.setPixmap(QPixmap("mail.png").scaled(18, 18, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        
        self.email_label = QLabel("your_username@domain.name")
        self.email_label.setStyleSheet("border: none;")
        
        email_container.addWidget(self.email_icon)
        email_container.addWidget(self.email_label)
        email_container.addStretch()

        self.output_layout.addWidget(self.name_label)
        self.output_layout.addWidget(self.age_label)
        self.output_layout.addSpacing(10)
        self.output_layout.addWidget(self.position_label)
        self.output_layout.addLayout(email_container)
        self.output_layout.addStretch()

    def pick_color(self):
        color = QColorDialog.getColor(self.fav_color, self, "Pick a Color")
        if color.isValid():
            self.fav_color = color
            self.color_swatch.setStyleSheet(f"background-color: {self.fav_color.name()}; border: 1px solid #888;")
            # อัปเดตสีพื้นหลังของ Card ทันทีถ้าต้องการให้ interactive มากขึ้น
            self.bg_widget.setStyleSheet(f"background-color: {self.fav_color.name()}; border-radius: 6px;")

    def update_display(self):
        name = self.name_input.text() if self.name_input.text() else "Your name here"
        age = f"({self.age_input.value()})"
        pos = self.position_input.currentText() if self.position_input.currentIndex() != -1 else "Your position here"
        email = self.email_input.text() if self.email_input.text() else "your_username@domain.name"

        self.name_label.setText(name)
        self.age_label.setText(age)
        self.position_label.setText(pos)
        self.email_label.setText(email)
        self.bg_widget.setStyleSheet(f"background-color: {self.fav_color.name()}; border-radius: 6px;")
        
        self.statusBar().showMessage("Card generated successfully")

    def clear_form(self):
        self.name_input.clear()
        self.age_input.setValue(25)
        self.email_input.clear()
        self.position_input.setCurrentIndex(-1)
        self.fav_color = QColor(default_color)
        self.color_swatch.setStyleSheet(f"background-color: {default_color}; border: 1px solid #888;")
        self.statusBar().showMessage("Form cleared")

    def clear_display(self):
        self.name_label.setText("Your name here")
        self.age_label.setText("(Age)")
        self.position_label.setText("Your position here")
        self.email_label.setText("your_username@domain.name")
        self.bg_widget.setStyleSheet(f"background-color: {default_color}; border-radius: 6px;")
        self.statusBar().showMessage("Display cleared")

    def clear_all(self):
        self.clear_form()
        self.clear_display()
        self.statusBar().showMessage("All cleared")

    def save_card(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save Card", "my_card.txt", "Text Files (*.txt)")
        if filename:
            with open(filename, "w", encoding="utf-8") as f:
                content = f"{self.name_label.text()}\n{self.age_label.text()}\n{self.position_label.text()}\nEmail: {self.email_label.text()}"
                f.write(content)
            self.statusBar().showMessage(f"Card saved to {os.path.basename(filename)}")

    def copy_card(self):
        content = f"{self.name_label.text()}\n{self.age_label.text()}\n{self.position_label.text()}\nEmail: {self.email_label.text()}"
        pyperclip.copy(content)
        self.statusBar().showMessage("Card copied to clipboard")

    def create_menu(self):
        menu_bar = self.menuBar()
        
        # File Menu
        file_menu = menu_bar.addMenu("File")
        
        gen_action = QAction("Generate Card", self)
        gen_action.triggered.connect(self.update_display)
        
        save_action = QAction("Save Card", self)
        save_action.triggered.connect(self.save_card)
        
        clear_disp_action = QAction("Clear Display", self)
        clear_disp_action.triggered.connect(self.clear_display)
        
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)

        file_menu.addActions([gen_action, save_action, clear_disp_action])
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

        # Edit Menu
        edit_menu = menu_bar.addMenu("Edit")
        
        copy_action = QAction("Copy Card", self)
        copy_action.triggered.connect(self.copy_card)
        
        clear_form_action = QAction("Clear Form", self)
        clear_form_action.triggered.connect(self.clear_form)
        
        edit_menu.addActions([copy_action, clear_form_action])

    def create_toolbar(self):
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)

        # Generate Action (ใช้วงกลมสีเขียวหรือไอคอนที่คุณมี)
        gen_act = QAction("Generate", self)
        gen_act.triggered.connect(self.update_display)
        # ลองใส่ Text เป็นไอคอนจำลองถ้าไม่มีไฟล์รูป
        gen_act.setText("▶") 
        
        # Save Action
        save_act = QAction("Save", self)
        save_act.triggered.connect(self.save_card)
        save_act.setText("💾")

        # Clear All Action
        clear_act = QAction("Clear All", self)
        clear_act.triggered.connect(self.clear_all)
        clear_act.setText("🗑")

        toolbar.addActions([gen_act, save_act, clear_act])

def main():
    app = QApplication(sys.argv)
    
    # พยายามโหลดไฟล์ CSS ถ้ามี
    if os.path.exists("P1_style.qss"):
        with open("P1_style.qss", "r") as f:
            app.setStyleSheet(f.read())
    else:
        # สไตล์เบื้องต้นถ้าไม่มีไฟล์ .qss
        app.setStyleSheet("""
            QMainWindow { background-color: #f0f0f0; }
            QLineEdit, QSpinBox, QComboBox { padding: 5px; border: 1px solid #ccc; border-radius: 4px; }
            QPushButton { padding: 5px 15px; }
        """)

    window = PersonalCard()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()