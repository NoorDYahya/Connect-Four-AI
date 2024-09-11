
import pygame
import sys
import math
import random
from board import Board
from player import HumanPlayer,AIPlayer,RandomPlayer

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
        self.board = Board(ROWS,COLS)
        self.players = [player1, player2]
        self.turn = random.randint(PLAYER_TURN,AI_TURN)
        self.current_player = self.players[self.turn]
        self.game_over = False
        self.not_over = [True]
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

    def run(self):

        while not self.game_over:

            # for every player event
            for event in pygame.event.get():

                # if player clses the window
                if event.type == pygame.QUIT:
                    sys.exit()

                # if player moves the mouse, their piece moves at the top of the screen
                if event.type == pygame.MOUSEMOTION and self.not_over[0]:
                    pygame.draw.rect(self.screen, BLACK, (0, 0, self.width, SQUARESIZE))
                    xpos = pygame.mouse.get_pos()[0]
                    if self.turn == PLAYER_TURN:
                        pygame.draw.circle(self.screen, RED, (xpos, int(SQUARESIZE / 2)), self.circle_radius)

                # if player clicks the button, we drop their piece down
                if event.type == pygame.MOUSEBUTTONDOWN and self.not_over[0]:
                    pygame.draw.rect(self.screen, BLACK, (0, 0, self.width, SQUARESIZE))

                    # ask for player 1 inupt
                    if isinstance(self.current_player,HumanPlayer):

                        # we assume players will use correct input
                        xpos = event.pos[0]
                        col = int(math.floor(xpos / SQUARESIZE))

                        self.current_player.make_move(self.board,self.font,self.screen,self.not_over,self.end_game,col)

                        self.draw_board()

                        # increment turn by 1
                        self.turn += 1

                        # this will alternate between 0 and 1 withe very turn
                        self.turn = self.turn % 2
                        self.current_player = self.players[self.turn]

                pygame.display.update()

            # if its the AI's turn
            if isinstance(self.current_player,AIPlayer) and not self.game_over and self.not_over[0]:

                col, minimax_score = self.current_player.minimax(self.board,5, -math.inf, math.inf, True)

                if self.board.is_valid_location( col):
                    self.current_player.make_move(self.board,self.font,self.screen,self.not_over,self.end_game,col)

                self.draw_board()
                self.turn += 1
                # this will alternate between 0 and 1 withe very turn
                self.turn = self.turn % 2
                self.current_player = self.players[self.turn]

            if isinstance(self.current_player, RandomPlayer) and not self.game_over and self.not_over[0]:
                # Randomly select a column to drop the piece in

                    self.current_player.make_move(self.board, self.font, self.screen, self.not_over, self.end_game, 0)
                    self.draw_board()

                    # Alternate the turn
                    self.turn = (self.turn + 1) % 2
                    self.current_player = self.players[self.turn]

            if not any(self.board.is_valid_location(col) for col in range(COLS)) and not self.game_over:
                pygame.draw.rect(self.screen, BLACK, (0, 0, self.width, SQUARESIZE))
                label = self.font.render("Draw!", True, (255, 255, 255))
                self.screen.blit(label, (40, 10))
                pygame.display.update()
                pygame.time.wait(3000)
                self.end_game()

def get_valid_locations(self,board):
        valid_locations = []

        for column in range(COLS):
            if board.is_valid_location(board, column):
                valid_locations.append(column)

        return valid_locations



if __name__ == "__main__":
    player1 = AIPlayer(1,1,RED)
    player2 = AIPlayer(2,2,YELLOW)
    # player1 = RandomPlayer(1,1,RED)
    # player2 = RandomPlayer(2,2,YELLOW)
    player1 = HumanPlayer(1,1,RED)
    player2 = HumanPlayer(2,2,YELLOW)
    game = Game(player1, player2)
    game.run()