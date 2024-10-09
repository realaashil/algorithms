import time

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors

# Check if placing a number in a cell is valid


def is_valid(board, row, col, num):
    """Check if num can be placed at board[row][col]"""
    # Check row
    if num in board[row]:
        return False
    # Check column
    if num in board[:, col]:
        return False
    # Check 3x3 box
    box_row_start = (row // 3) * 3
    box_col_start = (col // 3) * 3
    for i in range(3):
        for j in range(3):
            if board[box_row_start + i, box_col_start + j] == num:
                return False
    return True


# Collect empty cells beforehand for efficient backtracking


def get_empty_cells(board):
    """Get a list of all empty cells in the Sudoku"""
    empty_cells = []
    for row in range(9):
        for col in range(9):
            if board[row, col] == 0:
                empty_cells.append((row, col))
    return empty_cells


# Backtracking function to solve the Sudoku


def solve_sudoku(board, fig, ax, text_objs, empty_cells):
    """Solve the Sudoku using backtracking and update the figure"""
    if not empty_cells:
        return True  # All cells filled; solution found!

    # Get the next empty cell
    row, col = empty_cells.pop()

    # Try numbers 1-9
    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row, col] = num  # Tentative assignment
            update_plot(board, ax, text_objs)  # Update the plot
            plt.pause(0.01)  # Shorter pause for faster visualization

            if solve_sudoku(board, fig, ax, text_objs, empty_cells):
                return True  # Success, stop further search

            board[row, col] = 0  # Reset on backtrack
            update_plot(board, ax, text_objs)
            plt.pause(0.01)

    empty_cells.append((row, col))  # Backtrack, restore the empty cell
    return False  # Trigger backtracking


# Update the plot instead of redrawing it


def update_plot(board, ax, text_objs):
    """Update the text objects for the Sudoku board"""
    for i in range(9):
        for j in range(9):
            if board[i, j] != 0:
                text_objs[i][j].set_text(str(board[i, j]))  # Update cell value
            else:
                text_objs[i][j].set_text("")  # Empty cell
    plt.draw()


# Visualization function for the Sudoku board (initial setup)


def visualize_sudoku_setup(board):
    """Initial setup of the Sudoku board visualization"""
    cmap = colors.ListedColormap(
        [
            "white",
            "lightblue",
            "lightgreen",
            "yellow",
            "orange",
            "pink",
            "lightcoral",
            "lightgrey",
            "wheat",
            "lavender",
        ]
    )
    bounds = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # Bounds for numbers 0-9
    norm = colors.BoundaryNorm(bounds, cmap.N)

    fig, ax = plt.subplots()
    ax.imshow(board, cmap=cmap, norm=norm)

    # Draw gridlines
    for i in range(9):
        ax.axhline(i - 0.5, color="black", lw=2 if i % 3 == 0 else 0.5)
        ax.axvline(i - 0.5, color="black", lw=2 if i % 3 == 0 else 0.5)

    # Set up text objects for updating the board
    text_objs = [[None for _ in range(9)] for _ in range(9)]
    for i in range(9):
        for j in range(9):
            text_objs[i][j] = ax.text(j, i, "", va="center", ha="center", fontsize=16)

    plt.ion()  # Turn on interactive mode
    plt.show()

    return fig, ax, text_objs


# Example Sudoku puzzle
sudoku_board = np.array(
    [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]
)

# Initialize and run the solver with visualization
fig, ax, text_objs = visualize_sudoku_setup(sudoku_board)
empty_cells = get_empty_cells(sudoku_board)
solve_sudoku(sudoku_board, fig, ax, text_objs, empty_cells)

input("Press Enter to close...")  # Wait for user input before closing the plot
