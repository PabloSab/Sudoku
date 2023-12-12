import copy
import math, random


class SudokuGenerator:
    '''
	Parameters:
    row_length is the number of rows/columns of the board (always 9 for this project)
    removed_cells is an integer value - the number of cells to be removed

	Return:
	None
    '''

    def __init__(self, row_length, removed_cells):
        self.row_length = 9
        self.board = [[0 for i in range(9)] for j in range(9)]
        self.box_length = 3
        self.removed_cells = removed_cells

    '''
	Returns a 2D python list of numbers which represents the board

	Parameters: None
    '''

    def get_board(self):
        return self.board

    '''
	Displays the board to the console
    This is not strictly required, but it may be useful for debugging purposes

	Parameters: None
	Return: None
    '''

    def print_board(self):
        for i in range(len(self.board)):
            print(self.board[i])

    '''
	Determines if num is contained in the specified row (horizontal) of the board
    If num is already in the specified row, return False. Otherwise, return True

	Parameters:
	row is the index of the row we are checking
	num is the value we are looking for in the row

	Return: boolean
    '''

    def valid_in_row(self, row, num):
        for i in range(0, 9):  # cols 0-8
            if self.board[row][i] == num:
                return False
        return True

    '''
	Determines if num is contained in the specified column (vertical) of the board
    If num is already in the specified col, return False. Otherwise, return True

	Parameters:
	col is the index of the column we are checking
	num is the value we are looking for in the column

	Return: boolean
    '''

    def valid_in_col(self, col, num):
        try:
            for i in range(0, 9):
                if col > 9:
                    raise Exception  # Column index is out of range
                if self.board[i][col] == num:
                    return False
            return True
        except:
            print("input a row from 1-9")

    '''
	Determines if num is contained in the 3x3 box specified on the board
    If num is in the specified box starting at (row_start, col_start), return False.
    Otherwise, return True

	Parameters:
	row_start and col_start are the starting indices of the box to check
	i.e. the box is from (row_start, col_start) to (row_start+2, col_start+2)
	num is the value we are looking for in the box

	Return: boolean
    '''

    def valid_in_box(self, row_start, col_start, num):
        row_start = row_start // 3 * 3
        col_start = col_start // 3 * 3
        for i in range(row_start, row_start + 3):
            for j in range(col_start, col_start + 3):
                if i >= self.row_length or j >= self.row_length:
                    break
                if self.board[i][j] == num:
                    return False
        return True
    '''
    Determines if it is valid to enter num at (row, col) in the board
    This is done by checking that num is unused in the appropriate, row, column, and box

	Parameters:
	row and col are the row index and col index of the cell to check in the board
	num is the value to test if it is safe to enter in this cell

	Return: boolean
    '''

    def is_valid(self, row, col, num):
        if self.valid_in_row(row, num) and self.valid_in_col(col, num) and self.valid_in_box(row, col, num):
            return True
        else:
            return False

    '''
    Fills the specified 3x3 box with values
    For each position, generates a random digit which has not yet been used in the box

	Parameters:
	row_start and col_start are the starting indices of the box to check
	i.e. the box is from (row_start, col_start) to (row_start+2, col_start+2)

	Return: None
    '''

    def fill_box(self, row_start, col_start):
        box_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        random.shuffle(box_numbers)
        count = 0
        for i in range(row_start, row_start + 3):
            for j in range(col_start, col_start + 3):
                self.board[i][j] = box_numbers[count]
                count += 1

    '''
    Fills the three boxes along the main diagonal of the board
    These are the boxes which start at (0,0), (3,3), and (6,6)

	Parameters: None
	Return: None
    '''

    def fill_diagonal(self):
        self.fill_box(0, 0)
        self.fill_box(3, 3)
        self.fill_box(6, 6)

    '''

	Parameters:
	row, col specify the coordinates of the first empty (0) cell

	Return:
	boolean (whether or not we could solve the board)
    '''

    def fill_remaining(self, row, col):
        if (col >= self.row_length and row < self.row_length - 1):
            row += 1
            col = 0
        if row >= self.row_length and col >= self.row_length:
            return True
        if row < self.box_length:
            if col < self.box_length:
                col = self.box_length
        elif row < self.row_length - self.box_length:
            if col == int(row // self.box_length * self.box_length):
                col += self.box_length
        else:
            if col == self.row_length - self.box_length:
                row += 1
                col = 0
                if row >= self.row_length:
                    return True

        for num in range(1, self.row_length + 1):
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                if self.fill_remaining(row, col + 1):
                    return True
                self.board[row][col] = 0
        return False

    '''
	Parameters: None
	Return: None
    '''

    def fill_values(self):
        self.fill_diagonal()
        self.fill_remaining(0, self.box_length)

    '''
    Removes the appropriate number of cells from the board
    This is done by setting some values to 0
    Should be called after the entire solution has been constructed
    i.e. after fill_values has been called


	Parameters: None
	Return: None
    '''

    def remove_cells(self):
        i = 0
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        while i < self.removed_cells:
            if self.board[row][col] == 0:
                row = random.randint(0, 8)
                col = random.randint(0, 8)
            else:
                self.board[row][col] = 0
                i += 1
                row = random.randint(0, 8)
                col = random.randint(0, 8)


'''
Given a number of rows and number of cells to remove, this function:
1. creates a SudokuGenerator
2. fills its values and saves this as the solved state
3. removes the appropriate number of cells
4. returns the representative 2D Python Lists of the board and solution

Parameters:
size is the number of rows/columns of the board (9 for this project)
removed is the number of cells to clear (set to 0)

Return: list[list] (a 2D Python list to represent the board)
'''

def generate_sudoku1(size, removed):
    sudoku = SudokuGenerator(size, removed)
    sudoku.fill_values()
    board = sudoku.get_board()
    sol_board = copy.deepcopy(board)
    sudoku.remove_cells()
    board = sudoku.get_board()
    return board, sol_board

