import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors


class Sudoku:
    """This class generates, solves and Visualize sudoku puzzles."""

    def __init__(self, size=9):
        """Initilase a sudoku class with specified size."""
        self.size = size

    def is_valid(self, board, row, col, num):
        """Check if num can be placed at board[row][col]."""
        if num in board[row]:
            return False
        if num in board[:, col]:
            return False
        box_row_start = (row // 3) * 3
        box_col_start = (col // 3) * 3
        for i in range(3):
            for j in range(3):
                if board[box_row_start + i, box_col_start + j] == num:
                    return False
        return True

    def get_empty_cells(self, board):
        """Get a list of all empty cells in the Sudoku."""
        empty_cells = []
        for row in range(9):
            for col in range(9):
                if board[row, col] == 0:
                    empty_cells.append((row, col))
        return empty_cells

    def generate_sudoku(self):
        """Generate a Sudoku puzzle using backtracking."""
        board = np.zeros((9, 9), dtype=int)
        fig, ax, text_objs = self.visualize_sudoku_setup(board)
        self._fill_diagonal_boxes(board)
        self.solve_sudoku(board, fig, ax, text_objs, self.get_empty_cells(board))
        return board

    def generate_sudoku_puzzle(self, difficulty="easy"):
        """Generate a Sudoku puzzle with varying difficulty."""
        board = self.generate_sudoku()
        if difficulty == "easy":
            self._remove_cells(board, 30)
        elif difficulty == "medium":
            self._remove_cells(board, 40)
        elif difficulty == "hard":
            self._remove_cells(board, 50)
        return board

    def _remove_cells(self, board, num_cells):
        """Remove num_cells from the Sudoku board."""
        cells = np.random.permutation(81)
        for i in range(num_cells):
            row = cells[i] // 9
            col = cells[i] % 9
            board[row, col] = 0

    def _fill_diagonal_boxes(self, board):
        """Fill the diagonal 3x3 boxes of the Sudoku."""
        for i in range(0, 9, 3):
            self._fill_box(board, i, i)

    def _fill_box(self, board, row, col):
        """Fill a 3x3 box of the Sudoku."""
        nums = np.random.permutation(9) + 1
        for i in range(3):
            for j in range(3):
                if self.is_valid(board, row + i, col + j, nums[3 * i + j]):
                    board[row + i, col + j] = nums[3 * i + j]

    def solve_sudoku(self, board, fig, ax, text_objs, empty_cells):
        """Solve the Sudoku using backtracking and visualize the process."""
        if not empty_cells:
            return True

        row, col = empty_cells.pop()

        for num in range(1, 10):
            if self.is_valid(board, row, col, num):
                board[row, col] = num
                self.update_plot(board, text_objs)
                plt.pause(0.01)

                if self.solve_sudoku(board, fig, ax, text_objs, empty_cells):
                    return True

                board[row, col] = 0
                self.update_plot(board, text_objs)
                plt.pause(0.01)

        empty_cells.append((row, col))
        return False

    def update_plot(self, board, text_objs):
        """Update the text objects for the Sudoku board."""
        for i in range(9):
            for j in range(9):
                if board[i, j] != 0:
                    text_objs[i][j].set_text(str(board[i, j]))
                else:
                    text_objs[i][j].set_text("")  # Empty cell
        plt.draw()

    def visualize_sudoku_setup(self, board):
        """Initilaize setup of the Sudoku board visualization."""
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

        for i in range(9):
            ax.axhline(i - 0.5, color="black", lw=2 if i % 3 == 0 else 0.5)
            ax.axvline(i - 0.5, color="black", lw=2 if i % 3 == 0 else 0.5)

        text_objs = [[None for _ in range(9)] for _ in range(9)]
        for i in range(9):
            for j in range(9):
                text_objs[i][j] = ax.text(
                    j, i, "", va="center", ha="center", fontsize=16
                )

        plt.ion()
        plt.show()

        return fig, ax, text_objs


sudoku = Sudoku()
puzzle = sudoku.generate_sudoku_puzzle()
fig, ax, text_objs = sudoku.visualize_sudoku_setup(puzzle)
sudoku.solve_sudoku(puzzle, fig, ax, text_objs, sudoku.get_empty_cells(puzzle))
input("Press Enter to close...")
