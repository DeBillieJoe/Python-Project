import Reversi
import pygame
import sys
import time
import random
from pygame.locals import *

FPS = 10
WINDOWHEIGHT = 480
WINDOWWIDTH = 640
WIDTH = Reversi.WIDTH
HEIGHT = Reversi.HEIGHT
BLACK_TILE = Reversi.BLACK_TILE
WHITE_TILE = Reversi.WHITE_TILE
SPACE = 50
X_OFFSET = int((WINDOWWIDTH-(WIDTH*SPACE))/2)
Y_OFFSET = int((WINDOWHEIGHT-(HEIGHT*SPACE))/2)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BORDO = (128, 0, 0)
BLUE = (0, 0, 255)
DARK_GREEN = (0, 51, 0)
GREEN = (0, 145, 0)
ORANGE = (255, 165, 0)

pygame.init()
FONT = pygame.font.Font('freesansbold.ttf', 20)
BIGFONT = pygame.font.Font('freesansbold.ttf', 36)
HUGEFONT = pygame.font.Font('freesansbold.ttf', 72)

NEW_GAME = FONT.render('New Game', True, WHITE, BORDO)
NEW_GAME_BUTTON = NEW_GAME.get_rect()
NEW_GAME_BUTTON.topright = (WINDOWWIDTH-15, 15)

PLAY_AGAIN_TEXT = 'Do you want to play again?'
PLAY_AGAIN = BIGFONT.render(PLAY_AGAIN_TEXT, True, WHITE, DARK_GREEN)
PLAY_AGAIN_BUTTON = PLAY_AGAIN.get_rect()
PLAY_AGAIN_BUTTON.center = (int(WINDOWWIDTH/2), int(WINDOWHEIGHT/2)+50)

YES = BIGFONT.render('Yes', True, WHITE, DARK_GREEN)
YES_BUTTON = YES.get_rect()
YES_BUTTON.center = (int(WINDOWWIDTH/2)-60, int(WINDOWHEIGHT/2)+100)

NO = BIGFONT.render('No', True, WHITE, DARK_GREEN)
NO_BUTTON = NO.get_rect()
NO_BUTTON.center = (int(WINDOWWIDTH/2)+60, int(WINDOWHEIGHT/2)+100)

RAGE_QUIT = HUGEFONT.render('RAGE QUIT!!!', True, WHITE, BLACK)
RAGE_QUIT_SURFACE = RAGE_QUIT.get_rect()
RAGE_QUIT_SURFACE.center = (int(WINDOWWIDTH/2), int(WINDOWHEIGHT/2))

QUIT_MESSAGE = 'Do you really want to quit?'
WANNA_QUIT = BIGFONT.render(QUIT_MESSAGE, True, WHITE, DARK_GREEN)
WANNA_QUIT_BUTTON = WANNA_QUIT.get_rect()
WANNA_QUIT_BUTTON.center = (int(WINDOWWIDTH/2), int(WINDOWHEIGHT/2)-50)

ONE_PLAYER = BIGFONT.render('Player vs Computer', True, WHITE, BORDO)
ONE_PLAYER_BUTTON = ONE_PLAYER.get_rect()
ONE_PLAYER_BUTTON.center = (int(WINDOWWIDTH/2), int(WINDOWHEIGHT/2)-66)

TWO_PLAYER = BIGFONT.render('Player 1 vs Player 2', True, WHITE, BORDO)
TWO_PLAYER_BUTTON = TWO_PLAYER.get_rect()
TWO_PLAYER_BUTTON.center = (int(WINDOWWIDTH/2), int(WINDOWHEIGHT/2)+66)

EASY = BIGFONT.render('Easy', True, WHITE, BORDO)
EASY_BUTTON = EASY.get_rect()
EASY_BUTTON.center = (int(WINDOWWIDTH/2), int(WINDOWHEIGHT/2)-75)

MEDIUM = BIGFONT.render('Medium', True, WHITE, BORDO)
MEDIUM_BUTTON = MEDIUM.get_rect()
MEDIUM_BUTTON.center = (int(WINDOWWIDTH/2), int(WINDOWHEIGHT/2))

HARD = BIGFONT.render('Hard', True, WHITE, BORDO)
HARD_BUTTON = HARD.get_rect()
HARD_BUTTON.center = (int(WINDOWWIDTH/2), int(WINDOWHEIGHT/2)+75)


class Game:

    def __init__(self):
        self.board = Reversi.Board()
        self.clock = pygame.time.Clock()
        self.display = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
        self.BG = pygame.Surface(self.display.get_size())
        self.BG.fill(BORDO)

        self.END_BACKGROUND = pygame.Surface(self.display.get_size())
        self.END_BACKGROUND.fill(DARK_GREEN)

        pygame.display.set_caption('Reversi')
        self.players = 0
        self.player_one = None
        self.player_two = None
        self.turn = None

        while True:
            if self.run_game() is False:
                break

    def run_game(self):
        self.board = self.board.reset_board()
        self.turn = BLACK_TILE

        self.draw_board(self.board)
        self.choose_players()

        self.new_game()
        pygame.display.update()
        self.clock.tick(FPS)

        self.check_for_quit()
        player = None
        other_player = None
        while True:
            if self.player_one.tile == self.turn:
                player = self.player_one
                other_player = self.player_two
            elif self.player_two.tile == self.turn:
                player = self.player_two
                other_player = self.player_one

            if player.get_valid_moves() == []:
                break

            if isinstance(player, Reversi.Computer):
                self.draw_board(self.board)
                self.get_score()
                self.get_turn(self.turn)
                self.new_game()
                pygame.display.update()
                self.clock.tick(FPS)
                time.sleep(1)

                player.make_move(other_player)

            else:
                move = None
                while not move:
                    self.check_for_quit()

                    for event in pygame.event.get():
                        if event.type == MOUSEBUTTONUP:
                            mousex, mousey = event.pos
                            if NEW_GAME_BUTTON.collidepoint(mousex, mousey):
                                return True

                            move = self.clicked(mousex, mousey)
                            if move is not None and not \
                                    player.is_valid_move(move[0], move[1]):
                                move = None

                    self.draw_board(self.board)
                    self.get_score()
                    self.get_turn(self.turn)
                    self.new_game()
                    pygame.display.update()
                    self.clock.tick(FPS)

                player.make_move(move[0], move[1], other_player)

            if other_player.get_valid_moves() is not []:
                self.turn = other_player.tile

        self.draw_board(self.board)
        self.get_score()
        pygame.display.update()
        self.clock.tick(FPS)

        time.sleep(2)

        while True:
            self.display.blit(self.END_BACKGROUND, (0, 0))
            self.get_winner()
            self.display.blit(PLAY_AGAIN, PLAY_AGAIN_BUTTON)
            self.display.blit(YES, YES_BUTTON)
            self.display.blit(NO, NO_BUTTON)
            pygame.display.update()
            self.clock.tick(FPS)

            self.check_for_quit()
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONUP:
                    mousex, mousey = event.pos
                    if YES_BUTTON.collidepoint((mousex, mousey)):
                        return True
                    elif NO_BUTTON.collidepoint((mousex, mousey)):
                        return False

                pygame.display.update()
                self.clock.tick(FPS)

    def new_game(self):
        """Show the new game button."""
        self.display.blit(NEW_GAME, NEW_GAME_BUTTON)

    def get_score(self):
        """Show the score information."""
        if self.players == 1:
            if not isinstance(self.player_one, Reversi.Computer):
                text = 'Player: %s    Computer: %s'
            else:
                text = 'Computer: %s    Player: %s'
        else:
            if self.player_one.tile == BLACK_TILE:
                text = 'Player 1: %s    Player 2: %s'
            else:
                text = 'Player 2: %s    Player 1: %s'

        score = (str(self.player_one.score), str(self.player_two.score))
        score_board = FONT.render(text % score, True, WHITE)
        score_board_surface = score_board.get_rect()
        score_board_surface.bottomleft = (10, WINDOWHEIGHT-5)
        self.display.blit(score_board, score_board_surface)

    def get_turn(self, turn):
        """Show which player's turn it is."""
        text = None
        if self.players == 1:
            for player in [self.player_one, self.player_two]:
                if not isinstance(player, Reversi.Computer) and \
                        self.turn == player.tile:
                    text = "Player's turn!"
        else:
            if self.turn == self.player_one.tile:
                text = "Player 1's turn!"
            else:
                text = "Player 2's turn!"

        turn = FONT.render(text, True, WHITE)
        turn_surface = turn.get_rect()
        turn_surface.bottomleft = (280, WINDOWHEIGHT-5)
        self.display.blit(turn, turn_surface)

    def choose_players(self):
        """
        Let the user choose to play against the computer or a friend.
        Choose which player play first.
        """
        while True:
            self.check_for_quit()

            for event in pygame.event.get():
                if event.type == MOUSEBUTTONUP:
                    mouse = event.pos
                    choice = random.choice((0, 1))
                    rival = {0: (Reversi.Player(BLACK_TILE, self.board),
                                 Reversi.Computer(WHITE_TILE, self.board)),
                             1: (Reversi.Computer(BLACK_TILE, self.board),
                                 Reversi.Player(WHITE_TILE, self.board))}
                    rivals = {0: (Reversi.Player(BLACK_TILE, self.board),
                                  Reversi.Player(WHITE_TILE, self.board)),
                              1: (Reversi.Player(WHITE_TILE, self.board),
                                  Reversi.Player(BLACK_TILE, self.board))}
                    if ONE_PLAYER_BUTTON.collidepoint((mouse[0], mouse[1])):
                        self.player_one, self.player_two = rival[choice]
                        if isinstance(self.player_one, Reversi.Computer):
                            self.choose_difficulty(self.player_one)
                        else:
                            self.choose_difficulty(self.player_two)

                        self.players = 1
                        return
                    elif TWO_PLAYER_BUTTON.collidepoint((mouse[0], mouse[1])):
                        self.player_one, self.player_two = rivals[choice]
                        self.players = 2
                        return

            self.display.blit(ONE_PLAYER, ONE_PLAYER_BUTTON)
            self.display.blit(TWO_PLAYER, TWO_PLAYER_BUTTON)
            pygame.display.update()
            self.clock.tick(FPS)

    def choose_difficulty(self, computer):
        """
        Let the user to choose game's difficulty.
        """
        while True:
            self.check_for_quit()

            for event in pygame.event.get():
                if event.type == MOUSEBUTTONUP:
                    mouse = event.pos
                    if EASY_BUTTON.collidepoint((mouse[0], mouse[1])):
                        computer.set_difficulty('Easy')
                        return
                    elif MEDIUM_BUTTON.collidepoint((mouse[0], mouse[1])):
                        computer.set_difficulty('Medium')
                        return
                    elif HARD_BUTTON.collidepoint((mouse[0], mouse[1])):
                        computer.set_difficulty('Hard')
                        return

            self.draw_board(self.board)
            self.display.blit(EASY, EASY_BUTTON)
            self.display.blit(MEDIUM, MEDIUM_BUTTON)
            self.display.blit(HARD, HARD_BUTTON)
            pygame.display.update()
            self.clock.tick(FPS)

    def clicked(self, mousex, mousey):
        """Check if mouse click is on square."""
        for x in range(WIDTH):
            for y in range(HEIGHT):
                if mousex > x*SPACE+X_OFFSET and \
                   mousex < (x+1)*SPACE+X_OFFSET and \
                   mousey > y*SPACE+Y_OFFSET and \
                   mousey < (y+1)*SPACE+Y_OFFSET:
                    return (x, y)
        return None

    def draw_board(self, board):
        self.display.blit(self.BG, (0, 0))
        pygame.draw.rect(self.display, GREEN, (X_OFFSET, Y_OFFSET,
                         SPACE*WIDTH, SPACE*HEIGHT))

        for spot in [(x, x) for x in range(WIDTH + 1)]:
            left = ((spot[0]*SPACE)+X_OFFSET, Y_OFFSET)
            right = ((spot[0]*SPACE)+X_OFFSET, Y_OFFSET+(HEIGHT*SPACE))
            up = (X_OFFSET, (spot[1]*SPACE)+Y_OFFSET)
            down = (X_OFFSET+(WIDTH*SPACE), (spot[1] * SPACE) + Y_OFFSET)
            pygame.draw.line(self.display, BLACK, left, right)
            pygame.draw.line(self.display, BLACK, up, down)

        for x in range(WIDTH):
            for y in range(HEIGHT):
                centerx, centery = self.get_center(x, y)
                if board.board[x][y] in [BLACK_TILE, WHITE_TILE]:
                    if board.board[x][y] == WHITE_TILE:
                        tile_color = WHITE
                    else:
                        tile_color = BLACK

                    pygame.draw.circle(self.display, tile_color,
                                       (centerx, centery), int(SPACE/2)-4)

    def get_center(self, x, y):
        """Return the coordinates of the square's center."""
        return X_OFFSET + x*SPACE+int(SPACE/2), \
            Y_OFFSET + y*SPACE+int(SPACE/2)

    def rage_quit(self):
        rg_background = pygame.Surface(self.display.get_size())
        rg_background.fill(BLACK)

        while True:
            self.display.blit(rg_background, (0, 0))
            self.display.blit(RAGE_QUIT, RAGE_QUIT_SURFACE)
            pygame.display.update()
            self.clock.tick(FPS)
            time.sleep(0.5)
            pygame.quit()
            sys.exit()

    def check_for_quit(self):
        for event in pygame.event.get((QUIT, KEYUP)):
            if event.type == QUIT or \
                    (event.type == KEYUP and event.key == K_ESCAPE):
                while True:
                    self.display.blit(self.END_BACKGROUND, (0, 0))
                    self.display.blit(WANNA_QUIT, WANNA_QUIT_BUTTON)
                    self.display.blit(YES, YES_BUTTON)
                    self.display.blit(NO, NO_BUTTON)
                    pygame.display.update()
                    self.clock.tick(FPS)

                    for event in pygame.event.get():
                        if event.type == MOUSEBUTTONUP:
                            mousex, mousey = event.pos
                            if YES_BUTTON.collidepoint((mousex, mousey)):
                                pygame.quit()
                                sys.exit()
                            elif NO_BUTTON.collidepoint((mousex, mousey)):
                                self.display.blit(self.BG, (0, 0))
                                self.draw_board(self.board)
                                return True
            else:
                self.rage_quit()

    def get_winner(self):
        text = None
        if self.player_one.score == self.player_two.score:
            text = "It's a tie!"

        if self.players is 2:
            if self.player_one.score > self.player_two.score:
                score = (self.player_one.score, self.player_two.score)
                text = 'Player 1 won %d to %d!' % score
            else:
                score = (self.player_two.score, self.player_one.score)
                text = 'Player 2 won %d to %d' % score
        else:
            if self.player_one.score > self.player_two.score and not \
                isinstance(self.player_one, Reversi.Computer) or \
                    self.player_two.score > self.player_one.score and not \
                    isinstance(self.player_two, Reversi.Computer):
                score = (self.player_one.score, self.player_two.score)
                text = 'You won %d to %d' % score
            else:
                score = (self.player_two.score, self.player_one.score)
                text = 'You lost %d to %d' % score

        winner = BIGFONT.render(text, True, WHITE, DARK_GREEN)
        winner_button = winner.get_rect()
        winner_button.center = (int(WINDOWWIDTH/2), int(WINDOWHEIGHT/2)-50)

        self.display.blit(winner, winner_button)


def main():
    game = Game()

    return game


if __name__ == '__main__':
    main()
