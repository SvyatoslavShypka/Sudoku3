from PySide6.QtWidgets import QLabel, QMessageBox, QApplication, QHBoxLayout, QVBoxLayout, QPushButton, \
    QSlider, QInputDialog, QFileDialog
from PySide6.QtGui import QPainter, QFont, QColor, QPen, QMouseEvent
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QTimer, QRect
import random
from datetime import datetime
import json


class LoginWindow(QWidget):
    window_width = 1000
    window_height = 800
    CONFIG_FILE = "config.json"

    def __init__(self):
        super().__init__()
        self.error_label = QLabel(self)
        self.game_display = GameWidget(self)
        self.instructions_label = QLabel(self)
        self.new_game_button = None
        self.save_game_button = None
        self.load_game_button = None
        self.exit_button = None
        self.last_saved_filename = None
        self.load_config()
        self.difficulty_slider = None
        self.setup()

    def save_config(self):
        # Save the last saved file name to the configuration file
        with open(self.CONFIG_FILE, 'w') as f:
            json.dump({"last_saved_filename": self.last_saved_filename}, f)

    def load_config(self):
        # Load the last saved file name from the configuration file
        try:
            with open(self.CONFIG_FILE, 'r') as f:
                config = json.load(f)
                self.last_saved_filename = config.get("last_saved_filename")
        except FileNotFoundError:
            pass  # Ignore if the configuration file does not exist

    def exit_app(self):
        reply = QMessageBox.question(self, 'Quit Application',
                                     "<b>Are you sure you want to quit?</b>",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            QApplication.instance().quit()

    def setup(self):
        main_layout = QHBoxLayout()

        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        button_size = (120, 40)

        self.new_game_button = QPushButton("New game", self)
        self.new_game_button.setFixedSize(*button_size)
        self.new_game_button.clicked.connect(self.start_game)
        left_layout.addWidget(self.new_game_button)

        self.save_game_button = QPushButton("Save game", self)
        self.save_game_button.setFixedSize(*button_size)
        self.save_game_button.setEnabled(False)  # Initially inactive
        self.save_game_button.clicked.connect(self.save_game)
        left_layout.addWidget(self.save_game_button)

        self.load_game_button = QPushButton("Load game", self)
        self.load_game_button.setFixedSize(*button_size)
        self.load_game_button.clicked.connect(self.load_game)
        left_layout.addWidget(self.load_game_button)

        self.exit_button = QPushButton("Exit", self)
        self.exit_button.setFixedSize(*button_size)
        self.exit_button.clicked.connect(self.exit_app)
        left_layout.addWidget(self.exit_button)

        self.difficulty_slider = QSlider(Qt.Horizontal, self)  # Slider creation
        self.difficulty_slider.setMinimum(1)
        self.difficulty_slider.setMaximum(3)
        self.difficulty_slider.setValue(1)  # default value
        self.difficulty_slider.setTickInterval(1)
        self.difficulty_slider.setTickPosition(QSlider.TicksBelow)

        # Making fixed size for slider
        self.difficulty_slider.setFixedWidth(200)
        self.difficulty_slider.setFixedHeight(20)

        # Slider label
        slider_title = QLabel("Difficulty Level", self)
        slider_title.setAlignment(Qt.AlignCenter)

        # Slider values
        self.slider_value_label = QLabel(f"Current Value: {self.difficulty_slider.value()}", self)
        self.slider_value_label.setAlignment(Qt.AlignCenter)

        # Slider value update
        self.difficulty_slider.valueChanged.connect(self.update_difficulty)
        self.difficulty_slider.valueChanged.connect(lambda value: self.slider_value_label.setText(f"Current Value: {value}"))

        self.instructions_label.setText(
            "Instructions:\n"
            "- Use arrow keys to move around the grid.\n"
            "- Press numbers 1-9 to fill in the cells.\n"
            "- Press 'R' to reset the game.\n"
            "- Press 'Delete' or 'Backspace' to clear a cell.\n"
            "- Press 'Enter' to demonstrate solving the puzzle.\n"
        )
        self.instructions_label.setStyleSheet("QLabel { font-size: 16px; }")
        left_layout.addWidget(self.instructions_label)

        left_layout.addWidget(slider_title)
        left_layout.addWidget(self.difficulty_slider)
        left_layout.addWidget(self.slider_value_label)
        left_layout.addWidget(self.error_label)
        left_layout.addStretch(1)  # Add a stretch to push everything to the top

        main_layout.addLayout(left_layout)
        right_layout.addWidget(self.game_display)

        right_layout.addWidget(self.game_display)
        main_layout.addLayout(right_layout)

        self.setLayout(main_layout)

        self.game_display.setVisible(False)  # Initially hide the game display

        self.setFixedSize(self.window_width, self.window_height)
        self.setWindowTitle("Sudoku Game - Dariusz Szypka")

        self.setStyleSheet("""
            QWidget {
            background-color: #adaec4;
                   }
            QPushButton {
            background-color: #4CAF50; 
            color: white; 
            border: none; 
            padding: 10px 20px; 
            text-align: center; 
            text-decoration: none; 
            display: inline-block; 
            font-size: 16px; 
            margin: 4px 2px; 
            transition-duration: 0.4s; 
            cursor: pointer; /* Pointer cursor on hover */
            max-width: 150px; /* Maximum width */
            max-height: 40px; /* Maximum height */
                }
            QPushButton:hover {
            background-color: #ebd9bc; 
            color: black; /* Black text on hover */
                }
            QLabel {
            color: #333;
                }
            QSlider::groove:horizontal {
                border: 1px solid #bbb;
                background: #ebd9bc;
                height: 10px;
                border-radius: 4px;
                   }
            QSlider::sub-page:horizontal {
                background: #4CAF50;
                border: 1px solid #4CAF50;
                height: 10px;
                border-radius: 4px;
                   }
            QSlider::handle:horizontal {
                background: #000000;
                border: 1px solid #4CAF50;
                width: 20px;
                height: 20px;
                border-radius: 10px;
                margin: -5px 0;
                   }
               """)
        self.show()

    def start_game(self):
        self.error_label.clear()  # Clear any previous error messages
        self.game_display.start_game()
        self.game_display.setVisible(True)  # Show the game display
        self.save_game_button.setEnabled(True)  # Enable the save game button
        self.game_display.setFocus()  # Give focus to the GameWidget after starting the game

    def save_game(self):
        self.error_label.clear()  # Clear any previous error messages


        current_time = datetime.now().strftime("%Y%m%d-%H%M%S")
        suggested_filename = f"{current_time}.json"

        # Prompt the user for the filename
        filename, ok = QInputDialog.getText(self, "Save Game", "<b>Enter filename:</b>", text=suggested_filename)

        if ok and filename:
            self.game_display.save_game(filename)
            self.last_saved_filename = filename
            self.save_config()

    def load_game(self):
        self.error_label.clear()  # Clear any previous error messages

        # Suggest the last saved file name
        suggested_filename = self.last_saved_filename if self.last_saved_filename else "default_filename.json"

        # Open a file dialog to select the file to load
        filename, _ = QFileDialog.getOpenFileName(self, "Load game", suggested_filename,
                                                  "JSON Files (*.json);;All Files (*)")
        if filename:
            # Load the selected file
            self.game_display.load_game(filename)
            self.save_game_button.setEnabled(True)  # Enable the save game button
            self.game_display.setVisible(True)  # Show the game display
            self.game_display.setFocus()  # Give focus to the GameWidget after starting the game

    def update_difficulty(self, value):
        self.game_display.difficulty = value


class GameWidget(QWidget):
    square = 3
    dimension = square * square
    side = LoginWindow.window_width - 400
    cell_length = side // dimension
    thick_line = 8
    thin_line = 2

    def __init__(self, parent=None):
        super().__init__(parent)
        self.start_val = 1
        self.num_found = False
        self.solve_timer = QTimer()
        self.solve_i = self.solve_j = 0
        self.setFixedSize(self.side, self.side)
        self.grid = None
        self.begin_grid = None
        self.key_count = 1
        self.x = self.y = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_game)
        self.setFocusPolicy(Qt.StrongFocus)  # Set focus policy to accept key events
        self.parent = parent
        self.difficulty = 1
        self.solve_thread = None
        self.left_cells = self.dimension * self.dimension

    def save_game(self, file_name):
        game_state = self.serialize_game_state()
        with open(file_name, 'w') as file:
            json.dump(game_state, file)
        self.parent.error_label.setText("<b>Game saved successfully into file:  </b>" + file_name)

    def load_game(self, file_name):
        try:
            with open(file_name, 'r') as file:
                game_state = json.load(file)
            self.deserialize_game_state(game_state)
            self.update_game()
            self.parent.error_label.setText("<b>Game loaded successfully</b>")
        except FileNotFoundError:
            self.parent.error_label.setText("<b>No saved game found</b>")
        except json.JSONDecodeError:
            self.parent.error_label.setText("<b>Error loading saved game</b>")

    def serialize_game_state(self):
        game_state = {
            'grid': self.grid,
            'begin_grid': self.begin_grid,
            'x': self.x,
            'y': self.y,
            'key_count': self.key_count,
            'left_cells': self.left_cells,
        }
        return game_state

    def deserialize_game_state(self, game_state):
        self.grid = game_state['grid']
        self.begin_grid = game_state['begin_grid']
        self.x = game_state['x']
        self.y = game_state['y']
        self.key_count = game_state['key_count']
        self.left_cells = game_state['left_cells']

    def create_grid(self):
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
        grid, count_zeros = self.leverage_grid(grid, self.difficulty)
        self.left_cells = count_zeros
        self.begin_grid = self.get_copy_from_grid(grid)
        return grid

    def leverage_grid(self, grid, level):
        # Adjust the grid by removing some numbers based on the level of difficulty
        # it's not the best variant
        cells_to_remove = int(self.dimension * self.dimension * level / 4 - 3)
        cells_to_remove_box = cells_to_remove // 9
        count_zeros = 0
        x_step = y_step = 0
        for _ in range(cells_to_remove):
            x = random.randint(0, 2) + x_step
            y = random.randint(0, 2) + y_step
            while grid[x][y] == 0:
                x = random.randint(0, 2) + x_step
                y = random.randint(0, 2) + y_step
                # x = random.randint(0, self.dimension - 1)
                # y = random.randint(0, self.dimension - 1)
            grid[x][y] = 0
            count_zeros += 1
            if count_zeros % cells_to_remove_box == 0:
                x_step += 3
                if x_step > 6:
                    x_step = 0
                    y_step += 3
                    if y_step > 6:
                        break
        return grid, count_zeros

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
                    if self.is_starting_position(i, j):
                        # color of the starting cells
                        painter.fillRect(rect, QColor(0, 153, 0))
                        painter.drawText(rect, Qt.AlignCenter, str(self.grid[i][j]))
                    else:
                        # color of other cells
                        painter.fillRect(rect, QColor(0, 153, 153))
                        painter.drawText(rect, Qt.AlignCenter, str(self.grid[i][j]))
        for i in range(self.dimension + 1):
            thickness = self.thick_line if i % self.square == 0 else self.thin_line
            if i == 0:
                thickness = 2 * thickness
            painter.setPen(QPen(QColor(0, 0, 0), thickness))
            # horisontal lines
            y_pos = i * self.cell_length
            painter.drawLine(0, y_pos, self.side - thickness - 1, y_pos)
            # vertical lines
            x_pos = i * self.cell_length
            painter.drawLine(x_pos, 0, x_pos, self.side - self.thick_line - 2)

    def is_starting_position(self, i, j):
        return self.begin_grid[i][j] != 0

    def highlight_cell(self, painter):
        painter.setPen(QPen(QColor(255, 0, 255), self.thick_line))
        for i in range(2):
            # up_horizontal_line
            painter.drawLine(self.x * self.cell_length, (self.y + i) * self.cell_length,
                             self.x * self.cell_length + self.cell_length, (self.y + i) * self.cell_length)
            painter.drawLine((self.x + i) * self.cell_length, self.y * self.cell_length,
                             (self.x + i) * self.cell_length, self.y * self.cell_length + self.cell_length)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Left:
            self.x = max(0, self.x - 1)
        elif event.key() == Qt.Key_Right:
            self.x = min(8, self.x + 1)
        elif event.key() == Qt.Key_Up:
            self.y = max(0, self.y - 1)
        elif event.key() == Qt.Key_Down:
            self.y = min(8, self.y + 1)
        elif event.key() == Qt.Key_R:
            self.grid = self.get_copy_from_grid(self.begin_grid)
            self.update_game()
        elif event.key() == Qt.Key_Delete or event.key() == Qt.Key_Backspace:
            if not self.is_starting_position(self.x, self.y):
                self.grid[self.x][self.y] = 0
                self.left_cells += 1
        elif Qt.Key_1 <= event.key() <= Qt.Key_9:
            num = event.key() - Qt.Key_0
            if not self.is_starting_position(self.x, self.y):
                if self.is_allowed_here(self.grid, self.x, self.y, num):
                    self.grid[self.x][self.y] = num
                    self.left_cells -= 1
                    self.parent.error_label.clear()  # Clear the error message if the move is valid
                else:
                    self.parent.error_label.setText("<b>Invalid move</b>")
        elif event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.solve_with_delay()
            # self.left_cells = 0
            self.update_game()
        if self.left_cells == 0:
            self.parent.error_label.setText("<b>Congratulations!!! You solved the puzzle.</b>")
        self.update_game()

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.x = int(event.position().x() // (self.side // self.dimension))
            self.y = int(event.position().y() // (self.side // self.dimension))
            self.update_game()

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

    def get_copy_from_grid(self, origin_grid):
        # create grid with zeros
        copy_grid = [[0 for _ in range(self.dimension)] for _ in range(self.dimension)]
        for i in range(len(copy_grid)):
            for j in range(len(copy_grid[0])):
                copy_grid[i][j] = origin_grid[i][j]
        return copy_grid

    def solve_with_delay(self):
        self.grid = self.get_copy_from_grid(self.begin_grid)
        self.update_game()
        self.solve_i, self.solve_j = 0, 0
        self.solve_stack = []  # Stack to keep track of cells being solved
        self.solve_timer = QTimer()
        self.solve_timer.timeout.connect(self.step_solve)
        self.solve_timer.start(5)  # Adjust the delay as necessary

    def step_solve(self):
        if self.solve_i >= self.dimension:
            self.solve_timer.stop()
            self.parent.error_label.setText("<b> Automatically solved the puzzle step-by-step</b>")
            return

        # Find the next empty cell
        while self.solve_i < self.dimension and self.grid[self.solve_i][self.solve_j] != 0:
            self.solve_j += 1
            if self.solve_j == self.dimension:
                self.solve_j = 0
                self.solve_i += 1

        if self.solve_i < self.dimension:
            if self.num_found:
                self.num_found = False
                self.start_val = 1

            for val in range(self.start_val, self.dimension + 1):
                if self.is_allowed_here(self.grid, self.solve_i, self.solve_j, val):
                    self.grid[self.solve_i][self.solve_j] = val
                    self.left_cells -= 1
                    self.solve_stack.append((self.solve_i, self.solve_j, val))  # Save the cell state
                    self.update()
                    self.num_found = True
                    break

            if not self.num_found:
                if self.solve_stack:
                    last_i, last_j, last_val = self.solve_stack.pop()
                    self.grid[last_i][last_j] = 0
                    self.left_cells += 1
                    self.start_val = last_val + 1
                    self.solve_i, self.solve_j = last_i, last_j
                    self.solve_j -= 1  # Move back to try next value
                    if self.solve_j < 0:
                        self.solve_i -= 1
                        self.solve_j = self.dimension - 1

        self.update_game()
