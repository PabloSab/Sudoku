
import pygame, sys
from sudoku_generator import SudokuGenerator, generate_sudoku, generate_sudoku1
import copy

def main():
    pygame.init()
    pygame.font.init()
    SCREEN_WIDTH = 600
    SCREEN_LENGTH = 600

    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_LENGTH))
    pygame.display.set_caption("Sudoku")
    draw_start_screen(screen)

# Draws the winning screen. When a sudoku is successfully completed this method gets called.
def draw_start_screen(screen):
    Sudoku = SudokuGenerator(9,30)
    Sudoku.fill_values()
    bg = pygame.image.load('images//sudokubackground.jpg')
    screen.blit(bg, (0, 0))
    my_font = pygame.font.SysFont('Arial', 50)
    text = my_font.render('Welcome to Sudoku', True, (0, 0, 0))
    screen.blit(text, (100, 200))

    # named buttons for easier reference

    easy_button = draw_button(screen, "Easy", 50, 400)
    medium_button = draw_button(screen, "Medium", 225, 400)
    hard_button = draw_button(screen, "Hard", 400, 400)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if easy_button.collidepoint(event.pos):
                    game_screen(screen, 'easy')
                if medium_button.collidepoint(event.pos):
                    game_screen(screen, 'medium')
                if hard_button.collidepoint(event.pos):
                    game_screen(screen, 'hard')

        pygame.display.update()

# Draws the losing screen. FUnction is called when you solve a sudoku incorrectly.
def draw_lose_screen(screen):
    bg = pygame.image.load('images//sudokubackground.jpg')
    funny_pic = pygame.image.load('images/lose.png')
    funny_pic = pygame.transform.scale(funny_pic, (200, 200))
    screen.blit(bg, (0, 0))
    screen.blit(funny_pic, (350,150))
    my_font = pygame.font.SysFont('Arial', 50)
    text = my_font.render('Game Over :(', True, (0, 0, 0))
    screen.blit(text, (50, 200))

    exit_button = draw_button(screen, "Restart", 225, 450)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button.collidepoint(event.pos):
                    draw_start_screen(screen)


        pygame.display.update()

def draw_win_screen(screen):
    bg = pygame.image.load('images//sudokubackground.jpg')
    funny_pic = pygame.image.load('images/win.jpg')
    funny_pic = pygame.transform.scale(funny_pic, (200, 200))
    screen.blit(bg, (0, 0))
    screen.blit(funny_pic, (350,150))
    my_font = pygame.font.SysFont('Arial', 50)
    text = my_font.render('You Won!!', True, (0, 0, 0))
    screen.blit(text, (50, 200))

    exit_button = draw_button(screen, "Exit", 225, 450)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button.collidepoint(event.pos):
                    sys.exit()


        pygame.display.update()

# Draws buttons. Takes the screen where it will draw it, the text, and its x and y position (as integers) as parameters.
def draw_button(screen, text, button_x, button_y):
    button_color = (255, 99, 71)
    text_color = (255, 255, 255)
    font = pygame.font.Font(None, 50)
    button_width = 150
    button_height = 75

    button_surface = pygame.Surface((button_width, button_height))
    button_surface.fill(button_color)

    text_surface = font.render(text, True, text_color)

    text_x = (button_width - text_surface.get_width()) // 2
    text_y = (button_height - text_surface.get_height()) // 2

    # Blit the text surface onto the button surface
    button_surface.blit(text_surface, (text_x, text_y))

    button_surface.blit(text_surface, (100, 100))

    b = screen.blit(button_surface, (button_x, button_y))

    return b



# This method will be used to draw the main screen of the game. Tho I think drawing the grid is done with the board class.
def game_screen(screen, difficulty, board = None):
    count = 0
    if difficulty == 'easy':
        removed = 30
    elif difficulty == 'medium':
        removed = 40
    else:
        removed = 50
    if board == None:
        # Original is used to call the function again when hitting reset button.
        board, solution = generate_sudoku1(9, removed)
        original = copy.deepcopy(board)
    else:
        original = copy.deepcopy(board)
    draw_board(screen, board)
    reset_button = draw_button(screen, "reset", 25, 500)
    restart_button = draw_button(screen, "restart", 225, 500)
    exit_button = draw_button(screen, "exit", 425, 500)

    # Creates a copy of the board to modify the sketched values without affecting the original board.
    sketched_board = copy.deepcopy(board)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if reset_button.collidepoint(event.pos):
                    game_screen(screen, difficulty, original)
                if restart_button.collidepoint(event.pos):
                    game_screen(screen, difficulty)
                if exit_button.collidepoint(event.pos):
                    sys.exit()
                pos = pygame.mouse.get_pos()
                if pos[0] <= 396 and pos[1] <= 396:
                    if count > 0:
                        pygame.draw.rect(screen, (0, 0, 0), rect, 1)  # red border
                    cell_size = 400 // 9
                    col = pos[0] // 44 # 44 is cell size aka 400//9 = 44
                    row = pos[1] // 44
                    value = sketched_board[row][col]
                    rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                    pygame.draw.rect(screen, (255, 0, 0), rect, 1)  # red border
                    count += 1

            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7,
                                 pygame.K_8, pygame.K_9]:
                    if board[row][col] != 0:
                        pass
                    else:
                        # Get the number value from the key event
                        value = int(event.unicode)
                        #   clear the cell before assigning the new value
                        sketched_board[row][col] = 0
                        sketched_board[row][col] = value
                        sketch_number(screen, rect, value)

                if event.key == pygame.K_RETURN:
                    # *** Coloring the values as they are entered ***
                    colors = [[255, 204, 153], [255, 0, 0], [0, 255, 0], [0, 0, 255]]
                    colors1 = [[153, 255, 153], [102, 0, 102], [0, 0, 0], [255, 255, 0]]
                    colors2 = [[153, 204, 255], [0, 255, 255], [204, 0, 102], [255, 128, 0]]
                    color = 0
                    board[row][col] = value
                    font = pygame.font.SysFont('Arial', 24)
                    if color < 3:
                        color = 0
                    if row < 3:
                        if col == 3 or col == 4 or col == 5:
                            color += 1
                        if col == 6 or col == 7 or col == 8:
                            color += 2
                        pygame.draw.rect(screen, (255, 255, 255), rect)  # Fill the cell with the background color
                        pygame.draw.rect(screen, (255, 0, 0), rect, 1)
                        text = font.render(str(value), True, (colors[color][0], colors[color][1], colors[color][2]))
                        text_rect = text.get_rect(center=rect.center)
                        screen.blit(text, text_rect)

                    if 3 <= row < 6:
                        if col == 3 or col == 4 or col == 5:
                            color += 1
                        if col == 6 or col == 7 or col == 8:
                            color +=2
                        pygame.draw.rect(screen, (255, 255, 255), rect)  # Fill the cell with the background color
                        pygame.draw.rect(screen, (255, 0, 0), rect, 1)
                        text = font.render(str(value), True, (colors1[color][0], colors1[color][1], colors1[color][2]))
                        text_rect = text.get_rect(center=rect.center)
                        screen.blit(text, text_rect)

                    if 6 <= row < 9:
                        if col == 3 or col == 4 or col == 5:
                            color += 1
                        if col == 6 or col == 7 or col == 8:
                            color += 2
                        pygame.draw.rect(screen, (255, 255, 255), rect)  # Fill the cell with the background color
                        pygame.draw.rect(screen, (255, 0, 0), rect, 1)
                        text = font.render(str(value), True, (colors2[color][0], colors2[color][1], colors2[color][2]))
                        text_rect = text.get_rect(center=rect.center)
                        screen.blit(text, text_rect)
                    if sum(row.count(0) for row in board) == 0:
                        if board == solution:
                            condition = 'win'
                            draw_win_screen(screen)
                        else:
                            condition = 'lose'
                            draw_lose_screen(screen)

                # Make it move with arrow keys
                if event.key == pygame.K_RIGHT:
                    if count > 0:
                        pygame.draw.rect(screen, (0, 0, 0), rect, 1)  # red border
                    col += 1
                    if col == 9:
                        col = 0
                    value = sketched_board[row][col]
                    rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                    pygame.draw.rect(screen, (255, 0, 0), rect, 1)  # red border
                    count += 1
                if event.key == pygame.K_LEFT:
                    if count > 0:
                        pygame.draw.rect(screen, (0, 0, 0), rect, 1)  # red border
                    col -= 1
                    if col == -1:
                        col = 8
                    value = sketched_board[row][col]
                    rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                    pygame.draw.rect(screen, (255, 0, 0), rect, 1)  # red border
                    count += 1

                if event.key == pygame.K_UP:
                    if count > 0:
                        pygame.draw.rect(screen, (0, 0, 0), rect, 1)  # red border
                    row -= 1
                    if row == -1:
                        row = 8
                    value = sketched_board[row][col]
                    rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                    pygame.draw.rect(screen, (255, 0, 0), rect, 1)  # red border
                    count += 1

                if event.key == pygame.K_DOWN:
                    if count > 0:
                        pygame.draw.rect(screen, (0, 0, 0), rect, 1)  # red border
                    row += 1
                    if row == 9:
                        row = 0
                    value = sketched_board[row][col]
                    rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                    pygame.draw.rect(screen, (255, 0, 0), rect, 1)  # red border
                    count += 1



        pygame.display.update()


'''
This method draws the board used to play the main loop of the game. Pablo worked on this method
and also added colors afterwards so that any 3x3 box has their own unique color to improve readability
'''
def draw_board(screen,board):
    colors =[[255,204,153],[255,0,0], [0,255,0],[0,0,255]]
    colors1 = [[153,255,153],[102, 0, 102], [0, 0, 0], [255, 255, 0]]
    colors2 = [[153,204,255], [0,255,255], [204,0,102], [255,128,0]]
    color = 0
    bg = pygame.Surface(screen.get_size())
    bg.fill((255,255,255))
    screen.blit(bg, (0,0))
    cell_size = 400 // 9
    for i in range(0,9):
        for j in range(0,9):
            value = board[i][j]
            rect = pygame.Rect(j * cell_size, i * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, (255, 255, 255), rect)  # White background
            pygame.draw.rect(screen, (0, 0, 0), rect, 1)  # black border
            if value != 0:
                font = pygame.font.SysFont('Arial', 24)
                if color < 3:
                    color = 0
                if i<3:
                    if j == 3 or j == 4 or j == 5:
                        color += 1
                    if j == 6 or j ==7 or j ==8:
                        color += 2
                    text = font.render(str(value), True, (colors[color][0], colors[color][1], colors[color][2]))
                    text_rect = text.get_rect(center=rect.center)
                    screen.blit(text, text_rect)


                if 3<=i<6:
                    if j == 3 or j ==4 or j ==5:
                        color += 1
                    if j == 6 or j == 7 or j == 8:
                        color += 2
                    text = font.render(str(value), True, (colors1[color][0], colors1[color][1], colors1[color][2]))
                    text_rect = text.get_rect(center=rect.center)
                    screen.blit(text, text_rect)

                if 6<=i<9:
                    if j == 3 or j == 4 or j == 5:
                        color += 1
                    if j == 6 or j ==7 or j ==8:
                        color += 2
                    text = font.render(str(value), True, (colors2[color][0], colors2[color][1], colors2[color][2]))
                    text_rect = text.get_rect(center=rect.center)
                    screen.blit(text, text_rect)


# Sketches a number before actually entering it.
def sketch_number(screen, rect, value):
    # Clear the rectangle area before drawing the number
    pygame.draw.rect(screen, (255, 255, 255), rect)  # Fill the cell with the background color
    pygame.draw.rect(screen, (255, 0, 0), rect, 1)
    font = pygame.font.SysFont('Arial', 16)
    text = font.render(str(value), True, (50, 50, 50))
    text_rect = text.get_rect(center=rect.center)
    screen.blit(text, text_rect)

if __name__ == '__main__':
    main()
