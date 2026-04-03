"""
Panhathai Suporn
683040496-5
P1
"""
import sys
import json
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QScrollArea, QLabel, QDialog,
    QLineEdit, QComboBox, QDateEdit, QFormLayout,
    QMessageBox, QFileDialog, QFrame, QSizePolicy
)
from PySide6.QtCore import Qt, QDate, Signal
from PySide6.QtGui import QFont


# ─────────────────────────────────────────────
# Priority config
# ─────────────────────────────────────────────
PRIORITY_LEVELS = ["Low", "Medium", "High", "Critical"]

PRIORITY_COLORS = {
    "Low": "#d4edda",
    "Medium": "#cce5ff",
    "High": "#fff3cd",
    "Critical": "#f8d7da",
}

PRIORITY_BORDER = {
    "Low": "#28a745",
    "Medium": "#4a90d9",
    "High": "#ffc107",
    "Critical": "#dc3545",
}

PRIORITY_BADGE = {
    "Low": ("#28a745", "#ffffff"),
    "Medium": ("#4a90d9", "#ffffff"),
    "High": ("#ffc107", "#000000"),
    "Critical": ("#dc3545", "#ffffff"),
}


# ─────────────────────────────────────────────
# TaskCard – individual card widget
# ─────────────────────────────────────────────
class TaskCard(QFrame):
    delete_requested = Signal(object)

    def __init__(self, task: dict, parent=None):
        super().__init__(parent)
        self.task = task
        self._build_ui()
        self._apply_style()

    def _build_ui(self):
        self.setFixedHeight(100)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        priority = self.task.get("priority", "Low")
        border_color = PRIORITY_BORDER[priority]

        top_row = QHBoxLayout()
        top_row.setSpacing(8)

        self.lbl_title = QLabel(self.task["title"])
        self.lbl_title.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.lbl_title.setWordWrap(True)
        self.lbl_title.setStyleSheet("color:#1a1a2e;")
        top_row.addWidget(self.lbl_title, stretch=1)

        btn_done = QPushButton("✓ Done")
        btn_done.setFixedSize(72, 28)
        btn_done.setCursor(Qt.PointingHandCursor)
        btn_done.setToolTip("Mark as done and remove")
        btn_done.setStyleSheet(
            f"QPushButton{{background:transparent; border:1.5px solid {border_color};"
            f"border-radius:6px; font-size:9pt; color:{border_color}; font-weight:bold;}}"
            f"QPushButton:hover{{background:{border_color}; color:#fff;}}"
        )
        btn_done.clicked.connect(lambda: self.delete_requested.emit(self))
        top_row.addWidget(btn_done, alignment=Qt.AlignTop)

        bottom_row = QHBoxLayout()
        bottom_row.setSpacing(8)

        deadline_str = self.task.get("deadline", "No deadline")
        lbl_dead = QLabel(f"📅 {deadline_str}")
        lbl_dead.setFont(QFont("Segoe UI", 9))
        lbl_dead.setStyleSheet("color:#555;")
        bottom_row.addWidget(lbl_dead)
        bottom_row.addStretch()

        bg, fg = PRIORITY_BADGE[priority]
        badge = QLabel(priority.upper())
        badge.setFixedSize(70, 20)
        badge.setAlignment(Qt.AlignCenter)
        badge.setStyleSheet(
            f"background:{bg}; color:{fg}; border-radius:9px;"
            f"font-size:8px; font-weight:bold; letter-spacing:1px;"
        )
        bottom_row.addWidget(badge)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(14, 10, 14, 10)
        outer.setSpacing(6)
        outer.addLayout(top_row)
        outer.addLayout(bottom_row)

    def _apply_style(self):
        priority = self.task.get("priority", "Low")
        bg = PRIORITY_COLORS[priority]
        border = PRIORITY_BORDER[priority]
        self.setStyleSheet(
            f"TaskCard{{background:{bg}; border:1.5px solid {border};"
            f"border-radius:12px;}}"
            f"TaskCard:hover{{border:2px solid {border};}}"
        )


# ─────────────────────────────────────────────
# AddTaskDialog – pop-up form
# ─────────────────────────────────────────────
class AddTaskDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Task")
        self.setFixedSize(300, 250)
        self.setStyleSheet("""
            QDialog { background: #f8f9fa; }
            QLabel { font-family:'Segoe UI'; font-size:10pt; color:#333; }
            QLineEdit {
                border:1.5px solid #ced4da; border-radius:8px;
                padding:6px 10px; font-size:10pt; background:#fff;
            }
            QLineEdit:focus { border-color:#4a90d9; }
            QComboBox {
                border:1.5px solid #ced4da; border-radius:8px;
                padding:5px 10px; font-size:10pt; background:#fff;
            }
            QCalendarWidget { border:1px solid #ced4da; border-radius:8px; }
        """)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(14)

        heading = QLabel("New Task")
        heading.setFont(QFont("Segoe UI", 14, QFont.Bold))
        heading.setStyleSheet("color:#222;")
        layout.addWidget(heading)

        form = QFormLayout()
        form.setSpacing(10)
        form.setLabelAlignment(Qt.AlignRight)

        self.inp_title = QLineEdit()
        self.inp_title.setPlaceholderText("Enter task name…")
        form.addRow("Task:", self.inp_title)

        self.cmb_priority = QComboBox()
        self.cmb_priority.addItems(PRIORITY_LEVELS)
        form.addRow("Priority:", self.cmb_priority)

        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setMinimumDate(QDate.currentDate())
        self.date_edit.setDisplayFormat("yyyy-MM-dd")
        self.date_edit.setCalendarPopup(True)
        form.addRow("Deadline:", self.date_edit)

        layout.addLayout(form)

        btn_row = QHBoxLayout()

        btn_cancel = QPushButton("Cancel")
        btn_cancel.setFixedHeight(36)
        btn_cancel.setStyleSheet(
            "QPushButton{background:#e9ecef;border:none;border-radius:8px;"
            "font-size:10pt;color:#555;}"
            "QPushButton:hover{background:#dee2e6;}"
        )
        btn_cancel.clicked.connect(self.reject)

        btn_add = QPushButton("Add Task")
        btn_add.setFixedHeight(36)
        btn_add.setStyleSheet(
            "QPushButton{background:#4a90d9;border:none;border-radius:8px;"
            "font-size:10pt;color:#fff;font-weight:bold;}"
            "QPushButton:hover{background:#357abd;}"
        )
        btn_add.clicked.connect(self._on_add)

        btn_row.addWidget(btn_cancel)
        btn_row.addSpacing(10)
        btn_row.addWidget(btn_add)
        layout.addLayout(btn_row)

    def _on_add(self):
        if not self.inp_title.text().strip():
            QMessageBox.warning(self, "Missing Info", "Please enter a task name.")
            return
        self.accept()

    def get_task(self) -> dict:
        return {
            "title": self.inp_title.text().strip(),
            "priority": self.cmb_priority.currentText(),
            "deadline": self.date_edit.date().toString("yyyy-MM-dd"),
            "done": False,
        }


# ─────────────────────────────────────────────
# MainWindow
# ─────────────────────────────────────────────
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📝 To-Do List")
        self.setMinimumSize(560, 600)
        self.resize(640, 720)
        self.tasks: list[dict] = []
        self.cards: list[TaskCard] = []
        self._build_ui()
        self._apply_global_style()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(20, 16, 20, 16)
        root.setSpacing(12)

        # Header
        header = QHBoxLayout()
        app_title = QLabel("My To-Do List")
        app_title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        app_title.setStyleSheet("color:#1a1a2e;")
        header.addWidget(app_title)
        header.addStretch()
        self.lbl_count = QLabel("0 tasks")
        self.lbl_count.setStyleSheet("color:#888; font-size:10pt;")
        header.addWidget(self.lbl_count)
        root.addLayout(header)

        # Toolbar
        toolbar = QHBoxLayout()
        toolbar.setSpacing(8)
        btn_add = self._make_btn("＋ Add Task", "#4a90d9", "#357abd")
        btn_load = self._make_btn("📂 Load JSON", "#6c757d", "#545b62")
        btn_save = self._make_btn("💾 Save JSON", "#28a745", "#1e7e34")
        btn_add.clicked.connect(self._add_task)
        btn_load.clicked.connect(self._load_json)
        btn_save.clicked.connect(self._save_json)
        toolbar.addWidget(btn_add)
        toolbar.addWidget(btn_load)
        toolbar.addWidget(btn_save)
        toolbar.addStretch()
        root.addLayout(toolbar)

        # Divider
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("color:#dee2e6;")
        root.addWidget(line)

        # Scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.NoFrame)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.card_container = QWidget()
        self.card_layout = QVBoxLayout(self.card_container)
        self.card_layout.setContentsMargins(0, 4, 0, 4)
        self.card_layout.setSpacing(10)
        self.card_layout.addStretch()
        self.scroll_area.setWidget(self.card_container)
        root.addWidget(self.scroll_area, stretch=1)

        # Empty state
        self.lbl_empty = QLabel("No tasks yet.\nClick ＋ Add Task to get started!")
        self.lbl_empty.setAlignment(Qt.AlignCenter)
        self.lbl_empty.setStyleSheet("color:#bbb; font-size:12pt;")
        self.card_layout.insertWidget(0, self.lbl_empty)

        self._refresh_empty()

    def _make_btn(self, text, color, hover) -> QPushButton:
        btn = QPushButton(text)
        btn.setFixedHeight(36)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet(
            f"QPushButton{{background:{color};border:none;border-radius:8px;"
            f"font-size:10pt;color:#fff;padding:0 14px;}}"
            f"QPushButton:hover{{background:{hover};}}"
        )
        return btn

    def _apply_global_style(self):
        self.setStyleSheet("""
            QMainWindow { background:#f0f2f5; color: black; }
            QWidget { background:#f0f2f5; color: black; }   
            QLabel { color: black; }                         
            QScrollArea { background:transparent; }
            QScrollBar:vertical {
                background:#e9ecef; width:8px; border-radius:4px;
            }
            QScrollBar::handle:vertical {
                background:#adb5bd; border-radius:4px; min-height:20px;
            }
        """)
    
    # ── task management ─────────────────────────
    def _add_task(self):
        dlg = AddTaskDialog(self)
        if dlg.exec() == QDialog.Accepted:
            task = dlg.get_task()
            self.tasks.append(task)
            self._insert_card(task)
            self._refresh_count()
            self._refresh_empty()

    def _insert_card(self, task: dict):
        card = TaskCard(task)
        card.delete_requested.connect(self._remove_card)
        idx = self.card_layout.count() - 1  # before trailing stretch
        self.card_layout.insertWidget(idx, card)
        self.cards.append(card)

    def _remove_card(self, card: TaskCard):
        card.task["done"] = True
        self.cards.remove(card)
        self.card_layout.removeWidget(card)
        card.deleteLater()
        self._refresh_count()
        self._refresh_empty()

    # ── JSON IO ─────────────────────────────────
    def _save_json(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Save Tasks", "tasks.json", "JSON Files (*.json)"
        )
        if not path:
            return
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.tasks, f, indent=2, ensure_ascii=False)
        QMessageBox.information(self, "Saved", f"Tasks saved to:\n{path}")

    def _load_json(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Load Tasks", "", "JSON Files (*.json)"
        )
        if not path:
            return

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Clear existing cards and tasks
        for card in list(self.cards):
            self.card_layout.removeWidget(card)
            card.deleteLater()
        self.cards.clear()
        self.tasks.clear()

        # Populate from loaded data
        for task in data:
            self.tasks.append(task)
            if not task.get("done", False):
                self._insert_card(task)

        self._refresh_count()
        self._refresh_empty()
        QMessageBox.information(self, "Loaded", f"Loaded {len(self.tasks)} tasks.")

    # ── helpers ─────────────────────────────────
    def _refresh_count(self):
        n = len(self.tasks)
        done = sum(1 for t in self.tasks if t.get("done"))
        self.lbl_count.setText(f"{done}/{n} done")

    def _refresh_empty(self):
        has = len(self.cards) > 0
        self.lbl_empty.setVisible(not has)


# ─────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())