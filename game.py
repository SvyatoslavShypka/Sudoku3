import time

from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout
from PySide6.QtGui import QPixmap, QPainter, QColor, QFont, QMouseEvent, QIcon, QPen
from PySide6.QtCore import Qt, QTimer, QRect

import random

class LoginWindow(QWidget):
    width = 600
    height = 750

    def __init__(self):
        super().__init__()
        self.error_label = QLabel(self)
        self.game_display = GameWidget(self)
        self.setup()

    def quit_app(self):
        QApplication.instance().quit()

    def setup(self):

        layout = QVBoxLayout()

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

        self.setFixedSize(self.width, self.height)
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
    side = LoginWindow.width - 60
    cell_length = (side) // dimension
    thick_line = 8
    thin_line = 2

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(self.side, self.side)
        self.grid = self.create_grid()
        self.key_count = 1
        self.x = self.y = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_game)
        self.setFocusPolicy(Qt.StrongFocus)  # Set focus policy to accept key events
        self.parent = parent

    def create_grid(self, level=0):
        # create grid with zeros
        grid = [[0 for _ in range(self.dimension)] for _ in range(self.dimension)]
        x = y = 0
        num = random.randint(1, self.dimension)
        for i in range(self.dimension):
            while not self.is_allowed_here(grid, x, y, num):
                num = random.randint(1, self.dimension)
            grid[x][y] = num
            x += 1
        self.solve(grid, 0, 0)
        grid = self.leverage_grid(grid, level)
        return grid

    def leverage_grid(self, grid, level):
        # Adjust the grid by removing some numbers based on the level of difficulty
        cells_to_remove = 20 + level * 5
        for _ in range(cells_to_remove):
            x = random.randint(0, self.dimension - 1)
            y = random.randint(0, self.dimension - 1)
            while grid[x][y] == 0:
                x = random.randint(0, self.dimension - 1)
                y = random.randint(0, self.dimension - 1)
            grid[x][y] = 0
        return grid

    def is_allowed_here(self, m, i, j, num):
        for it in range(self.dimension):
            if m[i][it] == num or m[it][j] == num:
                return False
        it, jt = i // self.square, j // self.squar
        for i in range(it * self.squar, it * self.squar + self.squar):
            for j in range(jt * self.squar, jt * self.squar + self.squar):
                if m[i][j] == num:
                    return False
        return True

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
        font = QFont("Arial", self.cell_length // 2)
        painter.setFont(font)
        for i in range(self.dimension):
            for j in range(self.dimension):
                if self.grid[i][j] != 0:
                    rect = QRect(i * self.cell_length, j * self.cell_length, self.cell_length, self.cell_length)
                    painter.fillRect(rect, QColor(0, 153, 153))
                    painter.drawText(rect, Qt.AlignCenter, str(self.grid[i][j]))
        for i in range(self.dimension + 1):
            thick = self.thick_line if i % self.square == 0 else self.thin_line
            painter.setPen(QPen(QColor(0, 0, 0), thick))
            # horisontal lines
            y_pos = i * self.cell_length
            painter.drawLine(0, y_pos, self.side, y_pos)
            # vertical lines
            x_pos = i * self.cell_length
            painter.drawLine(x_pos, 0, x_pos, self.side)

    def highlight_cell(self, painter):
        painter.setPen(QPen(QColor(255, 0, 255), self.thick_line))
        for i in range(2):
            # up_horizontal_line
            painter.drawLine(self.x * self.cell_length, (self.y + i) * self.cell_length,
                             self.x * self.cell_length + self.cell_length, (self.y + i) * self.cell_length)
            painter.drawLine((self.x + i) * self.cell_length, self.y * self.cell_length,
                             (self.x + i) * self.cell_length, self.y * self.cell_length + self.cell_length)

    def keyPressEvent(self, event):
        # print("self.key_count", self.key_count)
        # self.key_count += 1
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
            self.x = int(event.position().x() // (self.side // self.dimension))
            self.y = int(event.position().y() // (self.side // self.dimension))
            self.update_game()

    def is_allowed_here(self, m, i, j, num):
        square = 3
        for it in range(self.dimension):
            if m[i][it] == num or m[it][j] == num:
                return False
        it, jt = i // square, j // square
        for i in range(it * square, it * square + square):
            for j in range(jt * square, jt * square + square):
                if m[i][j] == num:
                    return False
        return True

    def solve(self, grid, i, j):
        while grid[i][j] != 0:
            if i < self.dimension - 1:
                i += 1
            elif i == self.dimension - 1 and j < self.dimension - 1:
                i = 0
                j += 1
            elif i == self.dimension - 1 and j == self.dimension - 1:
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
    # Ustawianie ikonki aplikacji
    app_icon = QIcon("icon.png")
    app.setWindowIcon(app_icon)

    login_window = LoginWindow()

    app.exec()
