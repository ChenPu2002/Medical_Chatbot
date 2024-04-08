import sys
import re
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QComboBox, QLineEdit, QPushButton, QTextEdit, QSpacerItem, QSizePolicy, QDesktopWidget)
from PyQt5.QtCore import Qt, QTimer, QDateTime, QSize
from PyQt5.QtGui import QIcon, QFont, QPixmap
from input_process import InputProcess

class GUI(QWidget):

    def __init__(self):
        super().__init__()
        self.timer = QTimer()
        self.words = []
        self.word_index = 0
        self.initUI()

    def initUI(self):
        # self.setGeometry(100, 100, 600, 400)
        self.setWindowTitle('ChatDoctor - Your Personal Health Assistant')
        self.resize(800, 600)  # Set the window size to 800x600
        self.centerWindow()     # Center the window on the screen

        # Main layout
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Model selection
        model_layout = QHBoxLayout()
        model_label = QLabel('Model:')

        # Add a welcome message above the input field
        welcome_label = QLabel("Hello, welcome to the chatbot! Please select a model and type your question below.")
        welcome_label.setAlignment(Qt.AlignCenter)

        self.model_select = QComboBox()
        self.model_select.addItems(['Traditional Model', 'Advanced Model'])
        model_layout.addWidget(model_label)
        model_layout.addWidget(self.model_select)

        # Add horizontal spacer to center the model selection
        model_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # # Placeholder for icon (assuming QLabel is used for the icon)
        # icon = QIcon('logo1.png')
        # pixmap = icon.pixmap(100, 200)

        # self.label = QLabel()
        # self.label.setPixmap(pixmap)
        self.label = QLabel()
        self.label.setText("ChatDoctor")
        self.label.setFont(QFont("Verdana", 40))  # 设置字体和字号

        # Input field
        self.input_field = QLineEdit()
        font = self.input_field.font()
        font.setFamily('Arial')
        self.input_field.setFont(font)
        self.input_field.setStyleSheet("QLineEdit { border: 1px solid gray; border-radius: 4px; padding: 6px; }")
        self.input_field.setPlaceholderText('Type your question here')
        # checked
        # Click button
        self.click_button = QPushButton('Click or press Enter to submit')
        self.click_button.clicked.connect(self.processInput)
        # treating return key as click
        self.input_field.returnPressed.connect(self.click_button.click)

        # clear the input field after processing or change model_select
        # self.click_button.clicked.connect(self.input_field.clear)
        self.model_select.currentIndexChanged.connect(self.input_field.clear)

        self.clear_button = QPushButton('Clear input')
        self.clear_button.clicked.connect(self.input_field.clear)

        # Output area
        self.output_area = QTextEdit()
        self.output_area.setPlaceholderText('ChatDoctor will respond here')
        font = self.output_area.font()
        font.setFamily('Arial')
        self.output_area.setFont(font)
        self.output_area.setStyleSheet("QTextEdit { border: 1px solid gray; border-radius: 4px; padding: 6px; }")
        self.output_area.setReadOnly(True)
        
        self.model_select.currentIndexChanged.connect(self.output_area.clear)
        # Time and date display
        self.time_label = QLabel()
        self.time_label.setAlignment(Qt.AlignRight)
        self.updateTime()  # Set the initial time and date

        # Timer to update the time and date every second
        self.time_timer = QTimer(self)
        self.time_timer.timeout.connect(self.updateTime)
        self.time_timer.start(1000)  # Update every second

        # Layout for the time and date in the top right corner
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.time_label)
        main_layout.addLayout(top_layout)
        # checked
        # Adding widgets to the main layout
        main_layout.addLayout(model_layout)
        # main_layout.addWidget(self.icon_placeholder, 0, Qt.AlignCenter)  # Center the icon
        main_layout.addWidget(self.label, 0, Qt.AlignCenter)  # Center the icon
        main_layout.addWidget(self.input_field)
        main_layout.addWidget(self.click_button)
        main_layout.addWidget(self.clear_button)
        main_layout.addWidget(self.output_area)

        # Set the rounded style for the QWidget
        self.setStyleSheet("""
            QWidget {
                border-radius: 10px;
                background-color: #f0f0f0;
                font-size: 16px;
            }
            QPushButton {
                border-radius: 5px;
                background-color: #0078d7;
                color: white;
                padding: 5px;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #005ea1;
            }
            QLineEdit, QTextEdit, QLabel {
                border-radius: 5px;
                padding: 5px;
                color: black;  /* Set the text color to black */
            }
            QComboBox {
                border-radius: 5px;
                padding: 5px;
                color: black;  /* Set the text color to black */
                background-color: white;
            }
            QComboBox::drop-down {
                border-radius: 5px;
            }
            QComboBox::down-arrow {
                image: url(''); /* You can set an image path for the arrow */
            }
        """)

        # Set window icon if needed
        # self.setWindowIcon(QIcon('icon.png'))
        # Set up timer for word-by-word display
        self.timer.timeout.connect(self.displayNextWord)
    
    def centerWindow(self):
        # Get the screen resolution from the app, and calculate the center position
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def updateTime(self):
        current_time = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
        self.time_label.setText(current_time)

    def processInput(self):
        # Here you would normally send the input for processing and receive the output
        # For demonstration purposes, we just echo the input in the output area word by word
        # input_text = self.input_field.text()
        # output_text = ' '.join(input_text.split())  # Split and rejoin to echo word by word
        # self.output_area.setText(output_text)
        self.output_area.clear()
        input_text = self.input_field.text()
        output_text = InputProcess(input_text, self.model_select.currentText()).process()
        # print(output_text)
        self.words = output_text.split()
        #self.words = self.split_text(input_text)
        self.word_index = 0

        if self.words:
            self.timer.start(200)  # start the timer to add words every 500ms
    
    # def split_text(self, text):
    #     # pattern is only punctuation
    #     pattern = r"(\w+|[^\w\s])"
    #     tokens = re.findall(pattern, text)
    #     print(tokens)
    #     return tokens

    def displayNextWord(self):
        if self.word_index < len(self.words):
            current_text = self.output_area.toPlainText()
            next_word = self.words[self.word_index]
            self.output_area.setText(current_text + next_word + ' ')
            self.word_index += 1
        else:
            self.timer.stop()  # stop the timer if all words are displayed

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     app.setStyle('Fusion')  # Set the style to 'Fusion' for a modern look
#     gui = RoundedGUI()
#     gui.show()
#     sys.exit(app.exec_())
if __name__ == '__main__':
    raise ValueError("This file is not meant to be run directly. Run main.py instead.")