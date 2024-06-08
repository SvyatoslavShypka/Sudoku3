import pygame
import random


def start_game():
    pygame_icon = pygame.image.load("icon.png")
    pygame.display.set_icon(pygame_icon)


    def get_mouse_position(pos):
        nonlocal x, y
        x = pos[0] // cell_length
        if x > dimension - 1:
            x = dimension - 1
        elif x < 0:
            x = 0
        y = pos[1] // cell_length
        if y > dimension - 1:
            y = dimension - 1
        elif y < 0:
            y = 0

    def highlight_cell():
        for i in range(2):
            pygame.draw.line(screen, (255, 0, 255), (x * cell_length - 3, (y + i) * cell_length),
                             (x * cell_length + cell_length + 3, (y + i) * cell_length), 7)
            pygame.draw.line(screen, (255, 0, 255), ((x + i) * cell_length, y * cell_length),
                             ((x + i) * cell_length, y * cell_length + cell_length), 7)

    def draw_grids():
        for i in range(dimension):
            for j in range(dimension):
                if grid[i][j] != 0:
                    pygame.draw.rect(screen, (0, 153, 153), (i * cell_length, j * cell_length, cell_length + 1, cell_length + 1))
                    text1 = fontNumbers.render(str(grid[i][j]), 1, (0, 0, 0))
                    text_rect = text1.get_rect(center=(i * cell_length + cell_length / 2, j * cell_length + cell_length / 2))
                    screen.blit(text1, text_rect)
        for i in range(dimension + 1):
            thick = 8 if i % 3 == 0 else 2
            pygame.draw.line(screen, (0, 0, 0), (0, i * cell_length), (500, i * cell_length), thick)
            pygame.draw.line(screen, (0, 0, 0), (i * cell_length, 0), (i * cell_length, 500 + thick / 2), thick)

    def draw_number(num):
        text1 = fontNumbers.render(str(num), 1, (0, 0, 0))
        text_rect = text1.get_rect(center=(x * cell_length + cell_length / 2, y * cell_length + cell_length / 2))
        screen.blit(text1, text_rect)

    def raise_error1():
        text1 = fontNumbers.render("WRONG !!!", 1, (0, 0, 0))
        screen.blit(text1, (20, 570))

    def raise_error2():
        text1 = fontNumbers.render("Wrong !!! Not a valid Number", 1, (0, 0, 0))
        screen.blit(text1, (20, 570))

    def is_allowed_here(m, i, j, num):
        for it in range(dimension):
            if m[i][it] == num or m[it][j] == num:
                return False
        it, jt = i // square, j // square
        for i in range(it * square, it * square + square):
            for j in range(jt * square, jt * square + square):
                if m[i][j] == num:
                    return False
        return True

    def solve(grid, i, j):
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
                nonlocal x, y
                x, y = i, j
                screen.fill((255, 255, 255))
                draw_grids()
                highlight_cell()
                if visualize:
                    pygame.display.update()
                pygame.time.delay(1)
                if solve(grid, i, j):
                    return True
                else:
                    grid[i][j] = 0
                screen.fill((255, 255, 255))
                draw_grids()
                highlight_cell()
                if visualize:
                    pygame.display.update()
                    pygame.time.delay(50)
        return False

    def instruction():
        text1 = fontInfo.render("PRESS D TO RESET TO DEFAULT / R TO EMPTY", 1, (0, 0, 0))
        text2 = fontInfo.render("ENTER VALUES AND PRESS ENTER TO VISUALIZE", 1, (0, 0, 0))
        screen.blit(text1, (20, 520))
        screen.blit(text2, (20, 540))

    def finished():
        text1 = fontNumbers.render("FINISHED PRESS R or D", 1, (0, 0, 0))
        screen.blit(text1, (20, 570))

    def reset_grid(grid):
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                grid[i][j] = 0
        return grid

    def create_grid():
        return [
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

    def randomize_grid(level):
        grid = [[0] * dimension for _ in range(dimension)]
        x = y = 0
        num = random.randint(1, dimension)
        for i in range(dimension):
            while not is_allowed_here(grid, x, y, num):
                num = random.randint(1, dimension)
            grid[x][y] = num
            x += 1
        solve(grid, 0, 0)
        grid = leverage_grid(grid, level)
        return grid

    def leverage_grid(grid, level):
        # Adjust the grid by removing some numbers based on the level of difficulty
        cells_to_remove = 20 + level * 5
        for _ in range(cells_to_remove):
            x = random.randint(0, dimension - 1)
            y = random.randint(0, dimension - 1)
            while grid[x][y] == 0:
                x = random.randint(0, dimension - 1)
                y = random.randint(0, dimension - 1)
            grid[x][y] = 0
        return grid

    pygame.init()

    dimension = 9
    square = 3
    cell_length = 500 // dimension
    visualize = True

    screen = pygame.display.set_mode((500, 600))
    pygame.display.set_caption("Sudoku")
    fontNumbers = pygame.font.SysFont("arial", cell_length // 2)
    fontInfo = pygame.font.SysFont("arial", 20)

    grid = create_grid()
    x = y = 0


    running = True
    while running:
        screen.fill((255, 255, 255))
        draw_grids()
        highlight_cell()
        instruction()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                get_mouse_position(pygame.mouse.get_pos())
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x = max(0, x - 1)
                elif event.key == pygame.K_RIGHT:
                    x = min(dimension - 1, x + 1)
                elif event.key == pygame.K_UP:
                    y = max(0, y - 1)
                elif event.key == pygame.K_DOWN:
                    y = min(dimension - 1, y + 1)
                elif event.key == pygame.K_1:
                    num = 1
                    if is_allowed_here(grid, x, y, num):
                        grid[x][y] = num
                    else:
                        raise_error2()
                elif event.key == pygame.K_2:
                    num = 2
                    if is_allowed_here(grid, x, y, num):
                        grid[x][y] = num
                    else:
                        raise_error2()
                elif event.key == pygame.K_3:
                    num = 3
                    if is_allowed_here(grid, x, y, num):
                        grid[x][y] = num
                    else:
                        raise_error2()
                elif event.key == pygame.K_4:
                    num = 4
                    if is_allowed_here(grid, x, y, num):
                        grid[x][y] = num
                    else:
                        raise_error2()
                elif event.key == pygame.K_5:
                    num = 5
                    if is_allowed_here(grid, x, y, num):
                        grid[x][y] = num
                    else:
                        raise_error2()
                elif event.key == pygame.K_6:
                    num = 6
                    if is_allowed_here(grid, x, y, num):
                        grid[x][y] = num
                    else:
                        raise_error2()
                elif event.key == pygame.K_7:
                    num = 7
                    if is_allowed_here(grid, x, y, num):
                        grid[x][y] = num
                    else:
                        raise_error2()
                elif event.key == pygame.K_8:
                    num = 8
                    if is_allowed_here(grid, x, y, num):
                        grid[x][y] = num
                    else:
                        raise_error2()
                elif event.key == pygame.K_9:
                    num = 9
                    if is_allowed_here(grid, x, y, num):
                        grid[x][y] = num
                    else:
                        raise_error2()
                elif event.key == pygame.K_RETURN:
                    if solve(grid, 0, 0):
                        finished()
                    else:
                        raise_error1()
                elif event.key == pygame.K_r:
                    grid = reset_grid(grid)
                elif event.key == pygame.K_d:
                    grid = create_grid()

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    start_game()
