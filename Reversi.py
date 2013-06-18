import random, sys, pygame, time, copy
from pygame.locals import *


WHITE_TILE = 'WHITE_TILE'
BLACK_TILE = 'BLACK_TILE'
EMPTY_SPACE = 'EMPTY_SPACE'
HEIGHT = 8
WIDTH = 8
DIRECTIONS = [(0, 1), (1, 1), (1, 0), (1, -1),
              (0, -1), (-1, -1), (-1, 0), (-1, 1)]


class Board:
    def __init__(self):
        self.board = [[EMPTY_SPACE]*HEIGHT for i in range(0, WIDTH)]
        self.board[3][3] = WHITE_TILE
        self.board[3][4] = BLACK_TILE
        self.board[4][3] = BLACK_TILE
        self.board[4][4] = WHITE_TILE

    def reset_board(self):
        self.board = Board().board


class PlayerMove:
    def __init__(self, player, board):
        self.player = player
        self.board = board

    def is_on_board(self, mousex, mousey):
        return mousex >= 0 and mousex < WIDTH and \
            mousey >= 0 and mousey < HEIGHT

    def is_valid_move(self, mousex, mousey):
        if self.is_on_board(mousex, mousey):
            if self.board.board[mousex][mousey] != EMPTY_SPACE:
                return False
        else:
            return False

        self.board.board[mousex][mousey] = self.player

        if self.player == WHITE_TILE:
            other_tile = BLACK_TILE
        else:
            other_tile = WHITE_TILE

        tiles_to_flip = []

        for directionx, directiony in DIRECTIONS:
            x, y = mousex, mousey
            x += directionx
            y += directiony

            if self.is_on_board(x, y) and self.board.board[x][y] == other_tile:
                x += directionx
                y += directiony
                if not self.is_on_board(x, y):
                    continue
                while self.board.board[x][y] == other_tile:
                    x += directionx
                    y += directiony
                    if not self.is_on_board(x, y):
                        break
                if not self.is_on_board(x, y):
                    continue
                if self.board.board[x][y] == self.player:
                    while True:
                        x -= directionx
                        y -= directiony
                        if x == mousex and y == mousey:
                            break
                        tiles_to_flip.append((x, y))

        self.board.board[mousex][mousey] = EMPTY_SPACE

        if len(tiles_to_flip) > 0:
            return tiles_to_flip

        return False

    def get_valid_moves(self):
        valid_moves = [(x, y) for x in range(0, WIDTH)
                       for y in range(0, HEIGHT) if self.is_valid_move(x, y)]

        return valid_moves
