# main.py
from gui.main_window import Application
from PyQt5.QtWidgets import QApplication
import sys
from gui.utils import load_stylesheet

def main():
    app = QApplication(sys.argv)
    load_stylesheet(app, "main.css")  # Cargar CSS
    window = Application()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
