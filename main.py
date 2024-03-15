from gui import GUI
from PyQt5.QtWidgets import QApplication
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Set the style to 'Fusion' for a modern look
    gui = GUI()
    gui.show()
    sys.exit(app.exec_())