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
        self = Board()

        return self


class Player:

    def __init__(self, tile, board):
        self.tile = tile
        self.board = board
        self.score = 2

    def is_on_board(self, mousex, mousey):
        return mousex >= 0 and mousex < WIDTH and \
            mousey >= 0 and mousey < HEIGHT

    def is_valid_move(self, mousex, mousey):
        if self.is_on_board(mousex, mousey):
            if self.board.board[mousex][mousey] != EMPTY_SPACE:
                return False
        else:
            return False

        self.board.board[mousex][mousey] = self.tile

        if self.tile == WHITE_TILE:
            other_tile = BLACK_TILE
        else:
            other_tile = WHITE_TILE

        tiles_to_flip = []

        for direction in DIRECTIONS:
            x, y = mousex, mousey
            x += direction[0]
            y += direction[1]

            while self.is_on_board(x, y) and \
                    self.board.board[x][y] == other_tile:
                x += direction[0]
                y += direction[1]

                if not self.is_on_board(x, y):
                    continue

                if self.board.board[x][y] == self.tile:
                    while True:
                        x -= direction[0]
                        y -= direction[1]

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

    def make_move(self, mousex, mousey, other_player):
        tiles_to_flip = self.is_valid_move(mousex, mousey)

        if not tiles_to_flip:
            return False

        self.board.board[mousex][mousey] = self.tile
        for move in tiles_to_flip:
            self.board.board[move[0]][move[1]] = self.tile

        self.score += 1+len(tiles_to_flip)
        other_player.score -= len(tiles_to_flip)
        return True


class Computer(Player):
    def make_move(self, mousex, mousey, other_player):
        pass

    def is_on_corner(self, mousex, mousey):
        return (mousex, mousey) in [(0, 0), (WIDTH, 0),
                                    (0, HEIGHT), (WIDTH, HEIGHT)]

    def is_edge(self, mousex, mousey):
        pass
