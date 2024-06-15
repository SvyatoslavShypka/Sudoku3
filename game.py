from PySide6.QtWidgets import QApplication
import threading
from PySide6.QtGui import QIcon
from interface import LoginWindow


class GameSolverThread(threading.Thread):
    def __init__(self, game_widget):
        super().__init__()
        self.game_widget = game_widget

    def run(self):
        self.game_widget.solve_with_delay()


if __name__ == '__main__':
    app = QApplication([])
    app_icon = QIcon("icon.ico")
    app.setWindowIcon(app_icon)

    login_window = LoginWindow()

    app.exec()
