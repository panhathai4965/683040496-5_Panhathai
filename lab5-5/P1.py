"""""
Panhathai Suporn
683040496-5
P1
"""""

import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QStackedWidget,
    QVBoxLayout, QHBoxLayout, QGridLayout, QFormLayout,
    QLabel, QLineEdit, QDateEdit, QSpinBox,
    QPushButton, QDialog, QMessageBox, QScrollArea,
    QFrame, QSizePolicy
)
from PySide6.QtCore import Qt, Signal, QDate
from PySide6.QtGui import QFont

class RoomCard(QWidget):
    # Signal: emits (room_name, price) when user clicks Select
    room_selected = Signal(str, int)

    def __init__(self, room_name: str, price: int, description: str, emoji: str = "🏨"):
        super().__init__()
        self.room_name = room_name
        self.price = price
        self._is_selected = False

        self._build_ui(emoji, description)
        self.deselect()  # Set default style

    def _build_ui(self, emoji: str, description: str):
        self.setFixedSize(200, 220)
        self.setCursor(Qt.PointingHandCursor)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(6)

        self.emoji_label = QLabel(emoji)
        self.emoji_label.setFont(QFont("Segoe UI", 30))
        self.emoji_label.setAlignment(Qt.AlignCenter)

        self.name_label = QLabel(self.room_name)
        self.name_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.name_label.setAlignment(Qt.AlignCenter)

        self.price_label = QLabel(f"${self.price} / night")
        self.price_label.setStyleSheet("color: #4b5563; font-weight: bold;")
        self.price_label.setAlignment(Qt.AlignCenter)

        self.desc_label = QLabel(description)
        self.desc_label.setFont(QFont("Segoe UI", 9))
        self.desc_label.setStyleSheet("color: #6b7280;")
        self.desc_label.setAlignment(Qt.AlignCenter)
        self.desc_label.setWordWrap(True)

        self.select_btn = QPushButton("Select Room")
        self.select_btn.clicked.connect(self._on_select_clicked)

        layout.addWidget(self.emoji_label)
        layout.addWidget(self.name_label)
        layout.addWidget(self.price_label)
        layout.addWidget(self.desc_label)
        layout.addStretch()
        layout.addWidget(self.select_btn)

    def _on_select_clicked(self):
        self.room_selected.emit(self.room_name, self.price)

    def select(self):
        self._is_selected = True
        self.setStyleSheet("""
            RoomCard {
                background-color: #f0fdf4;
                border: 2px solid #22c55e;
                border-radius: 12px;
            }
        """)
        self.select_btn.setStyleSheet("""
            QPushButton {
                background-color: #22c55e;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 6px;
                font-weight: bold;
            }
        """)
        self.select_btn.setText("✓ Selected")

    def deselect(self):
        self._is_selected = False
        self.setStyleSheet("""
            RoomCard {
                background-color: #ffffff;
                border: 2px solid #e5e7eb;
                border-radius: 12px;
            }
            RoomCard:hover {
                border: 2px solid #6366f1;
                background-color: #f5f3ff;
            }
        """)
        self.select_btn.setStyleSheet("""
            QPushButton {
                background-color: #6366f1;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 6px;
            }
            QPushButton:hover { background-color: #4f46e5; }
        """)
        self.select_btn.setText("Select Room")

class ConfirmDialog(QDialog):
    def __init__(self, guest_name: str, room_name: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Booking Confirmed")
        self.setFixedSize(400, 250)
        self.setModal(True)
        self._build_ui(guest_name, room_name)

    def _build_ui(self, guest_name: str, room_name: str):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)
        layout.setAlignment(Qt.AlignCenter)

        icon = QLabel("✅")
        icon.setFont(QFont("Segoe UI", 40))
        icon.setAlignment(Qt.AlignCenter)

        title = QLabel("Booking Successful!")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setStyleSheet("color: #16a34a;")
        title.setAlignment(Qt.AlignCenter)

        desc = QLabel(f"Dear {guest_name},\n{room_name} is ready to welcome you! 🎉")
        desc.setFont(QFont("Segoe UI", 11))
        desc.setAlignment(Qt.AlignCenter)

        ok_btn = QPushButton("OK")
        ok_btn.setFixedSize(120, 40)
        ok_btn.setStyleSheet("""
            QPushButton {
                background-color: #22c55e;
                color: white;
                border-radius: 8px;
                font-weight: bold;
            }
        """)
        ok_btn.clicked.connect(self.accept)

        layout.addWidget(icon)
        layout.addWidget(title)
        layout.addWidget(desc)
        layout.addWidget(ok_btn, alignment=Qt.AlignCenter)

# ─────────────────────────────────────────────
#  Page 1: Booking Page
# ─────────────────────────────────────────────
class BookingPage(QWidget):
    def __init__(self):
        super().__init__()
        self.selected_room = None
        self.selected_price = 0
        self.cards = [] 
        self._build_ui()

    def _build_ui(self):
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        container = QWidget()
        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(30, 24, 30, 24)
        main_layout.setSpacing(20)

        # Title
        title = QLabel("🏨 Book Your Stay at CozyStay")
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title.setStyleSheet("color: #1e1b4b;")
        main_layout.addWidget(title)

        subtitle = QLabel("Fill in your details and choose your room")
        subtitle.setFont(QFont("Segoe UI", 10))
        subtitle.setStyleSheet("color: #6b7280;")
        main_layout.addWidget(subtitle)

        # ── Section 1: Guest Info Form ──
        form_title = QLabel("📋 Guest Information")
        form_title.setFont(QFont("Segoe UI", 12, QFont.Bold))
        form_title.setStyleSheet("color: #374151; margin-top: 8px;")
        main_layout.addWidget(form_title)

        form_frame = QFrame()
        form_frame.setStyleSheet("background-color: #f9fafb; border-radius: 10px;")
        form_layout = QGridLayout(form_frame)
        form_layout.setContentsMargins(20, 20, 20, 20)
        form_layout.setSpacing(15)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("e.g. John Smith")
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("e.g. 081-234-5678")

        from PySide6.QtGui import QPalette, QColor
        palette = self.name_input.palette()
        palette.setColor(QPalette.PlaceholderText, QColor("#9ca3af")) # บังคับสีเทา
        self.name_input.setPalette(palette)
        self.phone_input.setPalette(palette)
        
        self.checkin_input = QDateEdit(QDate.currentDate())
        self.checkin_input.setCalendarPopup(True)
        self.checkin_input.setDisplayFormat("dd/MM/yyyy")
        
        self.checkout_input = QDateEdit(QDate.currentDate().addDays(1))
        self.checkout_input.setCalendarPopup(True)
        self.checkout_input.setDisplayFormat("dd/MM/yyyy")
        
        self.guests_input = QSpinBox()
        self.guests_input.setRange(1, 10)
        self.guests_input.setSuffix(" guest(s)")

        input_style = """
            QLineEdit, QDateEdit, QSpinBox {
                border: 1px solid #d1d5db;
                border-radius: 6px;
                padding: 6px 10px;
                font-size: 13px;
                background-color: white; /* บังคับพื้นหลังขาวเสมอ */
                color: black;            /* บังคับตัวอักษรดำเสมอ */
            }

            /* --- ปรับแต่งปุ่มลูกศรสำหรับ QDateEdit (ปฏิทิน) --- */
            QDateEdit::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 25px; /* เพิ่มความกว้างปุ่มให้ชัดเจนเหมือนตัวอย่าง */
                border-left: 1px solid #d1d5db;
                background-color: #f3f4f6; /* สีพื้นหลังปุ่มสีเทาอ่อน */
                border-top-right-radius: 6px;
                border-bottom-right-radius: 6px;
            }
            QDateEdit::down-arrow {
                image: none; 
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 6px solid #374151; /* หัวลูกศรสีเทาเข้มเกือบดำ */
                width: 0; height: 0;
            }

            /* --- ปรับแต่งปุ่มลูกศรสำหรับ QSpinBox (จำนวนแขก) --- */
            QSpinBox::up-button, QSpinBox::down-button {
                background-color: #f3f4f6;
                border-left: 1px solid #d1d5db;
                width: 25px;
            }
            QSpinBox::up-button { border-top-right-radius: 6px; }
            QSpinBox::down-button { 
                border-bottom-right-radius: 6px;
                border-top: 1px solid #d1d5db; /* เส้นคั่นกลางระหว่างปุ่มขึ้น-ลง */
            }
            QSpinBox::up-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-bottom: 6px solid #374151;
            }
            QSpinBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 6px solid #374151;
            }
            
            /* เอฟเฟกต์ตอนเอาเมาส์ไปวางให้ปุ่มเข้มขึ้นเหมือนของจริง */
            QDateEdit::drop-down:hover, QSpinBox::up-button:hover, QSpinBox::down-button:hover {
                background-color: #e5e7eb;
            }
            QLineEdit:focus, QDateEdit:focus, QSpinBox:focus { border: 1px solid #6366f1; }

        """
        label_style = "font-size: 13px; color: #374151; font-weight: bold;"
        
        inputs = [
            ("Full Name :", self.name_input),
            ("Phone Number :", self.phone_input),
            ("Check-in Date :", self.checkin_input),
            ("Check-out Date :", self.checkout_input),
            ("Guests :", self.guests_input),
        ]

        for i, (text, widget) in enumerate(inputs):
            lbl = QLabel(text)
            lbl.setStyleSheet(label_style)
            widget.setStyleSheet(input_style)
            widget.setMinimumWidth(300)
            form_layout.addWidget(lbl, i, 0)
            form_layout.addWidget(widget, i, 1)

        main_layout.addWidget(form_frame)

        # ── Section 2: Room Selection ──
        room_title = QLabel("🛏 Select a Room")
        room_title.setFont(QFont("Segoe UI", 12, QFont.Bold))
        room_title.setStyleSheet("color: #374151; margin-top: 8px;")
        main_layout.addWidget(room_title)

        rooms_data = [
            ("Standard Room", 50,  "Single bed, Free Wi-Fi",             "🛏"),
            ("Deluxe Room",   120, "Double bed, Ocean view, Wi-Fi",      "🌊"),
            ("Suite Room",    250, "Living room, Jacuzzi, Premium view", "👑"),
            ("Family Room",   160, "2 Bedrooms, Perfect for families",   "👨‍👩‍👧‍👦"),
        ]

        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(14)

        for name, price, desc, emoji in rooms_data:
            card = RoomCard(name, price, desc, emoji)
            card.room_selected.connect(self._on_room_selected)
            self.cards.append(card)
            cards_layout.addWidget(card)

        cards_layout.addStretch()
        main_layout.addLayout(cards_layout)

        # ── Buttons ──
        btn_layout = QHBoxLayout()
        self.clear_btn = QPushButton("🗑  Clear Info")
        self.clear_btn.setFixedHeight(42)
        self.clear_btn.setStyleSheet("""
            QPushButton { background-color: #f3f4f6; color: #374151; border: 1px solid #d1d5db; border-radius: 8px; padding: 0 20px; }
            QPushButton:hover { background-color: #e5e7eb; }
        """)
        self.clear_btn.clicked.connect(self.clear_form)

        self.next_btn = QPushButton("Next  →")
        self.next_btn.setFixedHeight(42)
        self.next_btn.setStyleSheet("""
            QPushButton { background-color: #6366f1; color: white; border: none; border-radius: 8px; padding: 0 28px; font-weight: bold; }
            QPushButton:hover { background-color: #4f46e5; }
        """)

        btn_layout.addWidget(self.clear_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(self.next_btn)
        main_layout.addLayout(btn_layout)
        
        scroll.setWidget(container)
        page_layout = QVBoxLayout(self)
        page_layout.setContentsMargins(0, 0, 0, 0)
        page_layout.addWidget(scroll)

    def _on_room_selected(self, room_name: str, price: int):
        self.selected_room = room_name
        self.selected_price = price
        for card in self.cards:
            if card.room_name == room_name:
                card.select()
            else:
                card.deselect()

    def clear_form(self):
        self.name_input.clear()
        self.phone_input.clear()
        self.checkin_input.setDate(QDate.currentDate())
        self.checkout_input.setDate(QDate.currentDate().addDays(1))
        self.guests_input.setValue(1)
        self.selected_room = None
        for card in self.cards:
            card.deselect()

    def get_booking_data(self):
        name = self.name_input.text().strip()
        phone = self.phone_input.text().strip()
        checkin = self.checkin_input.date()
        checkout = self.checkout_input.date()

        if not name:
            QMessageBox.warning(self, "Missing Information", "Please enter your full name.")
            return None
        if not phone:
            QMessageBox.warning(self, "Missing Information", "Please enter your phone number.")
            return None
        if checkin >= checkout:
            QMessageBox.warning(self, "Invalid Dates", "Check-out date must be after check-in date.")
            return None
        if not self.selected_room:
            QMessageBox.warning(self, "No Room Selected", "Please select a room before proceeding.")
            return None

        nights = checkin.daysTo(checkout)
        total = nights * self.selected_price

        return {
            "name": name,
            "phone": phone,
            "checkin": checkin.toString("dd/MM/yyyy"),
            "checkout": checkout.toString("dd/MM/yyyy"),
            "guests": self.guests_input.value(),
            "room": self.selected_room,
            "price_per_night": self.selected_price,
            "nights": nights,
            "total": total
        }

# ─────────────────────────────────────────────
#  PAGE 2: ReviewPage
# ─────────────────────────────────────────────
class ReviewPage(QWidget):
    def __init__(self):
        super().__init__()
        self.current_data = {}
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(16)

        title = QLabel("📋 Booking Summary")
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        layout.addWidget(title)

        subtitle = QLabel("Please review your details before confirming")
        subtitle.setStyleSheet("color: #6b7280;")
        layout.addWidget(subtitle)

        self.info_frame = QFrame()
        self.info_frame.setStyleSheet("background-color: #f9fafb; border-radius: 12px; padding: 20px;")
        self.info_layout = QGridLayout(self.info_frame)
        self.info_layout.setSpacing(15)

        self.labels = {}
        display_keys = [
            ("room", "🛏  Room"), ("price", "💰  Price / Night"),
            ("name", "👤  Guest Name"), ("phone", "📞  Phone"),
            ("checkin", "📅  Check-in"), ("checkout", "📅  Check-out"),
            ("nights", "🌙  Nights"), ("guests", "👥  Guests")
        ]

        for i, (key, text) in enumerate(display_keys):
            k_lbl = QLabel(text)
            k_lbl.setStyleSheet("font-weight: bold; color: #374151;")
            v_lbl = QLabel("-")
            self.labels[key] = v_lbl
            self.info_layout.addWidget(k_lbl, i, 0)
            self.info_layout.addWidget(v_lbl, i, 1)

        layout.addWidget(self.info_frame)

        self.total_label = QLabel("Total Amount: $0")
        self.total_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        self.total_label.setStyleSheet("color: #6366f1;")
        self.total_label.setAlignment(Qt.AlignRight)
        layout.addWidget(self.total_label)

        btn_layout = QHBoxLayout()
        self.back_btn = QPushButton("←  Back")
        self.back_btn.setFixedSize(120, 44)
        self.back_btn.setStyleSheet("background-color: #f3f4f6; border-radius: 8px;")
        
        self.submit_btn = QPushButton("✅  Confirm Booking")
        self.submit_btn.setFixedSize(180, 44)
        self.submit_btn.setStyleSheet("""
            QPushButton { background-color: #22c55e; color: white; border-radius: 8px; font-weight: bold; }
            QPushButton:hover { background-color: #16a34a; }
        """)

        btn_layout.addWidget(self.back_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(self.submit_btn)
        layout.addLayout(btn_layout)

    def load_data(self, data: dict):
        self.current_data = data
        self.labels["room"].setText(data["room"])
        self.labels["price"].setText(f"${data['price_per_night']}")
        self.labels["name"].setText(data["name"])
        self.labels["phone"].setText(data["phone"])
        self.labels["checkin"].setText(data["checkin"])
        self.labels["checkout"].setText(data["checkout"])
        self.labels["nights"].setText(f"{data['nights']} night(s)")
        self.labels["guests"].setText(f"{data['guests']} guest(s)")
        self.total_label.setText(f"Total Amount: ${data['total']}")

# ─────────────────────────────────────────────
#  MainWindow
# ─────────────────────────────────────────────
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CozyStay — Hotel Booking System")
        self.setMinimumSize(900, 750)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.booking_page = BookingPage()
        self.review_page = ReviewPage()

        self.stack.addWidget(self.booking_page)
        self.stack.addWidget(self.review_page)

        self.booking_page.next_btn.clicked.connect(self._go_to_review)
        self.review_page.back_btn.clicked.connect(self._go_to_booking)
        self.review_page.submit_btn.clicked.connect(self._on_submit)

        self.setStyleSheet("QMainWindow { background-color: #f0f0ff; }")

    def _go_to_review(self):
        data = self.booking_page.get_booking_data()
        if data:
            self.review_page.load_data(data)
            self.stack.setCurrentIndex(1)

    def _go_to_booking(self):
        self.stack.setCurrentIndex(0)

    def _on_submit(self):
        data = self.review_page.current_data
        dlg = ConfirmDialog(data["name"], data["room"], self)
        if dlg.exec():
            self.booking_page.clear_form()
            self.stack.setCurrentIndex(0)

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()