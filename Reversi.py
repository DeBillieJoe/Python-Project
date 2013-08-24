import random


WHITE_TILE = 'WHITE_TILE'
BLACK_TILE = 'BLACK_TILE'
EMPTY_SPACE = 'EMPTY_SPACE'
HEIGHT = 8
WIDTH = 8
DIRECTIONS = ((0, 1), (1, 1), (1, 0), (1, -1),
              (0, -1), (-1, -1), (-1, 0), (-1, 1))

CORNERS = ((0, 0), (WIDTH-1, 0), (0, HEIGHT-1), (WIDTH-1, HEIGHT-1))

FIRST_ROW = tuple((x, 0) for x in range(2, WIDTH-2))
FIRST_COLUMN = tuple((0, y) for y in range(2, HEIGHT-2))
LAST_ROW = tuple((x, HEIGHT-1) for x in range(2, WIDTH-2))
LAST_COLUMN = tuple((WIDTH-1, y) for y in range(2, HEIGHT-2))
EDGES = FIRST_ROW+FIRST_COLUMN+LAST_COLUMN+LAST_ROW

BAD_SECTORS = ((1, 0), (1, 1), (0, 1), (WIDTH-2, 0), (WIDTH-1, 1),
               (WIDTH-2, 1), (0, HEIGHT-2), (HEIGHT-1, 1), (HEIGHT-2, 1),
               (WIDTH-2, HEIGHT-1), (WIDTH-2, HEIGHT-2), (WIDTH-1, HEIGHT-2))

RISK_SECTORS = tuple((sector[0], sector[1]+1) for sector in FIRST_ROW) + \
    tuple((sector[0]+1, sector[1]) for sector in FIRST_COLUMN) + \
    tuple((sector[0], sector[1]-1) for sector in LAST_ROW) + \
    tuple((sector[0]-1, sector[1]) for sector in LAST_COLUMN)


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
        """Check if mouse position is on board."""
        return mousex >= 0 and mousex < WIDTH and \
            mousey >= 0 and mousey < HEIGHT

    def is_valid_move(self, mousex, mousey):
        """Check if the move is valid."""
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
    def __init__(self, tile, board):
        super().__init__(tile, board)
        self.difficulty = None
        self.difficulties = {'Easy': self.easy_move,
                             'Medium': self.medium_move,
                             'Hard': self.hard_move}

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty

    def hard_move(self):
        """Return the best move positon and list of tiles to flip."""
        valid_moves = self.get_valid_moves()
        corner_moves, edge_moves, bad_moves, risk_moves = [], [], [], []
        possible_moves = []
        if valid_moves:
            for move in valid_moves:
                if self.is_on_corner(move):
                    corner_moves.append(move)
                elif self.is_on_edge(move):
                    edge_moves.append(move)
                elif self.is_bad_sector(move):
                    bad_moves.append(move)
                elif self.is_risk_sector(move):
                    risk_moves.append(move)
                else:
                    possible_moves.append(move)

            if corner_moves:
                possible_moves = corner_moves
            elif edge_moves:
                possible_moves = edge_moves
            if not possible_moves:
                if risk_moves:
                    possible_moves = risk_moves
                elif bad_moves:
                    possible_moves = bad_moves

            best_score = 0
            best_move = None
            random.shuffle(possible_moves)
            for move in possible_moves:
                tiles_to_flip = self.is_valid_move(move[0], move[1])
                if len(tiles_to_flip) > best_score:
                    best_score = len(tiles_to_flip)
                    best_move = move

            return best_move, self.is_valid_move(best_move[0], best_move[1])

    def easy_move(self):
        """Return random possible move and list of tiles to flip."""
        valid_moves = self.get_valid_moves()
        move = None
        if valid_moves:
            random.shuffle(valid_moves)
            choice = random.choice(range(len(valid_moves)))
            move = valid_moves[choice]

            return move, self.is_valid_move(move[0], move[1])

    def medium_move(self):
        """Return good move and list of tiles to flip."""
        valid_moves = self.get_valid_moves()
        best_move = None
        best_score = 0
        if valid_moves:
            random.shuffle(valid_moves)
            for move in valid_moves:
                if self.is_on_corner(move):
                    return move, self.is_valid_move(move[0], move[1])

                score = len(self.is_valid_move(move[0], move[1]))
                if score > best_score:
                    best_score = score
                    best_move = move

            return best_move, self.is_valid_move(best_move[0], best_move[1])

    def make_move(self, other_player):
        if not self.difficulties[self.difficulty]():
            return False

        best_move = self.difficulties[self.difficulty]()
        x, y = best_move[0]
        tiles_to_flip = best_move[1]
        self.board.board[x][y] = self.tile

        for sector in tiles_to_flip:
            self.board.board[sector[0]][sector[1]] = self.tile

        self.score += 1+len(tiles_to_flip)
        other_player.score -= len(tiles_to_flip)
        return True

    def is_on_corner(self, sector):
        return (sector[0], sector[1]) in CORNERS

    def is_on_edge(self, sector):
        return (sector[0], sector[1]) in EDGES

    def is_bad_sector(self, sector):
        return (sector[0], sector[1]) in BAD_SECTORS

    def is_risk_sector(self, sector):
        return (sector[0], sector[1]) in RISK_SECTORS
