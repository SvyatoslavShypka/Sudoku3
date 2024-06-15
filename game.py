from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from interface import LoginWindow


def main():
    app = QApplication([])
    app_icon = QIcon("../icon.ico")
    app.setWindowIcon(app_icon)

    login_window = LoginWindow()

    app.exec()


if __name__ == '__main__':
    main()