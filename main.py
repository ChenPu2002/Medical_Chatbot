print("Loading libraries...")
from gui import ChatWindow as GUI
from PyQt5.QtWidgets import QApplication
import sys
import time

if __name__ == '__main__':
    start_time = time.time()

    # code for running the GUI
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Set the style to 'Fusion' for a modern look
    gui = GUI()
    gui.show()
    print(f"GUI loaded in {time.time() - start_time:.2f} seconds")

    # click system exit to close the GUI
    sys.exit(app.exec_())