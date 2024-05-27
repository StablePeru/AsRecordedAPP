from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QGridLayout, QScrollArea, QMessageBox, QCompleter, QPlainTextEdit, QCheckBox, QProgressBar, QStyleFactory, QStyle, QShortcut, QDialog
from PyQt5.QtCore import Qt, QEvent, QTimer
from PyQt5.QtGui import QValidator, QKeySequence
from .custom_widgets import CharacterLabel, TimecodeLineEdit, CustomMessageBox, CharacterFilterDialog
from .main_widget import MainWidget  # Importar MainWidget
import pandas as pd

class CharacterFilterDialog(QDialog):
    def __init__(self, parent=None, character_names=None, active_characters=None):
        super().__init__(parent)
        self.setWindowTitle("Seleccionar Personajes")
        self.character_names = character_names if character_names else []
        self.active_characters = active_characters if active_characters else {}
        self.layout = QVBoxLayout(self)
        self.checkboxes = {}
        self.init_ui()

    def init_ui(self):
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Buscar personajes...")
        self.search_bar.textChanged.connect(self.filter_characters)
        self.layout.addWidget(self.search_bar)

        self.character_container = QWidget()
        self.character_layout = QVBoxLayout(self.character_container)
        
        for character in self.character_names:
            checkbox = QCheckBox(character)
            checkbox.setChecked(self.active_characters.get(character, True))
            self.character_layout.addWidget(checkbox)
            self.checkboxes[character] = checkbox

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.character_container)
        self.scroll_area.setWidgetResizable(True)
        self.layout.addWidget(self.scroll_area)

        self.save_button = QPushButton("Guardar")
        self.save_button.clicked.connect(self.save_selection)
        self.layout.addWidget(self.save_button)

    def filter_characters(self, text):
        for character, checkbox in self.checkboxes.items():
            checkbox.setParent(None)
            if text.lower() in character.lower():
                self.character_layout.addWidget(checkbox)

    def save_selection(self):
        for character, checkbox in self.checkboxes.items():
            self.active_characters[character] = checkbox.isChecked()
        self.accept()
