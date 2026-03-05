import sys
import random
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QComboBox, QSlider, QPushButton, 
                             QStatusBar, QToolBar, QFileDialog, QFrame)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QIcon

class RPGCharacterBuilder(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RPG Character Builder")
        self.setMinimumSize(800, 500)
        
        # --- ข้อมูลพื้นฐาน ---
        self.races = ["Human", "Elf", "Dwarf", "Orc", "Undead"]
        self.classes = ["Warrior", "Mage", "Rogue", "Paladin", "Ranger"]
        self.genders = ["Male", "Female", "Other"]
        
        self.init_ui()
        self.reset_fields()

    def init_ui(self):
        # Main Widget and Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # --- Left Panel: Form ---
        left_panel = QVBoxLayout()
        
        # Character Info
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter character name...")
        
        self.race_combo = QComboBox()
        self.race_combo.addItems(self.races)
        
        self.class_combo = QComboBox()
        self.class_combo.addItems(self.classes)
        
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(self.genders)

        left_panel.addWidget(QLabel("Character Name:"))
        left_panel.addWidget(self.name_input)
        left_panel.addWidget(QLabel("Race:"))
        left_panel.addWidget(self.race_combo)
        left_panel.addWidget(QLabel("Class:"))
        left_panel.addWidget(self.class_combo)
        left_panel.addWidget(QLabel("Gender:"))
        left_panel.addWidget(self.gender_combo)

        # Stat Allocation
        left_panel.addSpacing(20)
        left_panel.addWidget(QLabel("<b>Stat Allocation</b>"))
        
        self.stats = {}
        for stat_name in ["STR", "DEX", "INT", "VIT"]:
            row = QHBoxLayout()
            label = QLabel(f"{stat_name}:")
            label.setFixedWidth(40)
            slider = QSlider(Qt.Orientation.Horizontal)
            slider.setRange(1, 20)
            slider.setValue(5)
            val_label = QLabel("5")
            
            slider.valueChanged.connect(self.update_stats_display)
            
            row.addWidget(label)
            row.addWidget(slider)
            row.addWidget(val_label)
            left_panel.addLayout(row)
            self.stats[stat_name] = (slider, val_label)

        self.points_label = QLabel("Points used: 20 / 40")
        left_panel.addWidget(self.points_label)

        # Generate Button
        self.gen_btn = QPushButton("Generate Character Sheet")
        self.gen_btn.clicked.connect(self.generate_sheet)
        left_panel.addWidget(self.gen_btn)
        
        main_layout.addLayout(left_panel, stretch=2)

        # --- Right Panel: Character Sheet Display ---
        self.display_panel = QFrame()
        self.display_panel.setFixedWidth(300)
        self.display_panel.setStyleSheet("background-color: #1a1a2e; color: white; border-radius: 10px;")
        display_layout = QVBoxLayout(self.display_panel)
        
        self.sheet_name = QLabel("— Character Name —")
        self.sheet_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.sheet_name.setStyleSheet("font-size: 18px; font-weight: bold; color: #a29bfe;")
        
        self.sheet_sub = QLabel("Race • Class")
        self.sheet_sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        display_layout.addWidget(self.sheet_name)
        display_layout.addWidget(self.sheet_sub)
        display_layout.addSpacing(20)

        self.stat_bars = {}
        for stat_name in ["STR", "DEX", "INT", "VIT"]:
            row = QHBoxLayout()
            row.addWidget(QLabel(stat_name))
            bar = QLabel("") # ใช้ตัวอักษรสร้างบาร์ตามโจทย์
            bar.setStyleSheet("color: #00d2ff;")
            row.addWidget(bar)
            display_layout.addLayout(row)
            self.stat_bars[stat_name] = bar
            
        display_layout.addStretch()
        main_layout.addWidget(self.display_panel)

        # --- Menu & Toolbar ---
        self.create_menus_and_toolbar()

        # --- Status Bar ---
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.perm_label = QLabel("Created by: Your Name")
        self.status_bar.addPermanentWidget(self.perm_label)

    def create_menus_and_toolbar(self):
        # Actions
        new_act = QAction("New Character", self)
        new_act.triggered.connect(self.reset_fields)
        
        gen_act = QAction("Generate Sheet", self)
        gen_act.triggered.connect(self.generate_sheet)
        
        save_act = QAction("Save Sheet", self)
        save_act.triggered.connect(self.save_to_file)
        
        rand_act = QAction("Randomize", self)
        rand_act.triggered.connect(self.randomize_all)

        reset_stats_act = QAction("Reset Stats", self)
        reset_stats_act.triggered.connect(self.reset_stats_only)

        exit_act = QAction("Exit", self)
        exit_act.triggered.connect(self.close)

        # Menu Bar
        menu_bar = self.menuBar()
        game_menu = menu_bar.addMenu("Game")
        game_menu.addAction(new_act)
        game_menu.addAction(gen_act)
        game_menu.addAction(save_act)
        game_menu.addSeparator()
        game_menu.addAction(exit_act)

        edit_menu = menu_bar.addMenu("Edit")
        edit_menu.addAction(reset_stats_act)
        edit_menu.addAction(rand_act)

        # Tool Bar
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)
        toolbar.addAction(new_act)
        toolbar.addAction(gen_act)
        toolbar.addAction(rand_act)
        toolbar.addAction(save_act)

    # --- Logic ---
    def update_stats_display(self):
        total = 0
        for name, (slider, label) in self.stats.items():
            val = slider.value()
            label.setText(str(val))
            total += val
        
        self.points_label.setText(f"Points used: {total} / 40")
        if total > 40:
            self.points_label.setStyleSheet("color: red; font-weight: bold;")
        else:
            self.points_label.setStyleSheet("color: black;")

    def generate_sheet(self):
        name = self.name_input.text() if self.name_input.text() else "Unknown Hero"
        race = self.race_combo.currentText()
        char_class = self.class_combo.currentText()
        
        self.sheet_name.setText(f"— {name} —")
        self.sheet_sub.setText(f"{race} • {char_class}")
        
        for name, (slider, _) in self.stats.items():
            val = slider.value()
            self.stat_bars[name].setText("█" * val + f" {val}")
            
        self.status_bar.showMessage("Character sheet updated!", 3000)

    def randomize_all(self):
        self.name_input.setText(random.choice(["Aragon", "Legolas", "Gimli", "Gandalf", "Frodo"]))
        self.race_combo.setCurrentIndex(random.randint(0, 4))
        self.class_combo.setCurrentIndex(random.randint(0, 4))
        
        # Random Stats (Total <= 40)
        remaining = 40
        for i, (name, (slider, _)) in enumerate(self.stats.items()):
            if i < 3:
                val = random.randint(1, min(20, remaining - (3 - i)))
                slider.setValue(val)
                remaining -= val
            else:
                slider.setValue(min(20, remaining))
        
        self.status_bar.showMessage("Randomized character attributes!", 3000)

    def reset_fields(self):
        self.name_input.clear()
        self.race_combo.setCurrentIndex(0)
        self.class_combo.setCurrentIndex(0)
        self.reset_stats_only()
        self.status_bar.showMessage("Form reset to default.", 3000)

    def reset_stats_only(self):
        for slider, label in self.stats.values():
            slider.setValue(5)
        self.update_stats_display()

    def save_to_file(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save Character", "", "Text Files (*.txt)")
        if path:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(f"CHARACTER SHEET\n{'='*20}\n")
                f.write(f"Name: {self.name_input.text()}\n")
                f.write(f"Race: {self.race_combo.currentText()}\n")
                f.write(f"Class: {self.class_combo.currentText()}\n")
                for name, (slider, _) in self.stats.items():
                    f.write(f"{name}: {slider.value()}\n")
            self.status_bar.showMessage(f"Saved to {path}", 3000)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RPGCharacterBuilder()
    window.show()
    sys.exit(app.exec())