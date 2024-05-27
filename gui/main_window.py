from PyQt5.QtWidgets import QMainWindow, QMessageBox
from .main_widget import MainWidget
from .gidoia_widget import GidoiaWidget

class Application(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gidoiapp")
        self.setGeometry(200, 200, 800, 600)
        self.data_handler = None
        self.main_widget = MainWidget(self)
        self.setCentralWidget(self.main_widget)
        self.showMaximized()

    def set_gidoia_widget(self):
        self.gidoia_widget = GidoiaWidget(self.data_handler, self)
        self.setCentralWidget(self.gidoia_widget)

    def set_main_widget(self):
        self.main_widget = MainWidget(self)
        self.setCentralWidget(self.main_widget)

    def handle_close_event(self):
        if self.data_handler:
            reply = QMessageBox.question(self, "Gorde", "Programa itxi aurretik gorde nahi?", QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)
            if reply == QMessageBox.Yes:
                self.data_handler.save()
                return True
            elif reply == QMessageBox.No:
                return True
        return False

    def closeEvent(self, event):
        if not self.handle_close_event():
            event.ignore()
