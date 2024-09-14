import numpy as np
import pygame


# Constants
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
SQUARESIZE = 100
CIRCLE_RADIUS = int(SQUARESIZE/2 - 5)

# Board class handles the game board logic
class Board:
    def __init__(self,row,col):
        self.row = row
        self.col = col
        self.board = np.zeros((self.row, self.col),dtype=int)

    def create_board(self):
        self.board = np.zeros((self.row, self.col))
    def get_row(self):
        return self.row
    def get_col(self):
        return self.col
    def drop_piece(self, row, col, piece):
        self.board[row][col] = piece

    def is_valid_location(self, col):
        return self.board[0][col] == 0

    def get_next_open_row(self, col):
        for r in range(self.row-1, -1, -1):
            if self.board[r][col] == 0:
                return r

    def winning_move(self, piece):
        # Check horizontal locations
        for c in range(self.col-3):
            for r in range(self.row):
                if (self.board[r][c] == piece and self.board[r][c+1] == piece and
                    self.board[r][c+2] == piece and self.board[r][c+3] == piece):
                    return True
        # Check vertical locations
        for c in range(self.col):
            for r in range(self.row-3):
                if (self.board[r][c] == piece and self.board[r+1][c] == piece and
                    self.board[r+2][c] == piece and self.board[r+3][c] == piece):
                    return True
        # Check positively sloped diagonals
        for c in range(self.col-3):
            for r in range(3, self.row):
                if (self.board[r][c] == piece and self.board[r-1][c+1] == piece and
                    self.board[r-2][c+2] == piece and self.board[r-3][c+3] == piece):
                    return True
        # Check negatively sloped diagonals
        for c in range(3, self.col):
            for r in range(3, self.row):
                if (self.board[r][c] == piece and self.board[r-1][c-1] == piece and
                    self.board[r-2][c-2] == piece and self.board[r-3][c-3] == piece):
                    return True
        return False

    def winner_value(self):
        if self.winning_move(1):
            return 1  # Player 1 wins

        if self.winning_move(2):
            return 2  # Player 2 wins

        # Check if the board is full (i.e., a tie)
        if all(self.board[0][col] != 0 for col in range(self.col)):
            return 3  # Game is a tie

        # No winner, no tie, game is still ongoing
        return 0

    def get_valid_locations(self):
        return [col for col in range(self.col) if self.is_valid_location(col)]

    def is_full(self):
        return not any(self.is_valid_location(col) for col in range(self.col))

    def draw(self, screen):
        for c in range(self.col):
            for r in range(self.row):
                pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
                if self.board[r][c] == 0:
                    pygame.draw.circle(screen, WHITE, (int(c * SQUARESIZE + SQUARESIZE/2),
                                        int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE/2)), CIRCLE_RADIUS)
                elif self.board[r][c] == 1:
                    pygame.draw.circle(screen, RED, (int(c * SQUARESIZE + SQUARESIZE/2),
                                      int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE/2)), CIRCLE_RADIUS)
                else:
                    pygame.draw.circle(screen, YELLOW, (int(c * SQUARESIZE + SQUARESIZE/2),
                                         int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE/2)), CIRCLE_RADIUS)
        pygame.display.update()