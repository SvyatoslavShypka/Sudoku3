from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QLabel
from PySide6.QtGui import QCloseEvent, QPixmap
import multiprocessing
import sudoku_game

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setup()



    def setup(self):
        width = 1000
        height = 1000

        pix_label = QLabel(self)
        pixmap = QPixmap("icon.png").scaled(50, 50)
        pix_label.setPixmap(pixmap)
        pix_label.move(100, 50)

        new_game_button = QPushButton("New game", self)
        new_game_button.move(width - 80, height / 4)
        new_game_button.clicked.connect(self.new_game)

        quit_btn = QPushButton("Quit", self)
        quit_btn.move(width - 80, height - 30)
        quit_btn.clicked.connect(QApplication.instance().quit)

        self.setFixedSize(width, height)
        self.setWindowTitle("Sudoku Interface")
        self.show()

    def new_game(self):
        # Create a new process to run the start_game function
        game_process = multiprocessing.Process(target=sudoku_game.start_game)
        game_process.start()

    def closeEvent(self, event: QCloseEvent):
        should_close = QMessageBox.question(self, "Close App", "Do you want to close App?",
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if should_close == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()

if __name__ == '__main__':
    multiprocessing.set_start_method('spawn')
    app = QApplication([])

    login_window = LoginWindow()

    app.exec()
