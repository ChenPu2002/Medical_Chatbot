print("The first loading may be longer, for around 1 minute, but the following loading will be faster for less than 10 seconds.")
from gui import ChatWindow as GUI
from PyQt5.QtWidgets import QApplication
import sys

if __name__ == '__main__':

    # code for running the GUI
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Set the style to 'Fusion' for a modern look
    gui = GUI()
    gui.show()

    # click system exit to close the GUI
    sys.exit(app.exec_())