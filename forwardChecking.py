import time
def is_consistent(puzzle, row, column, number):
    # Check if the number already exists in the same row
    for i in range(9):
        if puzzle[row][i] == number:
            return False

    # Check if the number already exists in the same column
    for i in range(9):
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


def FC(puzzle):
    global updated_cells
    for row in range(9):
        for column in range(9):
            if puzzle[row][column] == 0:        #found an empty sell 
                domain = get_domain(puzzle, row, column)
                for num in domain:              #searching for a valid value, inside the current domain only 
                    if is_consistent(puzzle, row, column, num):
                        puzzle[row][column] = num

                        # Update direct neighboring cells' domains after the assignment
                        updated_cells = []
                        if row > 0 and puzzle[row - 1][column] == 0:
                            update_neighbour_domain(puzzle, row - 1, column, num)
                            updated_cells.append((row - 1, column))
                        if row < 9 - 1 and puzzle[row + 1][column] == 0:
                            update_neighbour_domain(puzzle, row + 1, column, num)
                            updated_cells.append((row + 1, column))
                        if column > 0 and puzzle[row][column - 1] == 0:
                            update_neighbour_domain(puzzle, row, column - 1, num)
                            updated_cells.append((row, column - 1))
                        if column < 9 - 1 and puzzle[row][column + 1] == 0:
                            update_neighbour_domain(puzzle, row, column + 1, num)
                            updated_cells.append((row, column + 1))

                        if FC(puzzle):
                            return True

                        # Restore the previous state
                        puzzle[row][column] = 0
                        restore_neighbour_domain(puzzle, updated_cells)

                # # If no valid assignment found, restore previous state and return False
                puzzle[row][column] = 0
                restore_neighbour_domain(puzzle, updated_cells)
                return False

    # All cells filled, puzzle solved
    return True


def update_neighbour_domain(puzzle, row, column, num):
    #update the domain of the neighboring cells by removing the assigned value
    domain = get_domain(puzzle, row, column)
    domain.discard(num)


def restore_neighbour_domain(puzzle, updated_cells):
    for row, column in updated_cells:
        #restore the domain of the neighboring cells by adding the value back
        domain = get_domain(puzzle, row, column)
        domain.add(puzzle[row][column])
    

    
# function to get the domain of the current cell
def get_domain(board, row, col):
    domain = set(range(1, 10))

    #Remove numbers that already exist in the row and column
    for i in range(9):
        if board[row][i] != 0:
            domain.discard(board[row][i])
        if board[i][col] != 0:
            domain.discard(board[i][col])

    #Remove numbers that exist in 3x3 grid from the domain
    start_row = (row // 3) * 3
    start_col = (col // 3) * 3
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] != 0:
                domain.discard(board[i][j])

    return domain

puzzles = [
    # Puzzle 1
    [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 2, 0, 4, 0, 0, 0, 0, 8],
        [0, 0, 3, 0, 0, 0, 0, 7, 0],
        [0, 0, 0, 9, 0, 0, 0, 5, 0],
        [0, 0, 0, 0, 5, 0, 4, 0, 0],
        [0, 0, 9, 0, 0, 2, 0, 0, 0],
        [0, 0, 0, 0, 0, 5, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 6, 0],
        [0, 0, 1, 0, 0, 0, 7, 0, 0]
    ],
    # Puzzle 2
    [
        [0, 0, 0, 0, 0, 6, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 3],
        [0, 0, 0, 0, 9, 7, 1, 0, 0],
        [6, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 3, 0, 0, 0, 0],
        [0, 5, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 7, 2, 0, 6, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 0]
    ],  # Puzzle 3
    [
        [0, 0, 1, 2, 0, 9, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 9, 0],
        [0, 4, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 7, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [3, 0, 0, 0, 0, 0, 0, 0, 0]
    ], # Puzzle 4
    [
        [0, 0, 0, 2, 6, 0, 7, 0, 1],
        [6, 8, 0, 0, 7, 0, 0, 9, 0],
        [1, 9, 0, 0, 0, 4, 5, 0, 0],
        [8, 2, 0, 1, 0, 0, 0, 4, 0],
        [0, 0, 4, 6, 0, 2, 9, 0, 0],
        [0, 5, 0, 0, 0, 3, 0, 2, 8],
        [0, 0, 9, 3, 0, 0, 0, 7, 4],
        [0, 4, 0, 0, 5, 0, 0, 3, 6],
        [7, 0, 3, 0, 1, 8, 0, 0, 0]
    ],

    # Puzzle 5
    [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 3, 0, 0, 0, 0, 0, 0],
        [0, 7, 0, 0, 0, 0, 0, 5, 0],
        [0, 0, 6, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 5, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 4, 0, 0],
        [0, 0, 0, 0, 3, 0, 0, 0, 0],
        [9, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 2]
    ],

    # Puzzle 6
    [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 2, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 6, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 4, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ],# Puzzle 7
    [
        [1, 0, 0, 4, 8, 9, 0, 0, 6],
        [7, 3, 0, 0, 0, 0, 0, 4, 0],
        [0, 0, 0, 0, 0, 1, 2, 9, 5],
        [0, 0, 7, 1, 2, 0, 6, 0, 0],
        [5, 0, 0, 7, 0, 3, 0, 0, 8],
        [0, 0, 6, 0, 9, 5, 7, 0, 0],
        [9, 1, 4, 6, 0, 0, 0, 0, 0],
        [0, 2, 0, 0, 0, 0, 0, 3, 7],
        [8, 0, 0, 5, 1, 2, 0, 0, 4]
    ],

    # Puzzle 8
    [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 4, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 8, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 5, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 2, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 6, 0],
        [0, 0, 0, 0, 0, 7, 0, 0, 0]
    ],

    # Puzzle 9
    [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 3, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 2, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 5, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 7, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 6, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ],  # Puzzle 10
    [
        [0, 7, 0, 0, 0, 0, 0, 0, 4],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 3, 0, 0, 0, 2, 0, 0],
        [0, 0, 0, 0, 0, 4, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 8, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 6, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ],

    # Puzzle 11
    [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 4, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 7],
        [0, 0, 0, 0, 0, 0, 0, 0, 8],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 3, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 9, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 2, 0, 0, 0]
    ],

    # Puzzle 12
    [
        [0, 0, 0, 0, 0, 4, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 5],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 6, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 9, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 7, 0, 0, 0]
    ],  # Puzzle 13
    [
        [0, 0, 0, 0, 0, 0, 0, 0, 9],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 2, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 9, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 4, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 5, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [6, 0, 0, 0, 0, 0, 0, 0, 0]
    ],

    # Puzzle 14
    [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 3, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 7, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 6, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 5, 0, 0],
        [0, 0, 0, 0, 0, 9, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 8, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1]
    ],

    # Puzzle 15
    [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 2, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 6],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 5, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 8, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 3, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 4, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 7]
    ],  # Puzzle 16
    [
        [4, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 8, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 5, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 7, 0, 0],
        [0, 0, 0, 0, 2, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 6, 0],
        [0, 0, 0, 0, 0, 4, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 9],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ],

    # Puzzle 17
    [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [6, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 4, 7, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 9, 0, 0],
        [0, 0, 7, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 5, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 8, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 0, 0]
    ],

    # Puzzle 18
    [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 7, 0, 0, 0, 0],
        [5, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 9, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 3],
        [0, 0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 8, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 5],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ],  # Puzzle 19
    [
        [0, 0, 0, 0, 0, 0, 6, 0, 0],
        [0, 0, 0, 0, 2, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 7, 0],
        [0, 6, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 4, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 7, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 3, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [8, 0, 0, 0, 0, 0, 0, 0, 0]
    ],

    # Puzzle 20
    [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 3, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 7, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 9, 0, 0],
        [0, 0, 0, 0, 5, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 6, 0],
        [0, 0, 0, 0, 0, 4, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 8, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1]
    ]]


#solve and print solutions for each puzzle
for i, puzzle in enumerate(puzzles):
    print(f"Solution for Puzzle {i+1}:")
    
    # Start the timer
    start_time = time.time()

    if FC(puzzle):
        for row in puzzle:
            print(row)
    
    #time taken to solve each puzzle in milliseconds
    elapsed_time = (time.time() - start_time) *1000
    print(f"Time taken: {elapsed_time:.3f} milliseconds")
    print()





