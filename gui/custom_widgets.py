from PyQt5.QtWidgets import QLabel, QPlainTextEdit, QLineEdit, QCheckBox, QMessageBox, QVBoxLayout, QScrollArea, QPushButton, QWidget, QDialog
from PyQt5.QtCore import Qt, QEvent

class CharacterLabel(QLabel):
    def __init__(self, character_name, parent=None):
        super().__init__(character_name, parent)
        self.setObjectName("characterLabel")
        self.setMouseTracking(True)

    def enterEvent(self, event):
        self.setStyleSheet("background-color: lightblue;")
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setStyleSheet("")
        super().leaveEvent(event)

class CustomMessageBox(QMessageBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for widget in self.findChildren(QWidget):
            if isinstance(widget, QLabel):
                widget.setStyleSheet("font-weight: 12px;")

class TimecodeLineEdit(QLineEdit):
    def __init__(self, data_handler, intervention_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data_handler = data_handler
        self.intervention_id = intervention_id
        self.installEventFilter(self)

    def eventFilter(self, source, event):
        if event.type() == QEvent.KeyPress and event.key() >= Qt.Key_0 and event.key() <= Qt.Key_9:
            new_text = self.format_new_text(self.text(), event.text())
            self.setText(new_text)
            return True
        return super().eventFilter(source, event)

    def format_new_text(self, current_text, new_digit):
        current_text = current_text.replace(':', '')
        new_text = current_text[1:] + new_digit
        formatted_text = ':'.join(new_text[i:i+2] for i in range(0, len(new_text), 2))
        return formatted_text[0:2] + ":" + formatted_text[2:4] + ":" + formatted_text[4:6] + ":" + formatted_text[6:]

    def focusInEvent(self, e):
        super().focusInEvent(e)
        self.selectAll()

    def focusOutEvent(self, e):
        super().focusOutEvent(e)
        self.data_handler.update_timecode(self.intervention_id, self.text())

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
