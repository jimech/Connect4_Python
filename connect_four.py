# JIMENA CHINCHILLA
# this is a simple connect four game using Pygame library.
# it contains the game logic and GameUI
#the ConnectGame class defines methods, represents methods and functions to interact with it
# Game UI is responsible  for drawing board, handler user inputs and running game loop.

import random
import pygame
import sys

ROWS = 6
COLS = 7
HUMAN = 0
COMPUTER = 1
EMPTY = 0
HUMAN_TOKEN = 1
COMPUTER_TOKEN = 2

class ConnectGame:
    def __init__(self):
        self.board = [[EMPTY] * COLS for _ in range(ROWS)]

    def is_valid_move(self, col):
        return self.board[ROWS - 1][col] == EMPTY

    def drop(self, col, token):
        for row in range(ROWS):
            #find the lowest free space
            if self.board[row][col] == EMPTY:
                self.board[row][col] = token
                break

    def print_board(self): #print current state
        for row in reversed(self.board):
            print(row)

    def is_winner(self, token):
        #check horizontally
        for r in range(ROWS):
            for c in range(COLS - 3):
                if all(self.board[r][c+i] == token for i in range(4)):
                    return True
        # check vertically
        for c in range(COLS):
            for r in range(ROWS - 3):
                if all(self.board[r+i][c] == token for i in range(4)):
                    return True
        # check diagonally
        for r in range(ROWS - 3):
            for c in range(COLS - 3):
                if all(self.board[r+i][c+i] == token for i in range(4)):
                    return True

                if all(self.board[r+3-i][c+i] == token for i in range(4)):
                    return True

        return False

    #Check if the
    #game is over(win or tie)
    def game_over(self):
        return self.is_winner(HUMAN_TOKEN) or self.is_winner(COMPUTER_TOKEN) or len(self.valid_moves()) == 0

    def valid_moves(self):
        return [col for col in range(COLS) if self.is_valid_move(col)]


# IN this part, I took guidance from GITHUB: KeithGalli/  Connect4-Python/ Path connect4_with_ai.py, to be able to implement pygame
# I Follow a different structure.
# It defines classes for the game logic and
# UI separately, with each class encapsulating related functionality. ---> The game logic is handled by the
# i organized the code into classes, the UI handling is encapsulated within the "GameUI" class
class GameUI:
    def __init__(self):
        self.game = ConnectGame()
        self.square_size = 100
        self.width = COLS * self.square_size
        self.height = (ROWS + 1) * self.square_size
        self.radius = int(self.square_size / 2 - 5)
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.init()
        self.myfont = pygame.font.SysFont("Roboto", 75)

 #
    def draw_board(self):
        for c in range(COLS):
            for r in range(ROWS):
                pygame.draw.rect(self.screen, (0, 0, 255), (c * self.square_size, r * self.square_size + self.square_size, self.square_size, self.square_size))
                pygame.draw.circle(self.screen, (0, 0, 0), (int(c * self.square_size + self.square_size / 2), int(r * self.square_size + self.square_size + self.square_size / 2)), self.radius)

        for c in range(COLS):
            for r in range(ROWS):
                if self.game.board[r][c] == HUMAN_TOKEN:
                    pygame.draw.circle(self.screen, (255, 0, 0), (int(c * self.square_size + self.square_size / 2), self.height - int(r * self.square_size + self.square_size / 2)), self.radius)
                elif self.game.board[r][c] == COMPUTER_TOKEN:
                    pygame.draw.circle(self.screen, (255, 255, 0), (int(c * self.square_size + self.square_size / 2), self.height - int(r * self.square_size + self.square_size / 2)), self.radius)
        pygame.display.update()

    def run(self):
        turn = random.randint(HUMAN, COMPUTER)
        game_over = False
        self.draw_board()

        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

# # Show player's token when mouse moves
                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(self.screen, (0, 0, 0), (0, 0, self.width, self.square_size))
                    posx = event.pos[0]
                    if turn == HUMAN:
                        pygame.draw.circle(self.screen, (255, 0, 0), (posx, int(self.square_size / 2)), self.radius)
                    pygame.display.update()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.draw.rect(self.screen, (0, 0, 0), (0, 0, self.width, self.square_size))
                    posx = event.pos[0]
                    if turn == HUMAN:
                        col = int(posx / self.square_size)

                        if col in self.game.valid_moves():
                            self.game.drop(col, HUMAN_TOKEN)

                            if self.game.is_winner(HUMAN_TOKEN):
                                label = self.myfont.render("You are the winner!!", 1, (255, 0, 0))
                                self.screen.blit(label, (40, 10))
                                game_over = True

                            turn += 1
                            turn %= 2

                            self.game.print_board()
                            self.draw_board()

            if turn == COMPUTER and not game_over:
                col = random.choice(self.game.valid_moves())

                if col in self.game.valid_moves():
                    self.game.drop(col, COMPUTER_TOKEN)

                    if self.game.is_winner(COMPUTER_TOKEN):
                        label = self.myfont.render("The computer wins!!", 1, (255, 255, 0))
                        self.screen.blit(label, (40, 10))
                        game_over = True

                    self.game.print_board()
                    self.draw_board()

                    turn += 1
                    turn %= 2

            if game_over:
                pygame.time.wait(3000)

if __name__ == "__main__":
    GameUI().run()
