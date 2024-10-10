import matplotlib.pyplot as plt
import numpy as np


class N_queen:

    def __init__(self, size):
        self.size = size
        self.board = np.zeros((size, size))
        self.solutions = []

    def is_safe(self, row, col, n):

        for i in range(row):
            if self.board[i][col] == 1:
                return False

        for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
            if self.board[i][j] == 1:
                return False

        for i, j in zip(range(row, -1, -1), range(col, n)):
            if self.board[i][j] == 1:
                return False

        return True

    def solve_n_queen(self, row=0):
        if row >= self.size:
            self.solutions.append(self.board.copy())
            return True

        for i in range(self.size):
            if self.is_safe(row, i, self.size):
                self.board[row][i] = 1
                self.solve_n_queen(row + 1)
                self.board[row][i] = 0

        return False

    def visualize_solution(self):
        for solution in self.solutions:
            chessboard = np.zeros((self.size, self.size))

            for i in range(self.size):
                for j in range(self.size):
                    if solution[i][j] == 1:
                        chessboard[i][j] = 1

            fig, ax = plt.subplots()
            ax.matshow(chessboard, cmap="gray")

            for i in range(self.size):
                for j in range(self.size):
                    if chessboard[i][j] == 1:
                        ax.text(
                            j,
                            i,
                            "Q",
                            va="center",
                            ha="center",
                            color="blue",
                            fontsize=20,
                        )

            plt.show()


n_queeen = N_queen(8)
n_queeen.solve_n_queen()
n_queeen.visualize_solution()
