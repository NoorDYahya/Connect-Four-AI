import numpy as np
import pygame
import sys
import math
import random
from board import Board
from abc import ABC, abstractmethod
from threading import Timer

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
SQUARESIZE = 100
CIRCLE_RADIUS = int(SQUARESIZE/2 - 5)
# Abstract Player class
class Player(ABC):
    def __init__(self, player_number, piece, color):
        self.player_number = player_number
        self.piece = piece
        self.color = color
        self.move_count = 0
    def get_piece(self):
        return self.piece
    def get_color(self):
        return self.color

    def increment_move_count(self):
        self.move_count += 1
    @abstractmethod
    def make_move(self, board ,font,screen,not_over,end_game,col):
      pass


# HumanPlayer class for human interactions
class HumanPlayer(Player):

    def make_move(self, board ,font,screen,not_over,end_game,col):
        if board.is_valid_location(col):
            row = board.get_next_open_row(col)
            board.drop_piece(row, col, self.piece)
            self.increment_move_count()
            if board.winning_move(self.piece):
                print(f"PLAYER {self.player_number} WINS! with {self.move_count} moves!")
                label = font.render(f"PLAYER {self.player_number} WINS!\n Takes {self.move_count} moves!", 1, self.color)
                screen.blit(label, (40, 10))
                not_over[0] = False
                t = Timer(3.0, end_game)
                t.start()


# AIPlayer class for AI moves using minmax strategy with alpha-beta pruning
class AIPlayer(Player):


    def evaluate_window(self, window, piece):
        score = 0
        opp_piece = 1 if piece == 2 else 2

        if window.count(piece) == 4:
            score += 100
        elif window.count(piece) == 3 and window.count(0) == 1:
            score += 5
        elif window.count(piece) == 2 and window.count(0) == 2:
            score += 2

        if window.count(opp_piece) == 3 and window.count(0) == 1:
            score -= 4

        return score

    def score_position(self, board, piece):
        score = 0
        # Score center column
        center_array = [int(i) for i in list(board.board[:, board.get_col()//2])]
        center_count = center_array.count(piece)
        score += center_count * 6

        # Score Horizontal
        for r in range(board.get_row()):
            row_array = [int(i) for i in list(board.board[r, :])]
            for c in range(board.get_col()-3):
                window = row_array[c:c+4]
                score += self.evaluate_window(window, piece)

        # Score Vertical
        for c in range(board.get_col()):
            col_array = [int(i) for i in list(board.board[:, c])]
            for r in range(board.get_row()-3):
                window = col_array[r:r+4]
                score += self.evaluate_window(window, piece)

        # Score positive sloped diagonal
        for r in range(board.get_row()-3):
            for c in range(board.get_col()-3):
                window = [board.board[r+i][c+i] for i in range(4)]
                score += self.evaluate_window(window, piece)

        # Score negative sloped diagonal
        for r in range(board.get_row()-3):
            for c in range(board.get_col()-3):
                window = [board.board[r+3-i][c+i] for i in range(4)]
                score += self.evaluate_window(window, piece)

        return score

    def is_terminal_node(self, board):
        return (board.winning_move(1) or board.winning_move(2) or board.is_full())

    def minimax(self, board, depth, alpha, beta, maximizingPlayer):
        # valid_locations = board.get_valid_locations()
        # is_terminal = self.is_terminal_node(board)
        # if depth == 0 or is_terminal:
        #     if is_terminal:
        #         if board.winning_move(self.piece):
        #             return (None, 100000000000000)
        #         elif board.winning_move(1 if self.piece == 2 else 2):
        #             return (None, -10000000000000)
        #         else:  # Game is over, no more valid moves
        #             return (None, 0)
        #     else:  # Depth is zero
        #         return (None, self.score_position(board, self.piece))
        # if maximizingPlayer:
        #     value = -math.inf
        #     best_col = random.choice(valid_locations)
        #     for col in valid_locations:
        #         row = board.get_next_open_row(col)
        #         b_copy = Board(board.get_row(),board.get_col())
        #         b_copy.board = np.copy(board.board)
        #         b_copy.drop_piece(row, col, self.piece)
        #         new_score = self.minimax(b_copy, depth-1, alpha, beta, False)[1]
        #         if new_score > value:
        #             value = new_score
        #             best_col = col
        #         alpha = max(alpha, value)
        #         if alpha >= beta:
        #             break
        #     return best_col, value
        # else:  # Minimizing player
        #     value = math.inf
        #     best_col = random.choice(valid_locations)
        #     opp_piece = 1 if self.piece == 2 else 2
        #     for col in valid_locations:
        #         row = board.get_next_open_row(col)
        #         b_copy = Board(board.get_row(),board.get_col())
        #         b_copy.board = np.copy(board.board)
        #         b_copy.drop_piece(row, col, opp_piece)
        #         new_score = self.minimax(b_copy, depth-1, alpha, beta, True)[1]
        #         if new_score < value:
        #             value = new_score
        #             best_col = col
        #         beta = min(beta, value)
        #         if alpha >= beta:
        #             break
        #     return best_col, value

            valid_locations = board.get_valid_locations()
            is_terminal = self.is_terminal_node(board)

            # Check if the node is terminal or depth limit is reached
            if depth == 0 or is_terminal:
                if is_terminal:
                    if board.winning_move(self.piece):
                        return (None, 100000000000000)  # Win
                    elif board.winning_move(1 if self.piece == 2 else 2):
                        return (None, -10000000000000)  # Loss
                    else:
                        return (None, 0)  # Draw
                else:
                    return (None, self.score_position(board, self.piece))

            if maximizingPlayer:
                value = -math.inf
                best_col = random.choice(valid_locations)
                for col in sorted(valid_locations, key=lambda x: self.heuristic(board, x, self.piece),
                                  reverse=True):  # Sort moves
                    row = board.get_next_open_row(col)
                    b_copy = Board(board.get_row(), board.get_col())
                    b_copy.board = np.copy(board.board)
                    b_copy.drop_piece(row, col, self.piece)

                    new_score = self.minimax(b_copy, depth - 1, alpha, beta, False)[1]
                    if new_score > value:
                        value = new_score
                        best_col = col
                    alpha = max(alpha, value)
                    if alpha >= beta:
                        break  # Alpha-beta pruning
                return best_col, value
            else:  # Minimizing player
                value = math.inf
                best_col = random.choice(valid_locations)
                opp_piece = 1 if self.piece == 2 else 2
                for col in sorted(valid_locations, key=lambda x: self.heuristic(board, x, opp_piece)):  # Sort moves
                    row = board.get_next_open_row(col)
                    b_copy = Board(board.get_row(), board.get_col())
                    b_copy.board = np.copy(board.board)
                    b_copy.drop_piece(row, col, opp_piece)

                    new_score = self.minimax(b_copy, depth - 1, alpha, beta, True)[1]
                    if new_score < value:
                        value = new_score
                        best_col = col
                    beta = min(beta, value)
                    if alpha >= beta:
                        break  # Alpha-beta pruning
                return best_col, value

    def heuristic(self, board, col, piece):
        # Copy the board and simulate the move by dropping a piece in the column
        row = board.get_next_open_row(col)
        board_copy = Board(board.get_row(), board.get_col())
        board_copy.board = np.copy(board.board)
        board_copy.drop_piece(row, col, piece)

        # Evaluate the board after the move is made
        return self.score_position(board_copy, piece)

    def make_move(self, board ,font,screen,not_over,end_game,col):

            pygame.time.wait(500)
            row = board.get_next_open_row(col)
            board.drop_piece(row, col, self.piece)
            self.increment_move_count()
            if board.winning_move(self.piece):
                print(f"PLAYER {self.player_number } WINS! with {self.move_count} moves!")
                label = font.render(f"PLAYER {self.player_number} WINS!\n Takes {self.move_count} moves!", 1, self.color)
                screen.blit(label, (40, 10))
                not_over[0] = False
                t = Timer(3.0, end_game)
                t.start()

# Q-learning constants

WIN_VALUE = 1.0
LOSS_VALUE = 0.0
TIED_VALUE = 0.5
alpha = 0.9  # learning rate
gamma = 0.95  # discount factor
q_init = 0.6  # init q table
import random
import numpy as np

class QLearningPlayer(Player):
    def __init__(self, player_number, piece, color):
        super().__init__(player_number, piece, color)
        self.QTable = {}
        self.history = []

    def indexBoard(self, board):
        """Returns a unique string representation of the board for indexing."""
        rows = board.get_row()
        cols = board.get_col()
        return ''.join(str(board.board[i][j]) for i in range(rows) for j in range(cols))

    def getQValue(self, board_index, cols):
        """Retrieves or initializes the Q-values for a given board state."""
        if board_index not in self.QTable:
            self.QTable[board_index] = q_init * np.ones((cols))
        return self.QTable[board_index]

    def findBestMove(self, board):
        """Finds the best move using the current Q-table and updates the history."""
        board_index = self.indexBoard(board)
        qValue = self.getQValue(board_index, board.get_col())
        while True:
            maxIndex = np.argmax(qValue)  # Get the index of the maximum Q-value
            if self.checkPosAvaliable(maxIndex, board):
                break
            else:
                qValue[maxIndex] = -1.0  # Mark as invalid
        self.history.append((board_index, maxIndex))
        return maxIndex

    def checkPosAvaliable(self, col, board):
        """Checks if a position in the board is available."""
        return 0 <= col < board.get_col() and board.board[0][col] == 0

    def finalResult(self, winner, board):
        """Updates Q-values after the game ends based on the result."""
        if winner == 3:
            final_value = TIED_VALUE
        elif winner == self.player_number:
            final_value = WIN_VALUE
        else:
            final_value = LOSS_VALUE

        self.history.reverse()
        next_max = -1.0  # For tracking the next max Q-value
        for board_index, action in self.history:
            # Retrieve or initialize the Q-values for this board state using board.get_col()
            qValue = self.getQValue(board_index, board.get_col())
            if next_max < 0:  # First loop
                qValue[action] = final_value
            else:
                qValue[action] = qValue[action] * (1.0 - alpha) + alpha * gamma * next_max

            next_max = qValue.max()
            self.QTable[board_index] = qValue

    def newGame(self):
        """Resets the history for a new game."""
        self.history = []

    def make_move(self, board, font, screen, not_over, end_game, col=None):
        pygame.time.wait(500)
        best_move = self.findBestMove(board)
        row = board.get_next_open_row(best_move)
        board.drop_piece(row, best_move, self.piece)
        self.increment_move_count()

        if board.winning_move(self.piece):
            print(f"PLAYER Q-learning {self.player_number} WINS! with {self.move_count} moves!")
            label = font.render(f"PLAYER {self.player_number} WINS!\n Takes {self.move_count} moves!", 1, self.color)
            screen.blit(label, (40, 10))
            not_over[0] = False
            t = Timer(3.0, end_game)
            t.start()

        winner = board.winner_value()  # Use winner_value to check the game state
        self.finalResult(winner, board)  # Pass the board object as an argument
        self.newGame()

    def train(self, trainNum, board_rows, board_cols, playerQ1, playerQ2):
        """Train the Q-learning player."""
        cnt = 0
        while cnt < trainNum:
            cnt += 1
            Player1First = random.choice([True, False])
            board = Board(board_rows, board_cols)
            playerQ1.newGame()
            playerQ2.newGame()

            while board.winner_value() == 0:  # Use winner_value to check the game state
                # First Player
                playerQ = playerQ1 if Player1First else playerQ2
                y1 = playerQ.findBestMove(board)
                row = board.get_next_open_row(y1)
                board.drop_piece(row, y1, 1 if Player1First else 2)

                if board.winner_value() != 0:
                    playerQ1.finalResult(board.winner_value(), board)
                    playerQ2.finalResult(board.winner_value(), board)
                    break
                else:
                    # Second Player
                    playerQ = playerQ2 if Player1First else playerQ1
                    y2 = playerQ.findBestMove(board)
                    row = board.get_next_open_row(y2)
                    board.drop_piece(row, y2, 2 if Player1First else 1)

                    if board.winner_value() != 0:
                        playerQ1.finalResult(board.winner_value(), board)
                        playerQ2.finalResult(board.winner_value(), board)
                        break
        return playerQ1, playerQ2



# random player
class RandomPlayer(Player):
    def make_move(self, board, font, screen, not_over, end_game, col=0):
        valid_locations = board.get_valid_locations()
        if valid_locations:
            col = random.choice(valid_locations)  # Randomly select a valid column
            pygame.time.wait(500)
            row = board.get_next_open_row(col)
            board.drop_piece(row, col, self.piece)
            self.increment_move_count()
            if board.winning_move(self.piece):
                print(f"PLAYER {self.player_number} WINS! with {self.move_count} moves! ")
                label = font.render(f"PLAYER {self.player_number} WINS!\n Takes {self.move_count} moves!", 1, self.color)
                screen.blit(label, (40, 10))
                not_over[0] = False
                t = Timer(3.0, end_game)
                t.start()