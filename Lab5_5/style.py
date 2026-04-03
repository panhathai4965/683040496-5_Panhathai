from PySide6.QtWidgets import QLabel, QFrame

C = {
    "bg":      "#ffffff",
    "surface": "#f0bcab",
    "card":    "#efd0d0",
    "border":  "#dee2e6",
    "accent":  "#2563eb",
    "purple":  "#7c3aed",
    "green":   "#16a34a",
    "red":     "#dc2626",
    "text":    "#111827",
    "muted":   "#6b7280",
    "gold":    "#d97706",
}

BASE = (
    f"background-color:{C['bg']};"
    f"color:{C['text']};"
    f"font-family:'Segoe UI','Helvetica Neue',sans-serif;"
)

INPUT_SS = f"""
QLineEdit {{
    background:{C['bg']};
    border:1px solid {C['border']};
    border-radius:6px;
    padding:8px 12px;
    color:{C['text']};
    font-size:13px;
}}
QLineEdit:focus {{
    border:1.5px solid {C['accent']};
}}
"""

COMBO_SS = f"""
QComboBox {{
    background:{C['bg']};
    border:1px solid {C['border']};
    border-radius:6px;
    padding:8px 12px;
    color:{C['text']};
    font-size:13px;
}}
QComboBox:focus {{
    border:1.5px solid {C['accent']};
}}
QComboBox::drop-down {{
    border:none;
    width:24px;
}}
QComboBox QAbstractItemView {{
    background:{C['bg']};
    border:1px solid {C['border']};
    color:{C['text']};
    selection-background-color:{C['accent']};
    selection-color:white;
    padding:4px;
}}
"""

SCROLL_SS = f"""
QScrollArea {{
    border:none;
    background:transparent;
}}
QScrollBar:vertical {{
    background:{C['surface']};
    width:6px;
    border-radius:3px;
}}
QScrollBar::handle:vertical {{
    background:{C['border']};
    border-radius:3px;
    min-height:30px;
}}
QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {{
    height:0;
}}
"""

# ─────────────────────────────────────────────────────────────
#  Shared helpers
# ─────────────────────────────────────────────────────────────
def btn_ss(bg: str, hover: str, fg: str = "#ffffff", border: str = "none") -> str:
    return f"""
        QPushButton {{
            background:{bg}; color:{fg};
            border:{border};
            border-radius:6px; padding:8px 20px;
            font-size:13px; font-weight:600;
        }}
        QPushButton:hover {{ background:{hover}; }}
    """

def section_label(text: str) -> QLabel:
    lbl = QLabel(text)
    lbl.setStyleSheet(
        f"color:{C['muted']};font-size:11px;font-weight:700;"
        f"letter-spacing:0.5px;text-transform:uppercase;"
    )
    return lbl


def field_label(text: str) -> QLabel:
    lbl = QLabel(text)
    lbl.setStyleSheet(f"color:{C['text']};font-size:13px;")
    lbl.setFixedWidth(110)
    return lbl

def divider() -> QFrame:
    line = QFrame()
    line.setFrameShape(QFrame.HLine)
    line.setStyleSheet(f"border:none; border-top:1px solid {C['border']};")
    line.setFixedHeight(1)
    return line

