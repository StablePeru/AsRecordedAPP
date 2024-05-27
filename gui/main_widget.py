from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFileDialog, QMessageBox, QTableWidget, QTableWidgetItem, QProgressBar
from datahandler.data_handler import DataHandler

class MainWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_layout = QVBoxLayout(self)

        self.open_button = QPushButton("Abrir nuevo Excel")
        self.open_button.setObjectName("openButton")
        self.open_button.clicked.connect(self.open_new_excel)

        self.go_button = QPushButton("Ir a Gidoia")
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
            QMessageBox.warning(self, "Error", "Ez duzu Excel-a aukeratu")
            return
        self.window().set_gidoia_widget()

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
