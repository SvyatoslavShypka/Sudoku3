from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from PySide6.QtGui import QPainter, QFont
from PySide6.QtCore import Qt
import random

class SudokuGame(QWidget):
    def __init__(self):
        super().__init__()
        self.square = 3
        self.dimension = self.square * self.square
        self.cell_length = 50
        self.grid = [[0 for _ in range(self.dimension)] for _ in range(self.dimension)]
        self.setup_ui()
        self.new_game()

    def setup_ui(self):
        self.setWindowTitle("Sudoku")
        self.setGeometry(100, 100, self.dimension * self.cell_length, self.dimension * self.cell_length)
        new_game_button = QPushButton("New Game")
        new_game_button.clicked.connect(self.new_game)
        solve_button = QPushButton("Solve")
        solve_button.clicked.connect(self.solve)
        layout = QVBoxLayout()
        layout.addWidget(new_game_button)
        layout.addWidget(solve_button)
        self.setLayout(layout)

    def new_game(self):
        self.grid = self.randomize_grid(level=0)
        self.update()

    def randomize_grid(self, level):
        grid = [[0 for _ in range(self.dimension)] for _ in range(self.dimension)]
        # grid = [[0] * self.dimension for _ in range(self.dimension)]
        x = y = 0
        num = random.randint(1, self.dimension)
        for i in range(self.dimension):
            while not self.is_allowed_here(grid, x, y, num):
                num = random.randint(1, self.dimension)
            grid[x][y] = num
            x += 1
        self.solve()
        grid = self.leverage_grid(level)
        return grid

    def leverage_grid(self, level):
        # Adjust the grid by removing some numbers based on the level of difficulty
        cells_to_remove = 20 + level * 5
        for _ in range(cells_to_remove):
            x = random.randint(0, self.dimension - 1)
            y = random.randint(0, self.dimension - 1)
            while self.grid[x][y] == 0:
                x = random.randint(0, self.dimension - 1)
                y = random.randint(0, self.dimension - 1)
            self.grid[x][y] = 0
        return self.grid


    def solve(self):
        stack = [(self.grid, 0, 0)]
        while stack:
            grid, i, j = stack.pop()
            if i == self.dimension:
                self.grid = grid
                self.update()
                return
            next_i = i + 1 if j == self.dimension - 1 else i
            next_j = (j + 1) % self.dimension
            if grid[i][j] != 0:
                stack.append((grid, next_i, next_j))
                continue
            for num in range(1, self.dimension + 1):
                if self.is_allowed_here(grid, i, j, num):
                    new_grid = [row[:] for row in grid]
                    new_grid[i][j] = num
                    stack.append((new_grid, next_i, next_j))
        print("No solution found")

    def is_allowed_here(self, m, i, j, num):
        for it in range(self.dimension):
            if m[i][it] == num or m[it][j] == num:
                return False
        it, jt = i // self.square, j // self.square
        for i in range(it * self.square, it * self.square + self.square):
            for j in range(jt * self.square, jt * self.square + self.square):
                if m[i][j] == num:
                    return False
        return True

    def paintEvent(self, event):
        painter = QPainter(self)
        font = QFont("Arial", 20)
        painter.setFont(font)
        for i in range(self.dimension):
            for j in range(self.dimension):
                value = self.grid[i][j]
                if value != 0:
                    painter.drawText(j * self.cell_length + self.cell_length / 2,
                                     i * self.cell_length + self.cell_length / 2,
                                     str(value))

if __name__ == "__main__":
    app = QApplication([])
    game = SudokuGame()
    game.show()
    app.exec()
