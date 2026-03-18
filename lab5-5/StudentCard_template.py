from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QPushButton, QFrame,
)
from PySide6.QtCore import Qt, Signal, QMimeData, QPoint
from PySide6.QtGui import QFont, QCursor, QDrag, QPixmap

from style import C
from data import COURSES

class StudentCard(QFrame):
    delete_requested = Signal(object)
    # Signal for delete request: emits self
     

    def __init__(self, data: dict, parent=None):
        super().__init__(parent)
        self.data = data

        # for drag and drop
        self._drag_start: QPoint | None = None
        self.setAcceptDrops(False)
        self.setCursor(QCursor(Qt.OpenHandCursor))
        
        self._build()


    def _build(self):
        # Extract data
        name = f"{self.data.get('firstname', '')} {self.data.get('lastname', '')}".strip()
        student_id = self.data.get('id', '')
        faculty = self.data.get('faculty', '')
        major = self.data.get('major', '')
        courses = self.data.get('courses', [])

        # Create course code to full name mapping
        course_map = {}
        for item in COURSES:
            if "·" in item:
                parts = item.split("·")
                code = parts[0].strip()
                full_name = item.strip()  # "CS101 · Intro to Programming"
                course_map[code] = full_name

        # Convert course codes to full names
        course_displays = [course_map.get(code, code) for code in courses]

        # height depends on number of courses selected
        # base height: name + dept rows, plus 18px per course line
        self.setMinimumHeight(70 + len(courses) * 18)

        self.setStyleSheet(f"""
            QFrame {{
                background:{C['card']};
                border-radius:8px;
                padding:12px;
            }}
            QFrame:hover {{
                background:{C['surface']};
            }}
        """)

        # Main layout (horizontal)
        main_lay = QHBoxLayout(self)
        main_lay.setContentsMargins(8, 8, 8, 8)
        main_lay.setSpacing(10)

        # Left: drag handle
        handle = QLabel("⠿")
        handle.setFixedWidth(16)
        handle.setAlignment(Qt.AlignTop)
        handle.setStyleSheet(f"background:transparent; color:{C['muted']};font-size:16px;padding-top:4px;")
        main_lay.addWidget(handle)

        # Center: student info (vertical layout)
        info_lay = QVBoxLayout()
        info_lay.setContentsMargins(0, 0, 0, 0)
        info_lay.setSpacing(4)

        # Name + ID row
        name_id_lay = QHBoxLayout()
        name_id_lay.setContentsMargins(0, 0, 0, 0)
        name_id_lay.setSpacing(8)
        
        lbl_name = QLabel(name)
        lbl_name.setStyleSheet(f"color:{C['text']}; font-weight:bold; font-size:14px;")
        
        lbl_id = QLabel(student_id)
        lbl_id.setStyleSheet(f"color:{C['muted']}; font-size:12px;")
        
        name_id_lay.addWidget(lbl_name)
        name_id_lay.addStretch()
        name_id_lay.addWidget(lbl_id)
        info_lay.addLayout(name_id_lay)

        # Faculty + Major row
        lbl_dept = QLabel(f"{faculty} · {major}")
        lbl_dept.setStyleSheet(f"color:{C['muted']}; font-size:12px;")
        info_lay.addWidget(lbl_dept)

        # Courses (each on separate line)
        if course_displays:
            for course_display in course_displays:
                lbl_course = QLabel(course_display)
                lbl_course.setStyleSheet(f"color:{C['text']}; font-size:12px;")
                lbl_course.setWordWrap(True)
                info_lay.addWidget(lbl_course)

        main_lay.addLayout(info_lay, stretch=1)

        # Right: delete button
        self.btn_del = QPushButton("✕")
        self.btn_del.setFixedSize(28, 28)
        self.btn_del.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_del.setStyleSheet(f"""
            QPushButton {{
                background:transparent;
                color:{C['muted']};
                border:none;
                border-radius:14px;
                font-size:12px;
                font-weight:bold;
            }}
            QPushButton:hover {{
                background:{C['red']};
                color:white;
                border:none;
            }}
        """)
        self.btn_del.clicked.connect(lambda: self.delete_requested.emit(self))
        main_lay.addWidget(self.btn_del, alignment=Qt.AlignTop)
        
    # ── Drag support ──────────────────────────────────────────
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_start = event.pos()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if (event.buttons() & Qt.LeftButton) and self._drag_start is not None:
            if (event.pos() - self._drag_start).manhattanLength() > 10:
                drag = QDrag(self)
                mime = QMimeData()
                mime.setText("student_card")
                drag.setMimeData(mime)

                pix = QPixmap(self.size())
                pix.fill(Qt.transparent)
                self.render(pix)
                drag.setPixmap(pix)
                drag.setHotSpot(event.pos())
                drag.exec(Qt.MoveAction)
        super().mouseMoveEvent(event)
