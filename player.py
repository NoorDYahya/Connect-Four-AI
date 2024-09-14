import numpy as np
import pygame
import sys
import math
import random
from board import Board
from abc import ABC, abstractmethod
from threading import Timer

BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
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
    def get_move_count(self):
        return self.move_count
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
class minMaxPlayer(Player):


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


class QLearningPlayer(Player):
    reward = {'win': 1, 'lose': 0, 'draw': 0.5}
    def __init__(self, player_number, piece, color):
        super().__init__(player_number, piece, color)
        self.stateAction_values = {}  # Stores state-action values for Q-learning
        self.state_action_history = []  # To store (state, action) pairs for the current game
        self.alpha = 0.9   # Learning rate
        self.gamma = 0.95  # Discount factor
        self.q_init = 0.6  # Initial Q-table value

    def index_board(self, board):
        """Returns a string representation of the board to use as a unique index."""
        return ''.join(map(str, board.board.flatten()))

    def get_q_values(self, board_index, cols):
        """Returns the Q-values for the current board state, initializing if necessary."""
        if board_index not in self.stateAction_values:
            self.stateAction_values[board_index] = np.ones(cols) * self.q_init
        return self.stateAction_values[board_index]

    def is_valid_move(self, col, board):
        """Checks if a move in the given column is valid."""
        return 0 <= col < board.get_col() and board.is_valid_location(col)

    def find_best_move(self, board):
        """Finds the best move based on the Q-table."""
        board_index = self.index_board(board)
        q_values = self.get_q_values(board_index, board.get_col())
        # Pick the best valid move
        valid_moves = [(col, q_values[col]) for col in range(board.get_col()) if self.is_valid_move(col, board)]
        if not valid_moves:
            raise ValueError("No valid moves available")
        # Choose the move with the highest Q-value
        best_move = max(valid_moves, key=lambda x: x[1])[0]
        # Save state-action history for future Q-value updates
        self.state_action_history.append((board_index, best_move))
        return best_move

    def update_q_values(self, result, board):
        """Updates the Q-values based on the result of the game."""
        if result == 3:  # Draw
            reward = self.reward['draw']
        elif result == self.player_number:
            reward = self.reward['win']
        else:
            reward = self.reward['lose']

        # Update Q-values in reverse order of the move history
        next_max = None  # Keep track of the next max Q-value for updating
        for board_index, action in reversed(self.state_action_history):
            q_values = self.get_q_values(board_index, board.get_col())
            if next_max is None:
                q_values[action] = reward
            else:
                q_values[action] = (1 - self.alpha) * q_values[action] + self.alpha * (reward + self.gamma * next_max)

            next_max = np.max(q_values)  # Next max is the max Q-value from this state

    def reset(self):
        """Resets the player's state-action history for a new game."""
        self.state_action_history = []

    def reset_moveCount(self):
        self.move_count = 0

    def make_move(self, board, font, screen, not_over, end_game, col=None):
        """Executes a move for the Q-learning player."""
        pygame.time.wait(500)
        best_move = self.find_best_move(board)
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

        # Update Q-values based on the game result
        winner = board.winner_value()
        self.update_q_values(winner, board)
        self.reset()

    def train(self, train_iterations, board_rows, board_cols, player1, player2):
        """Trains the Q-learning player against itself."""
        for iteration in range(train_iterations):
            board = Board(board_rows, board_cols)
            player1.reset()
            player2.reset()
            current_player = player1 if random.choice([True, False]) else player2

            while board.winner_value() == 0:
                best_move = current_player.find_best_move(board)
                row = board.get_next_open_row(best_move)
                board.drop_piece(row, best_move, current_player.piece)
                current_player = player1 if current_player == player2 else player2

            result = board.winner_value()
            player1.update_q_values(result, board)
            player2.update_q_values(result, board)

        return player1, player2


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