import pygame
import time

# Define the dimensions of the Sudoku grid
grid_size = 9
cell_size = 50
window_size = (
    cell_size * grid_size, cell_size * grid_size + 50)  # Increased window height by 50 for the elapsed time row

# Define colors
black = (0, 0, 0)
white = (255, 255, 255)

# Initialize pygame
pygame.init()

# Set up the game window
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("MAC")

# Flag to indicate if a solution has been found
solution_found = False

# Variables for elapsed time
start_time = 0
end_time = 0


def draw_grid(puzzle):
    window.fill(white)

    # Draw the Sudoku grid
    for i in range(grid_size + 1):
        if i % 3 == 0:
            pygame.draw.line(window, black, (0, i * cell_size), (grid_size * cell_size, i * cell_size), 4)
            pygame.draw.line(window, black, (i * cell_size, 0), (i * cell_size, grid_size * cell_size), 4)
        else:
            pygame.draw.line(window, black, (0, i * cell_size), (grid_size * cell_size, i * cell_size), 2)
            pygame.draw.line(window, black, (i * cell_size, 0), (i * cell_size, grid_size * cell_size), 2)

    # Draw the numbers in the Sudoku grid
    font = pygame.font.Font(None, 40)
    for i in range(grid_size):
        for j in range(grid_size):
            if puzzle[i][j] != 0:
                text = font.render(str(puzzle[i][j]), True, black)
                text_rect = text.get_rect(center=((j * cell_size) + cell_size // 2, (i * cell_size) + cell_size // 2))
                window.blit(text, text_rect)

    # Display elapsed time
    if start_time > 0 and not solution_found:
        elapsed_time = (time.time() - start_time) / 60  # Convert seconds to minutes
        time_text = font.render("Time: {:.2f} minutes".format(elapsed_time), True, black)
        window.blit(time_text, (10, window_size[1] - 30))

    pygame.display.flip()


def is_consistent(puzzle, row, column, number):
    # Check if the number already exists in the same row
    for i in range(grid_size):
        if puzzle[row][i] == number:
            return False

    # Check if the number already exists in the same column
    for i in range(grid_size):
        if puzzle[i][column] == number:
            return False

    # Check if the number already exists in the same 3x3 grid
    start_row = (row // 3) * 3
    start_col = (column // 3) * 3
    for i in range(3):
        for j in range(3):
            if puzzle[start_row + i][start_col + j] == number:
                return False

    return True


def get_domain(board, row, col):
    domain = set(range(1, 10))

    # Remove numbers that already exist in the row & col
    for i in range(9):
        if board[row][i] != 0:
            domain.discard(board[row][i])
        if board[i][col] != 0:
            domain.discard(board[i][col])

    # Remove numbers that exist in 3x3 grid from the domain
    start_row = (row // 3) * 3
    start_col = (col // 3) * 3
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] != 0:
                domain.discard(board[i][j])

    return domain


def revise(puzzle, number):
    # Reduce the domain of variables
    for row in range(grid_size):
        for column in range(grid_size):
            if puzzle[row][column] == -1:  # If cell value = -1, then the cell is unassigned
                puzzle[row][column] = number  # Assign the number
                domain = get_domain(puzzle, row, column)  # Get the domain of the cell

                if number in domain:  # Remove the number from the domain if number found in domain; correct assignment
                    domain.remove(number)

                    if not is_consistent(puzzle, row, column,
                                         number):  # Check consistency; return False if number violates constraint
                        return False
    return True


def mac(puzzle):
    global solution_found, start_time, end_time

    # Find unassigned cell
    for row in range(grid_size):
        for column in range(grid_size):
            if puzzle[row][column] == 0:
                domain = get_domain(puzzle, row, column)
                # Try all possible numbers
                for number in domain:
                    if is_consistent(puzzle, row, column, number):

                        # Assign the number
                        puzzle[row][column] = number

                        # Reduce the domain of variables
                        if revise(puzzle, number):
                            # Update the GUI
                            draw_grid(puzzle)
                            pygame.time.delay(100)

                        # Recursive
                        if mac(puzzle):
                            solution_found = True
                            return True

                        # Backtrack
                        puzzle[row][column] = 0


                # If no number leads to a solution, return False
                return False

    # All cells are assigned, puzzle is solved
    return True


# List of Sudoku puzzles to test
puzzles = [
    [
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
]

for puzzle in puzzles:
    # Copy the puzzle to avoid modifying the original
    puzzle_copy = [row[:] for row in puzzle]

    # Main game loop
    running = True
    while running:
        # Event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Exit the main loop if the window is closed

        # Solve the puzzle
        if not solution_found:
            if start_time == 0:
                start_time = time.time()  # Start the timer when solving begins
            mac(puzzles[0])  # Solve the first puzzle in the list
            if solution_found:
                end_time = time.time()  # Stop the timer when a solution is found