import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QFontDatabase, QFont
from PyQt5.QtCore import QTimer

class TimerWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()

        # Load and set the digital font
        fontId = QFontDatabase.addApplicationFont(r'C:\Users\mosta\Downloads\Tarhato-Font-digital-7\digital-7.ttf')
        fontName = QFontDatabase.applicationFontFamilies(fontId)[0]
        digitalFont = QFont(fontName, 48)

        self.timerDisplay = QLabel('00:00:00')
        self.timerDisplay.setFont(digitalFont)
        self.layout.addWidget(self.timerDisplay)

        self.startButton = QPushButton('Start')
        self.layout.addWidget(self.startButton)
        self.startButton.clicked.connect(self.startTimer)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateDisplay)
        self.elapsedTime = 0

        self.setLayout(self.layout)

    def startTimer(self):
        self.timer.start(1000)

    def updateDisplay(self):
        self.elapsedTime += 1
        # Convert elapsedTime to hours, minutes, seconds
        hours, remainder = divmod(self.elapsedTime, 3600)
        minutes, seconds = divmod(remainder, 60)
        # Update the display
        self.timerDisplay.setText(f'{hours:02d}:{minutes:02d}:{seconds:02d}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TimerWidget()
    window.show()
    sys.exit(app.exec_())
