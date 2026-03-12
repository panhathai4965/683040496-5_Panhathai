import sys
from PySide6.QtCore import Qt, Signal, QDate, QLocale
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QStackedWidget,
    QVBoxLayout, QHBoxLayout, QGridLayout, QFormLayout,
    QLabel, QLineEdit, QDateEdit, QSpinBox,
    QPushButton, QDialog, QMessageBox, QScrollArea,
    QFrame, QSizePolicy
)
from PySide6.QtCore import QLocale

QLocale.setDefault(QLocale(QLocale.English, QLocale.UnitedStates))

from PySide6.QtGui import QFont, QPalette, QColor, QIntValidator


class RoomCard(QWidget):
    room_selected = Signal(str, int)

    def __init__(self, room_name: str, price: int, description: str, emoji: str = "🏨"):
        super().__init__()
        self.room_name = room_name
        self.price = price
        self.description = description
        self.emoji = emoji
        self._is_selected = False
        self._build_ui(emoji, description)
        self.deselect()

    def _build_ui(self, emoji: str, description: str):
        self.setFixedSize(200, 200)
        self.setCursor(Qt.PointingHandCursor)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(6)

        self.emoji_label = QLabel(emoji)
        self.emoji_label.setFont(QFont("Segoe UI", 32))
        self.emoji_label.setAlignment(Qt.AlignCenter)

        self.name_label = QLabel(self.room_name)
        self.name_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.name_label.setAlignment(Qt.AlignCenter)

        self.price_label = QLabel(f"${self.price} / night")
        self.price_label.setFont(QFont("Segoe UI", 11))
        self.price_label.setAlignment(Qt.AlignCenter)
        self.price_label.setStyleSheet("color: #16a34a; font-weight: bold;")

        self.desc_label = QLabel(description)
        self.desc_label.setFont(QFont("Segoe UI", 10))
        self.desc_label.setAlignment(Qt.AlignCenter)
        self.desc_label.setWordWrap(True)
        self.desc_label.setStyleSheet("color: #64748b;")

        self.select_btn = QPushButton("Select Room")
        self.select_btn.setFixedHeight(32)
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
                padding: 5px;
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
                padding: 5px;
            }
            QPushButton:hover { background-color: #4f46e5; }
        """)
        self.select_btn.setText("Select Room")

    def is_selected(self):
        return self._is_selected

class ConfirmDialog(QDialog):
    def __init__(self, guest_name: str, room_name: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Booking Confirmed")
        self.setFixedSize(360, 220)
        self.setModal(True)
        self._build_ui(guest_name, room_name)

    def _build_ui(self, guest_name: str, room_name: str):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(12)

        icon = QLabel("🎉")
        icon.setFont(QFont("Segoe UI", 36))
        icon.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon)

        msg = QLabel(f"Thank you, {guest_name}!\nYour booking for the {room_name} is confirmed.")
        msg.setFont(QFont("Segoe UI", 12))
        msg.setAlignment(Qt.AlignCenter)
        layout.addWidget(msg)

        ok_btn = QPushButton("OK")
        ok_btn.setFixedHeight(36)
        ok_btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
        ok_btn.setStyleSheet("""
            QPushButton {
                background-color: #6366f1;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 0 28px;
            }
            QPushButton:hover { background-color: #4f46e5; }
        """)
        ok_btn.clicked.connect(self.accept)
        layout.addStretch()
        layout.addWidget(ok_btn)

class BookingPage(QWidget):
    def __init__(self):
        super().__init__()
        self.selected_room = None
        self.selected_price = 0
        self.cards = []
        self.rooms_data = [
            ("Standard Room", 50,  "Single bed, Free Wi-Fi",             "🛏", 1),
            ("Deluxe Room",   120, "Double bed, Ocean view, Wi-Fi",      "🌊", 2),
            ("Suite Room",    250, "Living room, Jacuzzi, Premium view", "👑", 3),
            ("Family Room",   160, "2 Bedrooms, Perfect for families",   "👨‍👩‍👧‍👦", 4),
        ]
        self._build_ui()

    def _build_ui(self):
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        container = QWidget()
        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(30, 24, 30, 24)
        main_layout.setSpacing(20)

        title = QLabel("🏨 Book Your Stay at CozyStay")
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title.setStyleSheet("color: #1e1b4b;")
        subtitle = QLabel("Fill in your details and choose your room")
        subtitle.setFont(QFont("Segoe UI", 10))
        subtitle.setStyleSheet("color: #6b7280;")
        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)

        # Section 1: Guest Info Form
        form_title = QLabel("📋 Guest Information")
        form_title.setFont(QFont("Segoe UI", 12, QFont.Bold))
        form_title.setStyleSheet("color: #374151; margin-top: 8px;")
        main_layout.addWidget(form_title)

        form_frame = QFrame()
        form_frame.setStyleSheet("""
            QFrame {
                background-color: #f9fafb;
                border-radius: 10px;
            }
        """)
        form_layout = QFormLayout(form_frame)
        form_layout.setLabelAlignment(Qt.AlignRight)
        form_layout.setFormAlignment(Qt.AlignLeft | Qt.AlignTop)
        form_layout.setHorizontalSpacing(18)
        form_layout.setVerticalSpacing(10)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter your full name")
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Enter your phone number")
        self.phone_input.setValidator(QIntValidator(0, 2147483647, self))

        self.checkin_input = QDateEdit()
        self.checkin_input.setCalendarPopup(True)
        self.checkin_input.setDate(QDate.currentDate())
        self.checkout_input = QDateEdit()
        self.checkout_input.setCalendarPopup(True)
        self.checkout_input.setDate(QDate.currentDate().addDays(1))
        self.guests_input = QSpinBox()
        self.guests_input.setMinimum(1)
        self.guests_input.setMaximum(10)
        self.guests_input.setValue(1)

        input_style = """
            QLineEdit, QDateEdit, QSpinBox {
                border: 1px solid #d1d5db;
                border-radius: 6px;
                padding: 6px 10px;
                font-size: 13px;
                background: white;
                color: #1e293b;
            }
            QLineEdit::placeholder {
                color: #9ca3af;
            }
            QDateEdit::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 24px;
                border-left: 1px solid #d1d5db;
            }
            QDateEdit::down-arrow {
                image: url(:/qt-project.org/styles/commonstyle/images/arrowdown-16.png);
                width: 16px;
                height: 16px;
            }
            QLineEdit:focus, QDateEdit:focus, QSpinBox:focus {
                border: 1px solid #6366f1;
            }
        """
        for w in [self.name_input, self.phone_input,
                  self.checkin_input, self.checkout_input, self.guests_input]:
            w.setStyleSheet(input_style)
            w.setMinimumWidth(200)

        label_style = "font-size: 13px; color: #374151; font-weight: bold;"
        form_layout.addRow(QLabel("Full Name :"), self.name_input)
        form_layout.addRow(QLabel("Phone Number :"), self.phone_input)
        form_layout.addRow(QLabel("Check-in Date :"), self.checkin_input)
        form_layout.addRow(QLabel("Check-out Date :"), self.checkout_input)
        form_layout.addRow(QLabel("Guests :"), self.guests_input)

        for i in range(form_layout.rowCount()):
            label = form_layout.itemAt(i, QFormLayout.LabelRole).widget()
            label.setStyleSheet(label_style)

        main_layout.addWidget(form_frame)

        # Section 2: Room Selection
        room_title = QLabel("🛏 Select a Room")
        room_title.setFont(QFont("Segoe UI", 12, QFont.Bold))
        room_title.setStyleSheet("color: #374151; margin-top: 8px;")
        main_layout.addWidget(room_title)

        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(14)
        cards_layout.setContentsMargins(0, 0, 0, 0)

        for name, price, desc, emoji, max_guests in self.rooms_data:
            card = RoomCard(name, price, desc, emoji)
            card.room_selected.connect(self._on_room_selected)
            self.cards.append(card)
            cards_layout.addWidget(card)
        cards_layout.addStretch()
        main_layout.addLayout(cards_layout)

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)

        self.clear_btn = QPushButton("🗑  Clear Info")
        self.clear_btn.setFixedHeight(42)
        self.clear_btn.setFont(QFont("Segoe UI", 11))
        self.clear_btn.setCursor(Qt.PointingHandCursor)
        self.clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #f3f4f6;
                color: #374151;
                border: 1px solid #d1d5db;
                border-radius: 8px;
                padding: 0 20px;
            }
            QPushButton:hover { background-color: #e5e7eb; }
        """)
        self.clear_btn.clicked.connect(self.clear_form)

        self.next_btn = QPushButton("Next  →")
        self.next_btn.setFixedHeight(42)
        self.next_btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.next_btn.setCursor(Qt.PointingHandCursor)
        self.next_btn.setStyleSheet("""
            QPushButton {
                background-color: #6366f1;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 0 28px;
            }
            QPushButton:hover { background-color: #4f46e5; }
        """)

        btn_layout.addWidget(self.clear_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(self.next_btn)

        main_layout.addLayout(btn_layout)
        main_layout.addStretch()

        scroll.setWidget(container)
        page_layout = QVBoxLayout(self)
        page_layout.setContentsMargins(0, 0, 0, 0)
        page_layout.addWidget(scroll)
        self.setLayout(page_layout)  # สำคัญมาก

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
        self.selected_price = 0
        for card in self.cards:
            card.deselect()

    def get_booking_data(self):
        name = self.name_input.text().strip()
        phone = self.phone_input.text().strip()
        checkin = self.checkin_input.date()
        checkout = self.checkout_input.date()
        guests = self.guests_input.value()

        if not name:
            QMessageBox.warning(self, "Missing Information", "Please enter your full name.")
            return None
        if not phone:
            QMessageBox.warning(self, "Missing Information", "Please enter your phone number.")
            return None
        if checkin >= checkout:
            QMessageBox.warning(self, "Invalid Dates",
                                "Check-out date must be after check-in date.")
            return None
        if not self.selected_room:
            QMessageBox.warning(self, "No Room Selected",
                                "Please select a room before proceeding.")
            return None

        # ตรวจสอบจำนวนคนกับความจุห้อง
        max_guests = 1
        if self.selected_room is not None:
            for room in self.rooms_data:
                if room[0] == self.selected_room:
                    max_guests = room[4]
                    break
        else:
            QMessageBox.warning(self, "No Room Selected",
                                "Please select a room before proceeding.")
            return None
        if guests > max_guests:
            QMessageBox.warning(self, "Too Many Guests",
                                f"{self.selected_room} รองรับได้สูงสุด {max_guests} คน")
            return None

        nights = checkin.daysTo(checkout)
        total = nights * self.selected_price

        data_dict = {
            "room": self.selected_room,
            "price": self.selected_price,
            "name": name,
            "phone": phone,
            "checkin": checkin.toString("yyyy-MM-dd"),
            "checkout": checkout.toString("yyyy-MM-dd"),
            "nights": nights,
            "guests": guests,
            "total": total
        }
        return data_dict

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
        title.setStyleSheet("color: #1e1b4b;")

        subtitle = QLabel("Please review your details before confirming")
        subtitle.setFont(QFont("Segoe UI", 10))
        subtitle.setStyleSheet("color: #6b7280;")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        self.info_frame = QFrame()
        self.info_frame.setStyleSheet("""
            QFrame {
                background-color: #f9fafb;
                border-radius: 12px;
            }
        """)

        self.info_layout = QGridLayout(self.info_frame)
        self.labels = []
        key_style = "font-weight: bold; color: #374151; font-size: 13px;"
        val_style = "color: #1f2937; font-size: 13px;"

        display_data = [
            ("🛏  Room",            ""),
            ("💰  Price / Night",   f"$ -"),
            ("👤  Guest Name",      ""),
            ("📞  Phone",           ""),
            ("📅  Check-in",        ""),
            ("📅  Check-out",       ""),
            ("🌙  Nights",          f"- night(s)"),
            ("👥  Guests",          f"- guest(s)"),
        ]
        for i, (k, v) in enumerate(display_data):
            key_lbl = QLabel(k)
            key_lbl.setStyleSheet(key_style)
            val_lbl = QLabel(v)
            val_lbl.setStyleSheet(val_style)
            self.info_layout.addWidget(key_lbl, i, 0)
            self.info_layout.addWidget(val_lbl, i, 1)
            self.labels.append(val_lbl)

        layout.addWidget(self.info_frame)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("color: #e5e7eb;")
        layout.addWidget(line)

        self.total_label = QLabel("Total: $ -")
        self.total_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        self.total_label.setStyleSheet("color: #22c55e;")
        layout.addWidget(self.total_label)

        layout.addStretch()

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)

        self.back_btn = QPushButton("←  Back")
        self.back_btn.setFixedHeight(44)
        self.back_btn.setFont(QFont("Segoe UI", 11))
        self.back_btn.setCursor(Qt.PointingHandCursor)
        self.back_btn.setStyleSheet("""
            QPushButton {
                background-color: #f3f4f6;
                color: #374151;
                border: 1px solid #d1d5db;
                border-radius: 8px;
                padding: 0 22px;
            }
            QPushButton:hover { background-color: #e5e7eb; }
        """)

        self.submit_btn = QPushButton("✅  Confirm Booking")
        self.submit_btn.setFixedHeight(44)
        self.submit_btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.submit_btn.setCursor(Qt.PointingHandCursor)
        self.submit_btn.setStyleSheet("""
            QPushButton {
                background-color: #22c55e;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 0 28px;
            }
            QPushButton:hover { background-color: #16a34a; }
        """)

        btn_layout.addWidget(self.back_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(self.submit_btn)
        layout.addLayout(btn_layout)

    def load_data(self, data: dict):
        self.current_data = data
        vals = [
            data.get("room", ""),
            f"${data.get('price', 0)}",
            data.get("name", ""),
            data.get("phone", ""),
            data.get("checkin", ""),
            data.get("checkout", ""),
            f"{data.get('nights', 0)} night(s)",
            f"{data.get('guests', 1)} guest(s)",
        ]
        for lbl, v in zip(self.labels, vals):
            lbl.setText(v)
        self.total_label.setText(f"Total: ${data.get('total', 0)}")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CozyStay — Hotel Booking System")
        self.setMinimumSize(820, 680)
        self.resize(900, 720)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.booking_page = BookingPage()
        self.review_page = ReviewPage()

        self.stack.addWidget(self.booking_page)
        self.stack.addWidget(self.review_page)

        self.booking_page.next_btn.clicked.connect(self._go_to_review)
        self.booking_page.clear_btn.clicked.connect(self.booking_page.clear_form)
        self.review_page.back_btn.clicked.connect(self._go_to_booking)
        self.review_page.submit_btn.clicked.connect(self._on_submit)

        self.stack.setCurrentIndex(0)

        self.setStyleSheet("""
            QMainWindow { background-color: #f0f0ff; }
            QScrollArea  { background-color: transparent; }
            QWidget      { font-family: 'Segoe UI', 'Tahoma', sans-serif; }
        """)

    def _go_to_review(self):
        data = self.booking_page.get_booking_data()
        if data is None:
            return
        self.review_page.load_data(data)
        self.stack.setCurrentIndex(1)

    def _go_to_booking(self):
        self.stack.setCurrentIndex(0)

    def _on_submit(self):
        data = self.review_page.current_data
        dlg = ConfirmDialog(data.get("name", ""), data.get("room", ""), self)
        dlg.exec()
        self.booking_page.clear_form()
        self.stack.setCurrentIndex(0)

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor("#f0f0ff"))
    palette.setColor(QPalette.Base, QColor("#ffffff"))
    palette.setColor(QPalette.Text, QColor("#1e293b"))
    palette.setColor(QPalette.Button, QColor("#f3f4f6"))
    palette.setColor(QPalette.ButtonText, QColor("#374151"))
    app.setPalette(palette)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()