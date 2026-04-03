""""
Panhathai Suporn
683040496-5
P2
"""

"""
Student Registration System — PySide6
======================================
3 pages via QStackedWidget + Signal/Slot.

Page 1 : Card list (drag-drop reorder, delete)
Page 2 : Add student form
Page 3 : Review & confirm
"""

import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QStackedWidget,
    QVBoxLayout, QHBoxLayout, QGridLayout, QScrollArea,
    QLabel, QLineEdit, QPushButton, QComboBox, QFrame,
    QMessageBox,
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QCursor
# เพิ่มที่กลุ่ม PySide6.QtCore
from PySide6.QtCore import Qt, Signal, QRegularExpression 
# เพิ่มที่กลุ่ม PySide6.QtGui
from PySide6.QtGui import QFont, QCursor, QRegularExpressionValidator

# สมมติว่าไฟล์เหล่านี้อยู่ในโฟลเดอร์เดียวกันตามเทมเพลต
from data import COURSES
from style import C, BASE, INPUT_SS, COMBO_SS, SCROLL_SS
from style import btn_ss, section_label, field_label, divider
from StudentCard_template import StudentCard


# ─────────────────────────────────────────────────────────────
#  Page 1 — Student List
# ─────────────────────────────────────────────────────────────
class StudentListPage(QWidget):
    go_to_add = Signal()

    def __init__(self):
        super().__init__()
        self._cards = []
        self.setAcceptDrops(True)
        self._build()

    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── top bar ──
        bar = QFrame()
        bar.setFixedHeight(64)
        bar.setStyleSheet(f"background:{C['bg']}; border-bottom:1px solid {C['border']};")
        bl = QHBoxLayout(bar)
        bl.setContentsMargins(32, 0, 32, 0)

        title = QLabel("Students")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setStyleSheet(f"color:{C['text']};")

        self.lbl_count = QLabel("0 enrolled")
        self.lbl_count.setStyleSheet(f"color:{C['muted']};font-size:13px;")

        btn_add = QPushButton("+ Add Student")
        btn_add.setCursor(QCursor(Qt.PointingHandCursor))
        btn_add.setStyleSheet(btn_ss(C['accent'], "#1d4ed8"))
        btn_add.clicked.connect(self.go_to_add.emit)

        bl.addWidget(title)
        bl.addSpacing(12)
        bl.addWidget(self.lbl_count, alignment=Qt.AlignVCenter)
        bl.addStretch()
        bl.addWidget(btn_add)

        # ── scroll area ──
        self._scroll = QScrollArea()
        self._scroll.setWidgetResizable(True)
        self._scroll.setStyleSheet(SCROLL_SS)
        
        self._container = QWidget()
        self._container.setStyleSheet(f"background:{C['bg']};")
        self._card_lay = QVBoxLayout(self._container)
        self._card_lay.setContentsMargins(32, 20, 32, 20)
        self._card_lay.setSpacing(12)
        self._card_lay.addStretch()

        self._scroll.setWidget(self._container)
        root.addWidget(bar)
        root.addWidget(self._scroll)

    def add_student(self, data: dict):
        card = StudentCard(data)
        # เชื่อมปุ่มลบ (ตอนนี้หาเจอแล้วเพราะมี self.)
        card.btn_del.clicked.connect(lambda: self._remove_card(card))
        # แทรกการ์ดไว้ก่อน Stretch (ตัวสุดท้ายใน layout)
        self._cards.append(card)
        self._card_lay.insertWidget(len(self._cards) - 1, card)
        self._refresh_count()

    def _remove_card(self, card: StudentCard):
        reply = QMessageBox.question(
            self, "Remove student",
            f"Remove {card.data['firstname']} {card.data['lastname']}?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            self._cards.remove(card)
            self._card_lay.removeWidget(card)
            card.deleteLater()
            self._refresh_count()

    def _refresh_count(self):
        count = len(self._cards)
        self.lbl_count.setText(f"{count} enrolled")

    # ── drag-drop reorder ──
    def dragEnterEvent(self, event):
        if event.mimeData().hasText() and event.mimeData().text() == "student_card":
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event):
        src = event.source()
        if not isinstance(src, StudentCard) or src not in self._cards:
            return

        local_y = self._container.mapFrom(self, event.position().toPoint()).y()
        target = len(self._cards) - 1
        for i, card in enumerate(self._cards):
            if local_y < card.y() + card.height() // 2:
                target = i
                break

        src_idx = self._cards.index(src)
        if src_idx == target: return

        self._cards.pop(src_idx)
        self._cards.insert(target, src)
        
        # จัดเรียง Layout ใหม่
        for i, card in enumerate(self._cards):
            self._card_lay.insertWidget(i, card)
        event.acceptProposedAction()


# ─────────────────────────────────────────────────────────────
#  Page 2 — Add Student Form
# ─────────────────────────────────────────────────────────────
class AddStudentPage(QWidget):
    cancel_clicked = Signal()
    review_requested = Signal(dict)

    def __init__(self):
        super().__init__()
        self._build()

    def _inp(self, ph: str = "") -> QLineEdit:
        e = QLineEdit()
        e.setPlaceholderText(ph)
        e.setMinimumHeight(38)
        e.setStyleSheet(INPUT_SS)
        return e

    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        # top bar
        bar = QFrame()
        bar.setFixedHeight(64)
        bar.setStyleSheet(f"background:{C['bg']}; border-bottom:1px solid {C['border']};")
        bl = QHBoxLayout(bar)
        bl.setContentsMargins(32, 0, 32, 0)
        t = QLabel("Add Student")
        t.setFont(QFont("Segoe UI", 16, QFont.Bold))
        t.setStyleSheet(f"color:{C['text']};")
        bl.addWidget(t)
        bl.addStretch()

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(SCROLL_SS)

        body = QWidget()
        body.setStyleSheet(f"background:{C['bg']};")
        form = QVBoxLayout(body)
        form.setContentsMargins(40, 28, 40, 28)
        form.setSpacing(15)

        # ── Personal Information ──
        form.addWidget(section_label("PERSONAL INFORMATION"))
        
        self.ed_id = self._inp("e.g. 683040222-2")
        # ตั้งค่า input mask ให้ง่าย: รับเฉพาะตัวเลข 10 ตัวเท่านั้น
        self.ed_id.setMaxLength(11)  # 9 digits + dash + 1 digit
        # เชื่อมต่อการแปลงข้อมูลเมื่อมีการพิมพ์
        self.ed_id.textChanged.connect(self._format_student_id)
        
        form.addWidget(field_label("Student ID *"))
        form.addWidget(self.ed_id)

        name_row = QHBoxLayout()
        self.ed_fname = self._inp("First name")
        self.ed_lname = self._inp("Last name")
        
        c1, c2 = QVBoxLayout(), QVBoxLayout()
        c1.addWidget(field_label("First Name *"))
        c1.addWidget(self.ed_fname)
        c2.addWidget(field_label("Last Name *"))
        c2.addWidget(self.ed_lname)
        name_row.addLayout(c1)
        name_row.addLayout(c2)
        form.addLayout(name_row)

        edu_row = QHBoxLayout()
        self.ed_faculty = self._inp("e.g. Science & Technology")
        self.ed_major = self._inp("e.g. Computer Science")
        
        c3, c4 = QVBoxLayout(), QVBoxLayout()
        c3.addWidget(field_label("Faculty *"))
        c3.addWidget(self.ed_faculty)
        c4.addWidget(field_label("Major *"))
        c4.addWidget(self.ed_major)
        edu_row.addLayout(c3)
        edu_row.addLayout(c4)
        form.addLayout(edu_row)

        form.addSpacing(10)
        form.addWidget(divider())

        # ── Course Selection ──
        form.addWidget(section_label("COURSE SELECTION (CHOOSE 1–3)"))
        
        self.cb_courses = []
        for i in range(1, 4):
            form.addWidget(field_label(f"Course {i}"))
            cb = QComboBox()
            cb.setStyleSheet(COMBO_SS)
            # วนลูปจาก COURSES ที่เป็น List ใน data.py
            for item in COURSES:
                if "·" in item:
                    # ถ้าเจอเครื่องหมาย · ให้แยก รหัส และ ชื่อ
                    parts = item.split("·")
                    c_code = parts[0].strip()
                    c_name = parts[1].strip()
                    # แสดง "CS101 · Intro..." แต่เก็บข้อมูลจริงๆ เป็น "CS101"
                    cb.addItem(item, c_code) 
                else:
                    # สำหรับรายการแรก "- Select Course -"
                    cb.addItem(item, None)
            
            form.addWidget(cb)
            self.cb_courses.append(cb)

        self.lbl_err = QLabel("")
        self.lbl_err.setStyleSheet(f"color:{C['red']}; font-size:13px;")
        form.addWidget(self.lbl_err)

        form.addStretch()

        # ── buttons ──
        btn_row = QHBoxLayout()
        bc = QPushButton("← Cancel")
        bc.setCursor(QCursor(Qt.PointingHandCursor))
        bc.setStyleSheet(btn_ss(C['bg'], C['surface'], C['muted'], border=f"1px solid {C['border']}"))
        bc.clicked.connect(self.cancel_clicked.emit)

        br = QPushButton("Review →")
        br.setCursor(QCursor(Qt.PointingHandCursor))
        br.setStyleSheet(btn_ss(C['accent'], "#1d4ed8"))
        br.clicked.connect(self._on_review)

        btn_row.addWidget(bc)
        btn_row.addStretch()
        btn_row.addWidget(br)
        form.addLayout(btn_row)

        scroll.setWidget(body)
        root.addWidget(bar)
        root.addWidget(scroll)

    def _on_review(self):
        data = {
            "id": self.ed_id.text().strip(),
            "firstname": self.ed_fname.text().strip(),
            "lastname": self.ed_lname.text().strip(),
            "fullname": f"{self.ed_fname.text().strip()} {self.ed_lname.text().strip()}",
            "faculty": self.ed_faculty.text().strip(),
            "major": self.ed_major.text().strip(),
            "courses": [c.currentData() for c in self.cb_courses if c.currentData()]
        }

        if not all([data["id"], data["firstname"], data["lastname"], data["faculty"], data["major"]]) or not data["courses"]:
            self.lbl_err.setText("Required: Student ID, First Name, Last Name, Faculty, Major, at least 1 course")
            return

        self.lbl_err.setText("")
        self.review_requested.emit(data)

    def _format_student_id(self):
        """Auto-format student ID to XXXXXXXXX-X format when typing"""
        text = self.ed_id.text()
        # เอาเฉพาะตัวเลข
        digits_only = ''.join(c for c in text if c.isdigit())
        
        # จำกัดไว้ 10 หลัก
        if len(digits_only) > 10:
            digits_only = digits_only[:10]
        
        # แปลงเป็นรูปแบบ XXXXXXXXX-X
        if len(digits_only) <= 9:
            formatted = digits_only
        else:
            formatted = digits_only[:9] + "-" + digits_only[9]
        
        # Update the field without triggering recursion
        self.ed_id.blockSignals(True)
        self.ed_id.setText(formatted)
        self.ed_id.blockSignals(False)

    def load_data(self, d: dict):
        self.ed_id.setText(d.get("id", ""))
        self.ed_fname.setText(d.get("firstname", ""))
        self.ed_lname.setText(d.get("lastname", ""))
        self.ed_faculty.setText(d.get("faculty", ""))
        self.ed_major.setText(d.get("major", ""))
        
        courses = d.get("courses", [])
        for i, cb in enumerate(self.cb_courses):
            if i < len(courses):
                idx = cb.findData(courses[i])
                cb.setCurrentIndex(idx)
            else:
                cb.setCurrentIndex(0)

    def clear_form(self):
        for w in [self.ed_id, self.ed_fname, self.ed_lname, self.ed_faculty, self.ed_major]:
            w.clear()
        for cb in self.cb_courses:
            cb.setCurrentIndex(0)
        self.lbl_err.setText("")


# ─────────────────────────────────────────────────────────────
#  Page 3 — Review & Confirm
# ─────────────────────────────────────────────────────────────
class ReviewPage(QWidget):
    edit_clicked = Signal(dict)
    confirm_clicked = Signal(dict)

    def __init__(self):
        super().__init__()
        self._data = {}
        self._build()

    def _row(self, layout, label: str):
        row = QHBoxLayout()
        lbl = QLabel(label)
        lbl.setFixedWidth(130)
        lbl.setStyleSheet(f"color:{C['muted']}; font-size:13px;")
        val = QLabel("—")
        val.setStyleSheet(f"color:{C['text']}; font-size:13px;")
        row.addWidget(lbl)
        row.addWidget(val, stretch=1)
        layout.addLayout(row)
        return val

    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        # top bar
        bar = QFrame()
        bar.setFixedHeight(64)
        bar.setStyleSheet(f"background:{C['bg']}; border-bottom:1px solid {C['border']};")
        bl = QHBoxLayout(bar)
        bl.setContentsMargins(32, 0, 32, 0)
        t = QLabel("Review & Confirm")
        t.setFont(QFont("Segoe UI", 16, QFont.Bold))
        bl.addWidget(t)
        bl.addStretch()

        body = QWidget()
        body.setStyleSheet(f"background:{C['bg']};")
        form = QVBoxLayout(body)
        form.setContentsMargins(40, 28, 40, 28)
        form.setSpacing(20)

        form.addWidget(section_label("STUDENT INFORMATION"))
        self.v_id = self._row(form, "Student ID")
        self.v_name = self._row(form, "Full Name")
        self.v_fac = self._row(form, "Faculty")
        self.v_maj = self._row(form, "Major")
        
        form.addSpacing(10)
        form.addWidget(divider())
        form.addWidget(section_label("COURSES"))
        self.v_courses = [self._row(form, f"Course {i+1}") for i in range(3)]

        form.addStretch()

        btn_row = QHBoxLayout()
        be = QPushButton("← Edit")
        be.setStyleSheet(btn_ss(C['bg'], C['surface'], C['muted'], border=f"1px solid {C['border']}"))
        be.clicked.connect(lambda: self.edit_clicked.emit(self._data))

        bc = QPushButton("Confirm Registration")
        bc.setStyleSheet(btn_ss(C['green'], "#15803d"))
        bc.clicked.connect(lambda: self.confirm_clicked.emit(self._data))

        btn_row.addWidget(be)
        btn_row.addStretch()
        btn_row.addWidget(bc)
        form.addLayout(btn_row)

        root.addWidget(bar)
        root.addWidget(body)

    def load_data(self, d: dict):
        self._data = d
        self.v_id.setText(d['id'])
        self.v_name.setText(d['fullname'])
        self.v_fac.setText(d['faculty'])
        self.v_maj.setText(d['major'])
        
        for i, val_lbl in enumerate(self.v_courses):
            if i < len(d['courses']):
                code = d['courses'][i]
                
                # ค้นหาชื่อเต็มจาก List COURSES ใน data.py
                full_name = ""
                for item in COURSES:
                    if item.startswith(code):
                        full_name = item
                        break
                
                # ถ้าหาเจอให้แสดงชื่อเต็ม ถ้าไม่เจอให้แสดงแค่รหัส
                display_text = full_name if full_name else code
                val_lbl.setText(display_text)
            else:
                val_lbl.setText("—")


# ─────────────────────────────────────────────────────────────
#  Main Window
# ─────────────────────────────────────────────────────────────
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Registration")
        self.setMinimumSize(860, 580)
        self.resize(980, 660)
        self.setStyleSheet(BASE)
        self._build()

    def _build(self):
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.p1 = StudentListPage()
        self.p2 = AddStudentPage()
        self.p3 = ReviewPage()

        self.stack.addWidget(self.p1)
        self.stack.addWidget(self.p2)
        self.stack.addWidget(self.p3)

        # Signals connecting
        self.p1.go_to_add.connect(lambda: self.stack.setCurrentWidget(self.p2))
        
        self.p2.cancel_clicked.connect(self._on_cancel_add)
        self.p2.review_requested.connect(self._on_review)
        
        self.p3.edit_clicked.connect(self._on_edit)
        self.p3.confirm_clicked.connect(self._on_confirm)

    def _on_cancel_add(self):
        self.p2.clear_form()
        self.stack.setCurrentWidget(self.p1)

    def _on_review(self, data):
        self.p3.load_data(data)
        self.stack.setCurrentWidget(self.p3)

    def _on_edit(self, data):
        self.p2.load_data(data)
        self.stack.setCurrentWidget(self.p2)

    def _on_confirm(self, data):
        self.p1.add_student(data)
        self.p2.clear_form()
        QMessageBox.information(self, "Success", "Registration completed successfully!")
        self.stack.setCurrentWidget(self.p1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    w = MainWindow()
    w.show()
    sys.exit(app.exec())