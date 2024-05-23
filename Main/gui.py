from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QLineEdit, 
    QTextEdit, QFileDialog, QGridLayout, QCheckBox, QMessageBox, QCompleter, QTableWidget, QTableWidgetItem, 
    QProgressBar, QPlainTextEdit, QScrollArea, QStyleFactory, QSizePolicy, QShortcut
)
from PyQt5.QtCore import Qt, pyqtSignal, QEvent, QTimer
from PyQt5.QtGui import QValidator, QResizeEvent, QKeySequence
from datahandler import DataHandler
import pandas as pd
import sys
import os

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

class MainWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.main_layout = QVBoxLayout(self)

        self.open_button = QPushButton("Abrir nuevo Excel")
        self.open_button.setObjectName("openButton")
        self.open_button.clicked.connect(self.open_new_excel)

        self.go_button = QPushButton("Ir al Guion")
        self.go_button.setObjectName("goButton")
        self.go_button.clicked.connect(self.go_to_gidoia)

        self.main_layout.addWidget(self.open_button)
        self.main_layout.addWidget(self.go_button)

        self.table = QTableWidget()
        self.table.setObjectName("mainTable")
        self.table.horizontalHeader().setStretchLastSection(True)
        self.main_layout.addWidget(self.table)
        
        self.setLayout(self.main_layout)

    def open_new_excel(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Excel File", "", "Excel Files (*.xls *.xlsx)")
        if file_path:
            self.window().data_handler = DataHandler(file_path)
            self.update_table()

    def go_to_gidoia(self):
        if not self.window().data_handler:
            QMessageBox.warning(self, "Error", "No has seleccionado el Excel")
            return
        self.window().gidoia_widget = GidoiaWidget(self.window().data_handler, self.window())
        self.window().setCentralWidget(self.window().gidoia_widget)

    def update_table(self):
        data = self.window().data_handler.get_incomplete_characters()
        self.table.setRowCount(len(data))
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Personaje", "Takes Restantes", "Porcentaje Completado"])
        for i, row in data.iterrows():
            self.insert_table_row(i, row)

    def insert_table_row(self, i, row):
        self.table.insertRow(i)
        self.table.setItem(i, 0, QTableWidgetItem(row['Personaje']))
        self.table.setItem(i, 1, QTableWidgetItem(str(row['Takes Restantes'])))
        progress = QProgressBar()
        progress.setValue(int(row['Porcentaje Completado']))
        self.table.setCellWidget(i, 2, progress)

class TimecodeValidator(QValidator):
    def validate(self, string, pos):
        if not string:
            return QValidator.Acceptable, string, pos
        string = string.replace(':', '')
        if not string.isdigit() or len(string) > 8:
            return QValidator.Invalid, string, pos
        return QValidator.Acceptable, string, pos

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

class GidoiaWidget(QWidget):
    def __init__(self, data_handler, parent=None):
        super().__init__(parent)
        self.data_handler = data_handler
        self.current_take_number = 1
        self.character_name = None
        self.search_active = False
        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)
        self.create_search_layouts()
        self.create_navigation_buttons()
        self.create_take_label()
        self.dialogue_layout = QGridLayout()
        self.main_layout.addLayout(self.dialogue_layout)
        '''self.create_save_button()'''
        self.create_back_button()
        self.character_completer = QCompleter(self.get_character_names())
        self.character_completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.character_input.setCompleter(self.character_completer)
        self.load_take(self.current_take_number)
        
        self.setup_shortcuts()  # Agregar esta línea para inicializar los shortcuts

    def setup_shortcuts(self):
        QShortcut(QKeySequence("Ctrl+N"), self, self.load_next_take)
        QShortcut(QKeySequence("Ctrl+P"), self, self.load_previous_take)
        QShortcut(QKeySequence("Ctrl+S"), self, self.save_changes)

    def create_search_layouts(self):
        self.take_search_layout = QHBoxLayout()
        self.take_number_input = QLineEdit()
        self.take_number_input.returnPressed.connect(self.load_take_from_input)
        self.take_search_button = self.create_button("Buscar Take", self.load_take_from_input)
        self.take_search_layout.addWidget(self.take_number_input)
        self.take_search_layout.addWidget(self.take_search_button)

        self.character_search_layout = QHBoxLayout()
        self.character_input = QLineEdit()
        self.character_input.returnPressed.connect(self.load_character_from_input)
        self.character_search_button = self.create_button("Buscar Personaje", self.load_character_from_input)
        self.character_search_layout.addWidget(self.character_input)
        self.character_search_layout.addWidget(self.character_search_button)

        self.search_layout = QHBoxLayout()
        self.search_layout.addLayout(self.take_search_layout)
        self.search_layout.addLayout(self.character_search_layout)
        self.main_layout.addLayout(self.search_layout)

    def create_navigation_buttons(self):
        self.navigation_layout = QHBoxLayout()
        self.prev_button = self.create_button("Take anterior", self.load_previous_take)
        self.next_button = self.create_button("Siguiente Take", self.load_next_take)
        self.navigation_layout.addWidget(self.prev_button)
        self.navigation_layout.addWidget(self.next_button)
        self.main_layout.addLayout(self.navigation_layout)

    def create_take_label(self):
        self.take_label = QLabel()
        self.take_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.take_label)

    def create_save_button(self):
        self.save_button = self.create_button("Guardar", self.save_changes)
        self.main_layout.addWidget(self.save_button)

    def create_back_button(self):
        self.back_button = self.create_button("Pagina principal", self.go_back)
        self.main_layout.addWidget(self.back_button)

    def create_button(self, text, function):
        button = QPushButton(text)
        button.clicked.connect(function)
        return button

    def get_character_names(self):
        return self.data_handler.get_character_names()

    def go_back(self):
        reply = QMessageBox.question(self, "Guardar", "Quieres guardar los cambios?", QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)
        if reply == QMessageBox.Cancel:
            return
        if reply == QMessageBox.Yes:
            self.data_handler.save()
        self.window().main_widget = MainWidget(self.window())
        self.window().setCentralWidget(self.window().main_widget)


    def validate_take_number(self, take_number):
        try:
            take_number = int(take_number)
        except ValueError:
            QMessageBox.warning(self, "Alerta", "Numero de Take no valido.")
            return None
        if not (1 <= take_number <= len(self.data_handler.takes)):
            QMessageBox.warning(self, "Alerta", "No hay mas Takes.")
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
            QMessageBox.warning(self, "Alerta", "No existe ese personaje.")
            return None
        character_dialogue = self.data_handler.intervenciones[upper_case_characters == character_name]
        if character_dialogue['Completo'].all():
            QMessageBox.warning(self, "Alerta", "El personaje esta completo.")
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
                QMessageBox.warning(self, "Alerta", f"No hay más intervenciones incompletas para el personaje {character_name}")
            if not hasattr(self, 'cancel_search_button'):
                self.cancel_search_button = self.create_button("Terminar busqueda", self.cancel_character_search)
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
            self.take_label.setText(f"<b>Take {take_number}</b>: {take_data['IN'].values[0]} - {take_data['OUT'].values[0]}")
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
            try:
                '''timecode_edit = self.create_timecode_edit(row)
                self.timecode_edits[str(row['ID']) + 'Hasiera'] = timecode_edit
                dialogue_layout.addWidget(timecode_edit, i, 0)'''

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

                # Ajustar estilo del diálogo si el checkbox está marcado
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

    def create_timecode_edit(self, row):
        initial_text = '00:00:00:00' if pd.isna(row.get('Hasiera', None)) else pd.to_datetime(str(row['Hasiera']), format='%H:%M:%S:%f').strftime('%H:%M:%S:%f')[:-4]
        timecode_edit = TimecodeLineEdit(self.data_handler, row['ID'], initial_text)
        timecode_edit.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        timecode_edit.setFixedWidth(timecode_edit.fontMetrics().boundingRect('00:00:00:00').width() + 100)
        timecode_edit.textChanged.connect(self.handle_timecode_input)
        timecode_edit.setObjectName(str(row['ID']))
        return timecode_edit

    def create_character_label(self, row):
        character_label = CharacterLabel(row['Personaje'])
        character_label.setObjectName("completedLabel" if row['Completo'] == 1 else ("characterLabelActiveSearch" if self.character_name and row['Personaje'] == self.character_name else "defaultCharacterLabel"))
        self.setStyleSheet(self.styleSheet())
        return character_label

    def create_dialogue_text(self, row):
        dialogue_text = QPlainTextEdit("" if pd.isna(row['Dialogo']) else str(row['Dialogo']))
        dialogue_text.setObjectName("dialogueText")
        dialogue_text.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # No permitir scroll
        dialogue_text.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # No permitir scroll horizontal

        def adjust_and_set_height():
            self.adjust_text_edit_height(dialogue_text)

        adjust_and_set_height()  # Ajustar tamaño del cuadro de texto al contenido

        def text_changed():
            self.set_text_changed_flag(row['ID'])
            adjust_and_set_height()  # Ajustar el tamaño del cuadro de texto al cambiar el contenido

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

    def create_complete_check_box(self, row):
        complete_check_box = QCheckBox()
        complete_check_box.setChecked(bool(row['Completo']))
        complete_check_box.stateChanged.connect(lambda state, x=row['ID']: self.mark_intervention_complete(x, state == 2))
        complete_check_box.setStyle(QStyleFactory.create('Windows'))
        return complete_check_box

    def handle_timecode_input(self):
        intervention_id = self.sender().objectName().replace('Hasiera', '')
        timecode_edit = self.timecode_edits[intervention_id + 'Hasiera']
        text = ''.join(c for c in timecode_edit.text() if c.isdigit()).ljust(8, '0')
        formatted_text = f"{text[:2]}:{text[2:4]}:{text[4:6]}:{text[6:]}"
        timecode_edit.setText(formatted_text)
        timecode_edit.textChanged.connect(self.handle_timecode_input)

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
                QMessageBox.warning(self, "Alerta", f"No hay más intervenciones incompletas para el personaje {self.character_name}")
            else:
                QMessageBox.warning(self, "Alerta", "No hay más takes disponibles.")
            return

        self.current_take_number = next_take
        self.load_take(self.current_take_number)

    def load_previous_take(self):
        self.load_adjacent_take(-1)

    def load_next_take(self):
        self.load_adjacent_take(1)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, "Guardar", "Guardar antes de cerrar?", QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)
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

        # Guardar automáticamente cuando se marque el checkbox
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

class Application(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gidoiapp")
        self.setGeometry(200, 200, 800, 600)
        self.data_handler = None
        self.main_widget = MainWidget(self)
        self.gidoia_widget = None
        self.setCentralWidget(self.main_widget)
        self.showMaximized()

    def handle_close_event(self):
        if self.data_handler:
            reply = QMessageBox.question(self, "Guardar", "Quieres guardar antes de cerrar?", QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)
            if reply == QMessageBox.Yes:
                self.data_handler.save()
                return True
            elif reply == QMessageBox.No:
                return True
        return False

    def closeEvent(self, event):
        if not self.handle_close_event():
            event.ignore()

def load_stylesheet(app, filename):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    css_path = os.path.join(script_dir, filename)
    with open(css_path, "r") as f:
        app.setStyleSheet(f.read())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    load_stylesheet(app, "main.css")
    gui = Application()
    gui.showMaximized()
    sys.exit(app.exec_())
