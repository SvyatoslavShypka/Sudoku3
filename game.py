from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout
from PySide6.QtGui import QPixmap, QPainter, QColor, QFont, QMouseEvent
from PySide6.QtCore import Qt, QTimer, QRect

import random

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.error_label = QLabel(self)
        self.game_display = GameWidget(self)
        self.setup()

    def quit_app(self):
        QApplication.instance().quit()

    def setup(self):
        width = 600
        height = 750

        layout = QVBoxLayout()

        pix_label = QLabel(self)
        pixmap = QPixmap("icon.png").scaled(30, 30)
        pix_label.setPixmap(pixmap)
        layout.addWidget(pix_label)

        new_game_button = QPushButton("New game", self)
        new_game_button.clicked.connect(self.start_game)
        layout.addWidget(new_game_button)

        quit_btn = QPushButton("Quit", self)
        quit_btn.clicked.connect(self.quit_app)
        layout.addWidget(quit_btn)

        self.setLayout(layout)

        self.game_display.setVisible(False)  # Initially hide the game display
        layout.addWidget(self.game_display)

        layout.addWidget(self.error_label)

        self.setFixedSize(width, height)
        self.setWindowTitle("Sudoku Interface")
        self.show()

    def start_game(self):
        self.error_label.clear()  # Clear any previous error messages
        self.game_display.start_game()
        self.game_display.setVisible(True)  # Show the game display
        self.game_display.setFocus()  # Give focus to the GameWidget


class GameWidget(QWidget):
    square = 3
    dimension = square * square

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(500, 500)
        self.grid = self.create_grid()
        self.key_count = 1
        self.x = self.y = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_game)
        self.setFocusPolicy(Qt.StrongFocus)  # Set focus policy to accept key events
        self.parent = parent

    def create_grid(self):
        grid = [[0 for _ in range(self.dimension)] for _ in range(self.dimension)]
        return grid

    def start_game(self):
        self.grid = self.create_grid()
        self.x = self.y = 0
        self.update_game()
        self.timer.start(1000 // 60)  # 60 FPS
        self.setFocus()  # Give focus to the GameWidget after starting the game

    def update_game(self):
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        self.draw_grids(painter)
        self.highlight_cell(painter)

    def draw_grids(self, painter):
        cell_length = 500 // self.dimension
        font = QFont("Arial", cell_length // 2)
        painter.setFont(font)
        for i in range(self.dimension):
            for j in range(self.dimension):
                if self.grid[i][j] != 0:
                    rect = QRect(i * cell_length, j * cell_length, cell_length, cell_length)
                    painter.fillRect(rect, QColor(0, 153, 153))
                    painter.drawText(rect, Qt.AlignCenter, str(self.grid[i][j]))
        for i in range(self.dimension + 1):
            thick = 8 if i % 3 == 0 else 2
            painter.setPen(QColor(0, 0, 0))
            painter.drawLine(0, i * cell_length, 500, i * cell_length)
            painter.drawLine(i * cell_length, 0, i * cell_length, 500)

    def highlight_cell(self, painter):
        cell_length = 500 // 9
        painter.setPen(QColor(255, 0, 255))
        for i in range(2):
            painter.drawLine(self.x * cell_length - 3, (self.y + i) * cell_length,
                             self.x * cell_length + cell_length + 3, (self.y + i) * cell_length)
            painter.drawLine((self.x + i) * cell_length, self.y * cell_length,
                             (self.x + i) * cell_length, self.y * cell_length + cell_length)

    def keyPressEvent(self, event):
        print("self.key_count", self.key_count)
        self.key_count += 1
        if event.key() == Qt.Key_Left:
            self.x = max(0, self.x - 1)
        elif event.key() == Qt.Key_Right:
            self.x = min(8, self.x + 1)
        elif event.key() == Qt.Key_Up:
            self.y = max(0, self.y - 1)
        elif event.key() == Qt.Key_Down:
            self.y = min(8, self.y + 1)
        elif Qt.Key_1 <= event.key() <= Qt.Key_9:
            num = event.key() - Qt.Key_0
            if self.is_allowed_here(self.grid, self.x, self.y, num):
                self.grid[self.x][self.y] = num
                self.parent.error_label.clear()  # Clear the error message if the move is valid
            else:
                self.parent.error_label.setText("Invalid move")
        elif event.key() == Qt.Key_Return:
            if self.solve(self.grid, 0, 0):
                self.parent.error_label.setText("Solved!")
            else:
                self.parent.error_label.setText("No solution")
        self.update_game()

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.x = int(event.position().x() // (500 // 9))
            self.y = int(event.position().y() // (500 // 9))
            self.update_game()

    def is_allowed_here(self, m, i, j, num):
        dimension = 9
        square = 3
        for it in range(dimension):
            if m[i][it] == num or m[it][j] == num:
                return False
        it, jt = i // square, j // square
        for i in range(it * square, it * square + square):
            for j in range(jt * square, jt * square + square):
                if m[i][j] == num:
                    return False
        return True

    def solve(self, grid, i, j):
        dimension = 9
        while grid[i][j] != 0:
            if i < dimension - 1:
                i += 1
            elif i == dimension - 1 and j < dimension - 1:
                i = 0
                j += 1
            elif i == dimension - 1 and j == dimension - 1:
                return True
        for it in range(1, 10):
            if self.is_allowed_here(grid, i, j, it):
                grid[i][j] = it
                self.x, self.y = i, j
                self.update_game()
                if self.solve(grid, i, j):
                    return True
                else:
                    grid[i][j] = 0
                self.update_game()
        return False


if __name__ == '__main__':
    app = QApplication([])

    login_window = LoginWindow()

    app.exec()
