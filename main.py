# import pygame library
import time

import pygame


def get_mouse_position(pos):
    # Function to get the grid coordinates based on mouse position
    global x
    x = pos[0] // cell_length
    if x > dimension - 1:
        x = dimension - 1
    elif x < 0:
        x = 0
    global y
    y = pos[1] // cell_length
    if y > dimension - 1:
        y = dimension - 1
    elif y < 0:
        y = 0


# Highlight the cell selected
def highlight_cell():
    # Function to draw highlight box around the selected cell
    for i in range(2):
        pygame.draw.line(screen, (255, 0, 255), (x * cell_length - 3, (y + i) * cell_length),
                         (x * cell_length + cell_length + 3, (y + i) * cell_length), 7)
        pygame.draw.line(screen, (255, 0, 255), ((x + i) * cell_length, y * cell_length),
                         ((x + i) * cell_length, y * cell_length + cell_length), 7)


def draw_grids():
    # Function to draw the Sudoku grid
    # Draw the lines
    for i in range(dimension):
        for j in range(dimension):
            if grid[i][j] != 0:
                # Fill blue color in already numbered grid
                pygame.draw.rect(screen, (0, 153, 153), (i * cell_length, j * cell_length, cell_length + 1, cell_length + 1))

                # Fill grid with default numbers specified
                text1 = fontNumbers.render(str(grid[i][j]), 1, (0, 0, 0))
                text_rect = text1.get_rect(center=(i * cell_length + cell_length / 2, j * cell_length + cell_length / 2))
                screen.blit(text1, text_rect)
    # Draw lines horizontally and vertically to form grid
    for i in range(dimension + 1):
        if i % 3 == 0:
            thick = 8
        else:
            thick = 2
        #     horizontal lines
        pygame.draw.line(screen, (0, 0, 0), (0, i * cell_length), (500, i * cell_length), thick)
        #     vertical lines
        pygame.draw.line(screen, (0, 0, 0), (i * cell_length, 0), (i * cell_length, 500 + thick / 2), thick)


def draw_number(num):
    # Function to draw the entered value in the selected cell
    # Render the number as a text surface
    text1 = fontNumbers.render(str(num), 1, (0, 0, 0))
    # Create a rectangle for the text surface, centered within the grid cell
    text_rect = text1.get_rect(center=(x * cell_length + cell_length / 2, y * cell_length + cell_length / 2))
    # Blit (draw) the text surface onto the screen at the specified rectangle
    screen.blit(text1, text_rect)


# Raise error when wrong value entered
def raise_error1():
    # Function to raise error when the wrong value is entered
    text1 = fontNumbers.render("WRONG !!!", 1, (0, 0, 0))
    # time.sleep(1)
    screen.blit(text1, (20, 570))


def raise_error2():
    # Function to raise error when an invalid number is pressed
    text1 = fontNumbers.render("Wrong !!! Not a valid Number", 1, (0, 0, 0))
    # time.sleep(1)
    screen.blit(text1, (20, 570))


# Check if the value entered in board is valid
def is_allowed_here(m, i, j, num):
    # Function to check if the entered value is valid in the Sudoku board
    for it in range(dimension):
        # check in horizontal line
        if m[i][it] == num:
            return False
        # check in vertical line
        if m[it][j] == num:
            return False
    it = i // square
    jt = j // square
    # check in square
    for i in range(it * square, it * square + square):
        for j in range(jt * square, jt * square + square):
            if m[i][j] == num:
                return False
    return True


# Solves the sudoku board using Backtracking Algorithm
def solve(grid, i, j):
    # Function to solve the Sudoku board using backtracking algorithm
    while grid[i][j] != 0:
        if i < dimension - 1:
            i += 1
        elif i == dimension - 1 and j < dimension - 1:
            i = 0
            j += 1
        elif i == dimension - 1 and j == dimension - 1:
            return True
    pygame.event.pump()
    for it in range(1, 10):
        if is_allowed_here(grid, i, j, it):
            grid[i][j] = it
            global x, y
            x = i
            y = j
            # white color background
            screen.fill((255, 255, 255))
            draw_grids()
            highlight_cell()
            pygame.display.update()
            pygame.time.delay(20)
            if solve(grid, i, j):
                return True
            else:
                grid[i][j] = 0
            # white color background
            screen.fill((255, 255, 255))
            draw_grids()
            highlight_cell()
            pygame.display.update()
            pygame.time.delay(50)
    return False


# Display instruction for the game
def instruction():
    # Function to display instructions for the game
    text1 = fontInfo.render("PRESS D TO RESET TO DEFAULT / R TO EMPTY", 1, (0, 0, 0))
    text2 = fontInfo.render("ENTER VALUES AND PRESS ENTER TO VISUALIZE", 1, (0, 0, 0))
    screen.blit(text1, (20, 520))
    screen.blit(text2, (20, 540))


# Display options when solved
def finished():
    # Function to display options when the Sudoku is solved
    text1 = fontNumbers.render("FINISHED PRESS R or D", 1, (0, 0, 0))
    screen.blit(text1, (20, 570))


def reset_grid(grid):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            grid[i][j] = 0
    return grid


def create_grid():
    grid = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]
    return grid


def copy_grid(grid_from):
    grid = create_grid()
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            grid[i][j] = grid_from[i][j]
    return grid


if __name__ == '__main__':
    # TODO: first numbers can't be edited
    # first numbers have to have another color
    # add time and scores
    # restrict cursor to go outside the table
    # errors don't work
    # randomize first table
    # centered table in the window
    # choose level of complexity %
    # load/save
    # add undo/redo

    # square
    square = 3
    # Dimention 9x9 = 9
    dimension = square * square
    # Initialise the pygame font
    pygame.font.init()

    # Total window
    # width = 500
    # height = 600
    width = 700
    height = 700
    screen = pygame.display.set_mode((width, height))

    # Title and Icon
    pygame.display.set_caption("SUDOKU GAME")
    img = pygame.image.load('icon.png')
    pygame.display.set_icon(img)

    x = 0
    y = 0
    cell_length = 500 / dimension
    num = 0
    # Default Sudoku Board.
    grid_default = create_grid()
    grid = copy_grid(grid_default)

    # Load test fonts for future use
    # font numbers
    fontNumbers = pygame.font.SysFont("comicsans", 30)
    fontInfo = pygame.font.SysFont("comicsans", 18)

    run = True
    eventPerformed = False
    toSolve = False
    isResolved = False
    wasError = False
    # The loop that keeps the window running
    while run:
        # White color background
        screen.fill((255, 255, 255))
        # Loop through the events stored in event.get()
        for event in pygame.event.get():
            # Quit the game window
            if event.type == pygame.QUIT:
                run = False
            # Get the mouse position to insert number
            if event.type == pygame.MOUSEBUTTONDOWN:
                eventPerformed = True
                pos = pygame.mouse.get_pos()
                get_mouse_position(pos)
            # Get the number to be inserted if key pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if x > 0:
                        x -= 1
                        eventPerformed = True
                if event.key == pygame.K_RIGHT:
                    if x < dimension - 1:
                        x += 1
                        eventPerformed = True
                if event.key == pygame.K_UP:
                    if y > 0:
                        y -= 1
                        eventPerformed = True
                if event.key == pygame.K_DOWN:
                    if y < dimension - 1:
                        y += 1
                        eventPerformed = True
                if event.key == pygame.K_1:
                    num = 1
                if event.key == pygame.K_2:
                    num = 2
                if event.key == pygame.K_3:
                    num = 3
                if event.key == pygame.K_4:
                    num = 4
                if event.key == pygame.K_5:
                    num = 5
                if event.key == pygame.K_6:
                    num = 6
                if event.key == pygame.K_7:
                    num = 7
                if event.key == pygame.K_8:
                    num = 8
                if event.key == pygame.K_9:
                    num = 9
                if event.key == pygame.K_RETURN:
                    toSolve = True
                # If R pressed clear the sudoku board
                if event.key == pygame.K_r:
                    isResolved = False
                    wasError = False
                    toSolve = False
                    grid = reset_grid(grid)
                # If D is pressed reset the board to default
                if event.key == pygame.K_d:
                    isResolved = False
                    wasError = False
                    toSolve = False
                    grid = copy_grid(grid_default)
        if toSolve:
            if not solve(grid, 0, 0):
                wasError = True
            else:
                isResolved = True
            toSolve = False
        if num != 0:
            draw_number(num)
            if is_allowed_here(grid, int(x), int(y), num):
                grid[int(x)][int(y)] = num
                eventPerformed = False
            else:
                grid[int(x)][int(y)] = 0
                raise_error2()
            num = 0

        if wasError:
            raise_error1()
        if isResolved:
            finished()
        draw_grids()
        if eventPerformed:
            highlight_cell()
        instruction()

        # Update window
        pygame.display.update()

        # Quit pygame window
    pygame.quit()
