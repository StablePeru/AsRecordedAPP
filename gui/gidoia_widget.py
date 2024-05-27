from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QGridLayout, QScrollArea, QMessageBox, QCompleter, QPlainTextEdit, QCheckBox, QProgressBar, QStyleFactory, QStyle, QShortcut
from PyQt5.QtCore import Qt, QEvent, QTimer
from PyQt5.QtGui import QValidator, QKeySequence
from .custom_widgets import CharacterLabel, TimecodeLineEdit, CustomMessageBox, CharacterFilterDialog
import pandas as pd

class GidoiaWidget(QWidget):
    def __init__(self, data_handler, parent=None):
        super().__init__(parent)
        self.data_handler = data_handler
        self.current_take_number = 1
        self.character_name = None
        self.search_active = False
        self.active_characters = {name: True for name in self.get_character_names()}
        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)
        self.create_search_layouts()
        self.create_navigation_buttons()
        self.create_take_label()
        self.dialogue_layout = QGridLayout()
        self.main_layout.addLayout(self.dialogue_layout)
        self.create_back_button()
        self.character_completer = QCompleter(self.get_character_names())
        self.character_completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.character_input.setCompleter(self.character_completer)
        self.load_take(self.current_take_number)
        self.setup_shortcuts()

    def setup_shortcuts(self):
        QShortcut(QKeySequence("Ctrl+N"), self, self.load_next_take)
        QShortcut(QKeySequence("Ctrl+P"), self, self.load_previous_take)
        QShortcut(QKeySequence("Ctrl+S"), self, self.save_changes)

    def create_search_layouts(self):
        self.take_search_layout = QHBoxLayout()
        self.take_number_input = QLineEdit()
        self.take_number_input.returnPressed.connect(self.load_take_from_input)
        self.take_search_button = self.create_button("Take-a bilatu", self.load_take_from_input)
        self.take_search_layout.addWidget(self.take_number_input)
        self.take_search_layout.addWidget(self.take_search_button)

        self.character_search_layout = QHBoxLayout()
        self.character_input = QLineEdit()
        self.character_input.returnPressed.connect(self.load_character_from_input)
        self.character_search_button = self.create_button("Pertsonaia bilatu", self.load_character_from_input)
        self.character_search_layout.addWidget(self.character_input)
        self.character_search_layout.addWidget(self.character_search_button)

        self.search_layout = QHBoxLayout()
        self.search_layout.addLayout(self.take_search_layout)
        self.search_layout.addLayout(self.character_search_layout)
        self.main_layout.addLayout(self.search_layout)

    def create_navigation_buttons(self):
        self.navigation_layout = QHBoxLayout()
        self.prev_button = self.create_button("Take anterior", self.load_previous_take)
        self.characters_button = self.create_button("Personajes", self.open_character_filter_dialog)
        self.next_button = self.create_button("Siguiente Take", self.load_next_take)
        self.navigation_layout.addWidget(self.prev_button)
        self.navigation_layout.addWidget(self.characters_button)
        self.navigation_layout.addWidget(self.next_button)
        self.main_layout.addLayout(self.navigation_layout)

    def create_take_label(self):
        self.take_label = QLabel()
        self.take_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.take_label)

    def create_back_button(self):
        self.back_button = self.create_button("Main Page", self.go_back)
        self.main_layout.addWidget(self.back_button)

    def create_button(self, text, function):
        button = QPushButton(text)
        button.clicked.connect(function)
        return button

    def get_character_names(self):
        return self.data_handler.get_character_names()

    def go_back(self):
        reply = QMessageBox.question(self, "Gorde", "Programa itxi aurretik gorde nahi?", QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)
        if reply == QMessageBox.Cancel:
            return
        if reply == QMessageBox.Yes:
            self.data_handler.save()
        self.window().set_main_widget()

    def open_character_filter_dialog(self):
        dialog = CharacterFilterDialog(self, self.get_character_names(), self.active_characters)
        if dialog.exec_():
            self.active_characters = dialog.active_characters
            self.load_take(self.current_take_number)

    def validate_take_number(self, take_number):
        try:
            take_number = int(take_number)
        except ValueError:
            QMessageBox.warning(self, "Warning", "Invalid take number.")
            return None
        if not (1 <= take_number <= len(self.data_handler.takes)):
            QMessageBox.warning(self, "Warning", "Gidoiak ez ditu ainbeste Take.")
            return None
        return take_number

    def load_take_from_input(self):
        self.clear_focus()
        take_number = self.validate_take_number(self.take_number_input.text())
        if take_number is not None:
            self.current_take_number = take_number
            self.load_take(self.current_take_number)

    def validate_character_name(self, character_name):
        character_name = character_name.upper()
        upper_case_characters = self.data_handler.intervenciones['Personaje'].str.upper()
        if character_name not in upper_case_characters.values:
            QMessageBox.warning(self, "Warning", "Pertsonai hori ez dago.")
            return None
        character_dialogue = self.data_handler.intervenciones[upper_case_characters == character_name]
        if character_dialogue['Completo'].all():
            QMessageBox.warning(self, "Warning", "Pertsonai hori bukatua dago.")
            return None
        return character_name

    def load_character_from_input(self):
        self.clear_focus()
        character_name = self.validate_character_name(self.character_input.text())
        if character_name is not None:
            self.character_name = character_name
            self.search_active = True
            take_number = self.find_next_incomplete_take(1, character_name, 1)
            if take_number is not None:
                self.current_take_number = take_number
                self.load_take(self.current_take_number)
            else:
                QMessageBox.warning(self, "Warning", f"No hay más intervenciones incompletas para el personaje {character_name}")
            if not hasattr(self, 'cancel_search_button'):
                self.cancel_search_button = self.create_button("Bilaketa bukatu", self.cancel_character_search)
                self.character_search_layout.addWidget(self.cancel_search_button)

    def find_next_incomplete_take(self, start_take, character_name, direction):
        max_take = self.data_handler.takes['Numero Take'].max()
        if direction > 0:
            range_func = range
        else:
            range_func = lambda start, end: range(start, end, -1)
        for take_number in range_func(start_take, max_take + 1 if direction > 0 else 0):
            dialogue_data = self.data_handler.get_dialogue(take_number)
            if any((dialogue_data['Personaje'] == character_name) & (dialogue_data['Completo'] == 0)):
                return take_number
        return None

    def cancel_character_search(self):
        self.character_name = None
        self.search_active = False
        self.character_input.clear()
        self.load_take(self.current_take_number)
        self.character_search_layout.removeWidget(self.cancel_search_button)
        self.cancel_search_button.deleteLater()
        del self.cancel_search_button

    def load_take(self, take_number):
        try:
            take_data = self.data_handler.get_take(take_number)
            dialogue_data = self.data_handler.get_dialogue(take_number)
            self.take_label.setText(f"Take {take_number}: {take_data['IN'].values[0]} - {take_data['OUT'].values[0]}")
        except KeyError as e:
            QMessageBox.critical(self, "Error", f"Missing column in data: {str(e)}")
            return
        except IndexError as e:
            QMessageBox.critical(self, "Error", f"Index error: {str(e)}")
            return
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load take {take_number}: {str(e)}")
            return

        for i in reversed(range(self.dialogue_layout.count())):
            item = self.dialogue_layout.itemAt(i)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()

        self.dialogue_texts = {}
        self.character_labels = {}
        self.text_changed_flags = {}
        self.timecode_edits = {}
        self.complete_checkboxes = {}

        dialogue_widget = QWidget()
        dialogue_layout = QGridLayout()
        dialogue_widget.setLayout(dialogue_layout)
        for i, (index, row) in enumerate(dialogue_data.iterrows()):
            if not self.active_characters.get(row['Personaje'], True):
                continue
            try:
                character_label = self.create_character_label(row)
                self.character_labels[row['ID']] = character_label
                dialogue_layout.addWidget(character_label, i, 1)

                dialogue_text = self.create_dialogue_text(row)
                self.dialogue_texts[row['ID']] = dialogue_text
                self.text_changed_flags[row['ID']] = False
                dialogue_layout.addWidget(dialogue_text, i, 2)

                complete_check_box = self.create_complete_check_box(row)
                self.complete_checkboxes[row['ID']] = complete_check_box
                dialogue_layout.addWidget(complete_check_box, i, 3)

                self.adjust_text_edit_height(dialogue_text)

                if row['Completo'] == 1:
                    dialogue_text.setObjectName("completedDialogue")
                    dialogue_text.setStyleSheet("background-color: lightgreen;")

            except KeyError as e:
                QMessageBox.critical(self, "Error", f"Missing column in data row: {str(e)}")
                continue
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load dialogue row: {str(e)}")
                continue

        scroll_area = QScrollArea()
        scroll_area.setWidget(dialogue_widget)
        scroll_area.setWidgetResizable(True)
        self.dialogue_layout.addWidget(scroll_area)
        self.setStyleSheet(self.styleSheet())

        for dialogue_text in self.dialogue_texts.values():
            self.adjust_text_edit_height(dialogue_text)

        QTimer.singleShot(0, self.force_resize)

    def create_complete_check_box(self, row):
        complete_check_box = QCheckBox()
        complete_check_box.setChecked(bool(row['Completo']))
        complete_check_box.stateChanged.connect(lambda state, x=row['ID']: self.mark_intervention_complete(x, state == 2))
        complete_check_box.setStyle(QStyleFactory.create('Windows'))
        return complete_check_box

    def force_resize(self):
        for dialogue_text in self.dialogue_texts.values():
            self.adjust_text_edit_height(dialogue_text)

    def create_character_label(self, row):
        character_label = CharacterLabel(row['Personaje'])
        character_label.setObjectName("completedLabel" if row['Completo'] == 1 else ("characterLabelActiveSearch" if self.character_name and row['Personaje'] == self.character_name else "defaultCharacterLabel"))
        self.setStyleSheet(self.styleSheet())
        return character_label

    def create_dialogue_text(self, row):
        dialogue_text = QPlainTextEdit("" if pd.isna(row['Dialogo']) else str(row['Dialogo']))
        dialogue_text.setObjectName("dialogueText")
        dialogue_text.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        dialogue_text.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        def adjust_and_set_height():
            self.adjust_text_edit_height(dialogue_text)

        adjust_and_set_height()

        def text_changed():
            self.set_text_changed_flag(row['ID'])
            adjust_and_set_height()

        def save_on_focus_out():
            if self.text_changed_flags.get(row['ID'], False):
                self.data_handler.update_dialogue(row['ID'], dialogue_text.toPlainText())
                self.data_handler.save()
                self.text_changed_flags[row['ID']] = False

        dialogue_text.textChanged.connect(text_changed)
        dialogue_text.focusOutEvent = lambda event: save_on_focus_out() or QPlainTextEdit.focusOutEvent(dialogue_text, event)

        dialogue_text.setMouseTracking(True)

        def highlight():
            dialogue_text.setStyleSheet("background-color: lightyellow;")
        
        def remove_highlight():
            dialogue_text.setStyleSheet("")

        dialogue_text.enterEvent = lambda event: highlight() or QPlainTextEdit.enterEvent(dialogue_text, event)
        dialogue_text.leaveEvent = lambda event: remove_highlight() or QPlainTextEdit.leaveEvent(dialogue_text, event)

        return dialogue_text

    def adjust_text_edit_height(self, dialogue_text):
        document = dialogue_text.document()
        font_metrics = dialogue_text.fontMetrics()
        line_height = font_metrics.lineSpacing()
        available_width = dialogue_text.viewport().width()
        document.setTextWidth(available_width)

        total_height = 0
        block = document.begin()
        while block.isValid():
            layout = block.layout()
            if layout:
                line_count = layout.lineCount()
                total_height += line_count * line_height
            block = block.next()

        total_height += dialogue_text.contentsMargins().top() + dialogue_text.contentsMargins().bottom()
        dialogue_text.setFixedHeight(int(total_height) + 5)
        dialogue_text.updateGeometry()

    def load_adjacent_take(self, direction):
        self.clear_focus()
        next_take = None
        if self.search_active:
            next_take = self.find_next_incomplete_take(self.current_take_number + direction, self.character_name, direction)
        else:
            next_take = self.current_take_number + direction
        
        max_take = self.data_handler.takes['Numero Take'].max()
        
        if next_take is None or next_take < 1 or next_take > max_take:
            if self.search_active:
                QMessageBox.warning(self, "Warning", f"No hay más intervenciones incompletas para el personaje {self.character_name}")
            else:
                QMessageBox.warning(self, "Warning", "No hay más takes disponibles.")
            return

        self.current_take_number = next_take
        self.load_take(self.current_take_number)

    def load_previous_take(self):
        self.load_adjacent_take(-1)

    def load_next_take(self):
        self.load_adjacent_take(1)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, "Gorde", "Programa itxi aurretik gorde nahi?", QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)
        if reply == QMessageBox.Cancel:
            event.ignore()
            return
        if reply == QMessageBox.Yes:
            self.data_handler.save()
        event.accept()

    def mark_intervention_complete(self, intervention_id, state):
        self.data_handler.mark_complete(intervention_id, state)
        character_label = self.character_labels[intervention_id]
        dialogue_text = self.dialogue_texts[intervention_id]
        complete_check_box = self.complete_checkboxes[intervention_id]

        character_label.setObjectName("completedLabel" if state else "defaultCharacterLabel")
        dialogue_text.setObjectName("completedDialogue" if state else "dialogueText")
        complete_check_box.setChecked(state)

        character_label.style().unpolish(character_label)
        character_label.style().polish(character_label)
        character_label.update()

        dialogue_text.style().unpolish(dialogue_text)
        dialogue_text.style().polish(dialogue_text)
        dialogue_text.update()

        self.data_handler.save()

    def save_changes(self):
        self.data_handler.save()

    def find_character_take(self, start, end, step):
        for take_number in range(start, end, step):
            dialogue_data = self.data_handler.get_dialogue(take_number)
            if all(dialogue_data['Completo'] == 1):
                continue
            character_dialogue = dialogue_data[(dialogue_data['Personaje'] == self.character_name) & (dialogue_data['Completo'] == 0)]
            if not character_dialogue.empty:
                return take_number
        return None

    def clear_focus(self):
        if not self.dialogue_texts:
            return

        for intervention_id, text_edit in self.dialogue_texts.items():
            try:
                text_edit.clearFocus()
                if 'Hasiera' in text_edit.objectName():
                    self.data_handler.update_timecode(intervention_id, text_edit.text())
                else:
                    if self.text_changed_flags.get(intervention_id, False):
                        self.data_handler.update_dialogue(intervention_id, text_edit.toPlainText())
                        self.text_changed_flags[intervention_id] = False
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error updating intervention {intervention_id}: {str(e)}")

    def set_text_changed_flag(self, intervention_id):
        self.text_changed_flags[intervention_id] = True
        if 'Hasiera' in self.sender().objectName():
            self.data_handler.update_timecode(intervention_id, self.sender().text())
        else:
            if intervention_id in self.dialogue_texts:
                new_dialogue = self.dialogue_texts[intervention_id].toPlainText()
                self.data_handler.update_dialogue(intervention_id, new_dialogue)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        for dialogue_text in self.dialogue_texts.values():
            self.adjust_text_edit_height(dialogue_text)
