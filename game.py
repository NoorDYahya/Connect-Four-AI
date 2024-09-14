import pygame
import sys
import random
import math
from board import Board
from player import HumanPlayer, minMaxPlayer, QLearningPlayer, RandomPlayer

ROWS = 6
COLS = 7
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
SQUARESIZE = 100
CIRCLE_RADIUS = int(SQUARESIZE/2 - 5)
PLAYER_TURN = 0
AI_TURN = 1
PLAYER_PIECE = 1
AI_PIECE = 2

class Game:
    def __init__(self, player1, player2):
        self.board = Board(ROWS, COLS)
        self.players = [player1, player2]
        self.turn = random.randint(PLAYER_TURN, AI_TURN)
        self.current_player = self.players[self.turn]
        self.game_over = False
        self.not_over = [True]
        self.draw = False
        pygame.init()
        self.width = COLS * SQUARESIZE
        self.height = (ROWS + 1) * SQUARESIZE
        self.circle_radius = int(SQUARESIZE / 2 - 5)
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.font = pygame.font.SysFont("monospace", 30)
        self.draw_board()
        pygame.display.update()

    def draw_board(self):
        self.board.draw(self.screen)

    def end_game(self):
        self.game_over = True

    def reset(self):
        self.board = Board(ROWS, COLS)
        self.turn = random.randint(PLAYER_TURN, AI_TURN)
        self.current_player = self.players[self.turn]
        self.game_over = False
        self.not_over = [True]
        self.draw_board()
        pygame.display.update()

    def run(self):
        winner = None  # Track the winner
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEMOTION and self.not_over[0]:
                    pygame.draw.rect(self.screen, BLACK, (0, 0, self.width, SQUARESIZE))
                    xpos = pygame.mouse.get_pos()[0]
                    if self.turn == PLAYER_TURN:
                        pygame.draw.circle(self.screen, RED, (xpos, int(SQUARESIZE / 2)), self.circle_radius)

                if event.type == pygame.MOUSEBUTTONDOWN and self.not_over[0]:
                    pygame.draw.rect(self.screen, BLACK, (0, 0, self.width, SQUARESIZE))
                    if isinstance(self.current_player, HumanPlayer):
                        xpos = event.pos[0]
                        col = int(xpos // SQUARESIZE)
                        self.current_player.make_move(self.board, self.font, self.screen, self.not_over, self.end_game, col)
                        self.draw_board()
                        self.turn = (self.turn + 1) % 2
                        self.current_player = self.players[self.turn]

                pygame.display.update()

            if isinstance(self.current_player, minMaxPlayer) and not self.game_over and self.not_over[0]:
                col, minimax_score = self.current_player.minimax(self.board, 5, -math.inf, math.inf, True)
                if self.board.is_valid_location(col):
                    self.current_player.make_move(self.board, self.font, self.screen, self.not_over, self.end_game, col)
                self.draw_board()
                self.turn = (self.turn + 1) % 2
                self.current_player = self.players[self.turn]

            if isinstance(self.current_player, QLearningPlayer) and not self.game_over and self.not_over[0]:
                best_move = self.current_player.find_best_move(self.board)
                if self.board.is_valid_location(best_move):
                    self.current_player.make_move(self.board, self.font, self.screen, self.not_over, self.end_game, best_move)
                self.draw_board()
                self.turn = (self.turn + 1) % 2
                self.current_player = self.players[self.turn]

            if isinstance(self.current_player, RandomPlayer) and not self.game_over and self.not_over[0]:
                self.current_player.make_move(self.board, self.font, self.screen, self.not_over, self.end_game)
                self.draw_board()
                self.turn = (self.turn + 1) % 2
                self.current_player = self.players[self.turn]

            # Check for game over and determine the winner
            # if not self.not_over[0]:
            #     if isinstance(self.current_player, QLearningPlayer):
            #         winner = self.current_player.player_number
            #     elif isinstance(self.players[(self.turn + 1) % 2], QLearningPlayer):
            #         winner = self.players[(self.turn + 1) % 2].player_number
            #     self.end_game()

            if not any(self.board.is_valid_location(col) for col in range(COLS)) and not self.game_over:
                pygame.draw.rect(self.screen, BLACK, (0, 0, self.width, SQUARESIZE))
                label = self.font.render("Draw!", True, (255, 255, 255))
                self.screen.blit(label, (40, 10))
                pygame.display.update()
                pygame.time.wait(3000)
                self.draw = True
                self.end_game()
        if self.draw:
             winner = 0
        if isinstance(self.current_player, QLearningPlayer):
            winner = self.current_player.player_number
        elif isinstance(self.current_player,RandomPlayer) or isinstance(self.current_player, minMaxPlayer):
            winner = self.players[(self.turn + 1) % 2].player_number
        elif isinstance(self.players[(self.turn + 1) % 2], QLearningPlayer):
            winner = self.players[(self.turn + 1) % 2].player_number
        return winner, self.current_player.get_move_count()  # Return winner and move count after the game


if __name__ == "__main__":
    pygame.init()
    total_moves_1 = 0
    total_moves_2 = 0
    player1_wins = 0
    player2_wins = 0
    total_games = 250
    # Instantiate Q-Learning players
    # q_learning_player1 = QLearningPlayer(1, 1, RED)
    # q_learning_player2 = QLearningPlayer(2, 2, YELLOW)
    # q1, q2 = q_learning_player1.train(1000, ROWS, COLS, q_learning_player1, q_learning_player2)

    for i in range(total_games):
        print(f"Starting Game {i + 1}")

        # q_learning_player1.reset_moveCount()
        # q_learning_player2.reset_moveCount()
        # player1 = q1
        # player2 = q2

        player1 = minMaxPlayer(1, 1, RED)
        # player2 = AIPlayer(2,2,YELLOW)

        # player1 = RandomPlayer(1,1,RED)
        player2 = RandomPlayer(2,2,YELLOW)

        # player1 = HumanPlayer(1,1,RED)
        # player2 = HumanPlayer(2,2,YELLOW)

        game = Game(player1, player2)
        winner, move_count = game.run()  # Capture the winner and move count
        tie_game  = 0
        # Track the winner and their move count
        # print(winner,move_count)
        if winner == 0 :
            tie_game +=1
        if winner == 1:
            total_moves_1 += move_count
            player1_wins += 1
        elif winner == 2:
            total_moves_2 += move_count
            player2_wins += 1

        # Reset the game state after each run
        game.reset()


    # Calculate and print statistics after 10 games
    avg_moves1 = total_moves_1 / total_games
    avg_moves2 = total_moves_2 / total_games

    win_percentage_player1 = (player1_wins / total_games) * 100
    win_percentage_player2 = (player2_wins / total_games) * 100
    print("**************")

    print(f"Number of Tie games: {tie_game}")
    print(f"player 1 avg moves: {avg_moves1}")
    print(f"Player 1 win percentage: {win_percentage_player1}%")
    print("**************")
    print(f"player 2 avg moves: {avg_moves2}")
    print(f"Player 2 win percentage: {win_percentage_player2}%")

    pygame.quit()