import tkinter as tk
import time


class SudokuSolver:
    def __init__(self, board, canvas, cell_size=50):
        self.board = board
        self.canvas = canvas
        self.cell_size = cell_size
        self.N = 9

    def is_valid(self, row, col, num):
        for i in range(self.N):
            if self.board[row][i] == num or self.board[i][col] == num:
                return False

        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if self.board[i][j] == num:
                    return False
        return True

    def solve_with_delay(self):
        def solve():
            for i in range(self.N):
                for j in range(self.N):
                    if self.board[i][j] == 0:
                        for num in range(1, 10):
                            if self.is_valid(i, j, num):
                                self.board[i][j] = num
                                self.update_board(i, j, num)
                                if solve():
                                    return True
                                self.board[i][j] = 0  # Backtrack
                                self.update_board(i, j, 0)
                        return False
            return True

        if solve():
            print("Sudoku solved successfully!")
        else:
            print("No solution exists.")

    def update_board(self, row, col, num):
        self.canvas.create_text(
            col * self.cell_size + self.cell_size // 2,
            row * self.cell_size + self.cell_size // 2,
            text=str(num) if num != 0 else '',
            font=("Arial", 24)
        )
        self.canvas.update()
        time.sleep(0.1)  # Adjust the delay as needed

    def draw_board(self):
        for i in range(self.N):
            for j in range(self.N):
                x0 = j * self.cell_size
                y0 = i * self.cell_size
                x1 = x0 + self.cell_size
                y1 = y0 + self.cell_size
                self.canvas.create_rectangle(x0, y0, x1, y1, outline="black")
                if self.board[i][j] != 0:
                    self.canvas.create_text(
                        x0 + self.cell_size // 2,
                        y0 + self.cell_size // 2,
                        text=str(self.board[i][j]),
                        font=("Arial", 24)
                    )


def main():
    board = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]

    root = tk.Tk()
    root.title("Sudoku Solver")
    canvas = tk.Canvas(root, width=450, height=450)
    canvas.pack()

    solver = SudokuSolver(board, canvas)
    solver.draw_board()

    solve_button = tk.Button(root, text="Solve", command=solver.solve_with_delay)
    solve_button.pack()

    root.mainloop()


if __name__ == "__main__":
    main()
