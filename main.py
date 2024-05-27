import sys
from PyQt5.QtWidgets import QApplication
from gui.main_window import Application
from gui.utils import load_stylesheet

if __name__ == "__main__":
    app = QApplication(sys.argv)
    load_stylesheet(app, "resources/main.css")
    gui = Application()
    gui.showMaximized()
    sys.exit(app.exec_())
