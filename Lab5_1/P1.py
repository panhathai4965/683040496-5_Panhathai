"""
Panhathai Suporn
683040496-5
P1
"""

import sys
from PySide6.QtWidgets import (QApplication, QMainWindow,
                                QVBoxLayout, QWidget, QHBoxLayout,
                                QGridLayout, QFormLayout, QLineEdit,
                                QLabel,QPushButton,QButtonGroup,
                                QRadioButton,QDateEdit,QComboBox,
                                QCheckBox,QTextEdit)

from PySide6.QtCore import Qt, QSize, QDate
from PySide6.QtGui import QPixmap, QFont
import os 

class MainWindow(QMainWindow):
    def __init__ (self):
        super().__init__()

        self.setWindowTitle("LOGIN")
        self.setGeometry(100, 100, 350, 500)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #ffffff;
            }
            QLabel {
                color: #333333;
            }
            QLineEdit {
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 10px;
                background-color: #f9f9f9;
                font-size: 14px;
                color: #000000;
            }
            QLineEdit:focus {
                border: 2px solid #3498db;
                background-color: #ffffff;
            }
            QPushButton#LoginButton {
                background-color: #ed5a8a;
                color: white;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton#LoginButton:hover {
                background-color: pink;
            }
            QCheckBox {
                color: #555555;
            }
            QCheckBox::indicator:checked {
                background-color: #ed5a8a;
                border: 1px solid #ed5a8a;
                image: ("checked.png");
            }
        """)

        cental_widget = QWidget()
        self.setCentralWidget(cental_widget)
        layout = QVBoxLayout(cental_widget)
        layout.setContentsMargins(40, 20, 40, 20) #left, top, right, bottom
        layout.setSpacing(5) #แต่ละwidget ห่างกัน...
        layout.addStretch()# ทำให้ชิดกัน

        title = QLabel("LOGIN")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignLeft)
        layout.addWidget(title)
        layout.addSpacing(30)


        texxt_email = QLabel("Email:")
        texxt_email.setFont(QFont("Arial", 12)) 
        texxt_email.setAlignment(Qt.AlignLeft)
        layout.addWidget(texxt_email)
        email = QLineEdit()
        email.setFont(QFont("Arial", 12))
        layout.addWidget(email)
        layout.addSpacing(20)

        text_password = QLabel("Password:")
        text_password.setFont(QFont("Arial", 12))
        text_password.setAlignment(Qt.AlignLeft)
        layout.addWidget(text_password)
        password = QLineEdit()
        password.setFont(QFont("Arial", 12))
        layout.addWidget(password)

        Remember_me = QCheckBox("Remember Me?")
        Remember_me.setFont(QFont("Arial", 12))
        layout.addWidget(Remember_me)
        layout.addSpacing(10)

        submit_button = QPushButton("LOGIN")
        submit_button.setObjectName("LoginButton")
        submit_button.setFixedSize(QSize(300, 40))
        layout.addWidget(submit_button, alignment=Qt.AlignCenter)
        layout.addSpacing(5)

        forgot_password = QLabel('<a href="#">Forgot Password?</a>')
        forgot_password.setFont(QFont("Arial", 10))
        forgot_password.setAlignment(Qt.AlignRight)
        layout.addWidget(forgot_password)
        layout.addSpacing(10)

        text_or = QLabel("————————[OR]————————")
        text_or.setFont(QFont("Arial", 12))
        text_or.setAlignment(Qt.AlignCenter)
        layout.addWidget(text_or)

        group_box = QHBoxLayout()
        group_box.setContentsMargins(0,20,0,20)
        group_box.setSpacing(15)
        group_box.addStretch()

        instagram_image = QLabel()
        try:   
            current_dir = os.path.dirname(os.path.abspath(__file__))
            image_part = os.path.join(current_dir, "g.webp")

            pixmap = QPixmap(image_part) 
            instagram_image.setPixmap(pixmap.scaled(
                50, 50,  
                Qt.KeepAspectRatio,  
                Qt.SmoothTransformation  
            ))
            instagram_image.setAlignment(Qt.AlignCenter)
        except:
            instagram_image.setText("Image not found: g.webp")
            instagram_image.setAlignment(Qt.AlignCenter)
        group_box.addWidget(instagram_image)

        facebook_image = QLabel()
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            image_part = os.path.join(current_dir, "f.webp")

            pixmap = QPixmap(image_part) 
            facebook_image.setPixmap(pixmap.scaled(
                50, 50,  
                Qt.KeepAspectRatio,  
                Qt.SmoothTransformation  
            ))
        except:
            facebook_image.setText("Image not found: f.webp")
            facebook_image.setAlignment(Qt.AlignCenter)
        group_box.addWidget(facebook_image)

        try:
            in_image = QLabel()
            current_dir = os.path.dirname(os.path.abspath(__file__))
            image_part = os.path.join(current_dir, "in.webp")

            pixmap = QPixmap(image_part) 
            in_image.setPixmap(pixmap.scaled(
                50, 50,  
                Qt.KeepAspectRatio,  
                Qt.SmoothTransformation  
            ))
            in_image.setAlignment(Qt.AlignCenter)
        except:
            in_image.setText("Image not found: in.webp")
            in_image.setAlignment(Qt.AlignCenter)
        group_box.addWidget(in_image)

        group_box.addStretch()
        layout.addLayout(group_box)

        # Sign up text
        sign_up_text = QLabel("Need  an account?"+"<a href='#'>SIGN UP<a/>")
        sign_up_text.setFont(QFont("Arial", 10))
        sign_up_text.setAlignment(Qt.AlignCenter)
        layout.addWidget(sign_up_text)



def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
    
if __name__ == "__main__":
    main()