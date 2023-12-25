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
pygame.display.set_caption("Soduku solver using BT")

# Flag to indicate if a solution has been found
solution_found = False

# Variables for elapsed time
start_timer = 0
end_timer = 0


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
    if start_timer > 0 and not solution_found:
        elapsed_time = (time.time() - start_timer) / 60  # Convert seconds to minutes
        time_text = font.render("Time: {:.2f} minutes".format(elapsed_time), True, black)
        window.blit(time_text, (10, window_size[1] - 30))

    pygame.display.flip()



def valid(puzzle, num, pos):
    # Check row
    for i in range(len(puzzle[0])):
        if puzzle[pos[0]][i] == num and pos[1] != i:
            return False

    # Check column
    for i in range(len(puzzle)):
        if puzzle[i][pos[1]] == num and pos[0] != i:
            return False

    # Check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x * 3, box_x*3 + 3):
            if puzzle[i][j] == num and (i,j) != pos:
                return False

    return True


def BT(puzzle):
    global solution_found, start_timer, end_timer
    # Find unassigned cell
    for row in range(grid_size):
        for col in range(grid_size):
            if puzzle[row][col] == 0:
                # Try all possible numbers
                for i in range(1, 10):
                    if valid(puzzle, i, (row,col,)):
                        # Assign the number
                        puzzle[row][col] = i
                        # Update the GUI
                        draw_grid(puzzle)
                        pygame.time.delay(100)

                        # Recursive
                        if BT(puzzle):
                            solution_found = True
                            return True

                        # Backtrack
                        puzzle[row][col] = 0

                # If no number leads to a solution, return False
                return False

    # All cells are assigned, puzzle is solved
    return True


# List of Sudoku puzzles to test
puzzles = [
    [
        [0, 0, 4, 0, 0, 0, 0, 0, 2],
        [0, 0, 0, 0, 0, 8, 0, 0, 0],
        [0, 0, 0, 0, 7, 0, 3, 0, 8],
        [0, 0, 0, 0, 0, 0, 0, 2, 0],
        [0, 5, 0, 0, 0, 0, 0, 7, 0],
        [0, 7, 6, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 3, 0, 0, 1, 0, 0],
        [0, 4, 0, 0, 0, 0, 0, 0, 0],
        [7, 0, 0, 0, 0, 0, 6, 0, 0]
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
            if start_timer == 0:
                start_timer = time.time()  # Start the timer when solving begins
            BT(puzzles[0])  # Solve the first puzzle in the list
            if solution_found:
                end_timer = time.time()  # Stop the timer when a solution is found
    '''# Solve the puzzle using MAC algorithm
    if MAC(puzzle_copy):
        print("Sudoku puzzle solved:")
        for row in puzzle_copy:
            print(row)
        print()
    else:
        print("No solution found for the Sudoku puzzle.")'''
