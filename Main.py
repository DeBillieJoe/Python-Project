import Reversi
import pygame
import sys
from pygame.locals import *

FPS = 10
WINDOWHEIGHT = 480
WINDOWWIDTH = 640
WIDTH = Reversi.WIDTH
HEIGHT = Reversi.HEIGHT
BLACK_TILE = Reversi.BLACK_TILE
WHITE_TILE = Reversi.WHITE_TILE
SPACE = 50
XMARGIN = int((WINDOWWIDTH-(WIDTH*SPACE))/2)
YMARGIN = int((WINDOWHEIGHT-(HEIGHT*SPACE))/2)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 1000)


pygame.init()
FONT = pygame.font.Font('freesansbold.ttf', 16)
BIGFONT = pygame.font.Font('freesansbold.ttf', 32)


class Game:
    def __init__(self, b_image, bg_image):
        self.board = Reversi.Board()
        self.clock = pygame.time.Clock()
        self.display = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
        pygame.display.set_caption('Reversi')

        self.b_image = pygame.image.load(b_image)
        self.b_image = pygame.transform.smoothscale(self.b_image, (WIDTH*SPACE, HEIGHT*SPACE))
        b_image_rect = self.b_image.get_rect()
        b_image_rect.topleft = (XMARGIN, YMARGIN)
        self.bg_image = pygame.image.load(bg_image)
        self.bg_image = pygame.transform.smoothscale(self.bg_image, (WINDOWWIDTH, WINDOWHEIGHT))
        self.bg_image.blit(self.b_image, b_image_rect)

        while True:
            if self.run_game() is False:
                break

    def run_game(self):
        main_board = self.board
        main_board.reset_board()

        self.draw_board(main_board)

        newGameSurf = FONT.render('New Game', True, WHITE, RED)
        newGameRect = newGameSurf.get_rect()
        newGameRect.topright = (WINDOWWIDTH-8, 10)

        while True:
            self.draw_board(main_board)
            #drawInfo(boardToDraw, playerTile, computerTile, turn)

            # Draw the "New Game" and "Hints" buttons.
            self.display.blit(newGameSurf, newGameRect)
            #DISPLAYSURF.blit(hintsSurf, hintsRect)
            self.check_for_quit()
            self.clock.tick(FPS)
            pygame.display.update()

    def draw_board(self, board):
        self.display.blit(self.bg_image, self.bg_image.get_rect())

        for spot in [(x, x) for x in range(WIDTH + 1)]:
            left = [(spot[0]*SPACE)+XMARGIN, YMARGIN]
            right = [(spot[0]*SPACE)+XMARGIN, YMARGIN+(HEIGHT*SPACE)]
            up = [XMARGIN, (spot[1]*SPACE)+YMARGIN]
            down = [XMARGIN+(WIDTH*SPACE), (spot[1] * SPACE) + YMARGIN]
            pygame.draw.line(self.display, BLACK, (left[0], left[1]), (right[0], right[1]))
            pygame.draw.line(self.display, BLACK, (up[0], up[1]), (down[0], down[1]))

        for x in range(WIDTH):
            for y in range(HEIGHT):
                centerx, centery = self.board_to_pixel_coord(x, y)
                if board.board[x][y] in [BLACK_TILE, WHITE_TILE]:
                    if board.board[x][y] == WHITE_TILE:
                        tile_color = WHITE
                    else:
                        tile_color = BLACK

                    pygame.draw.circle(self.display, tile_color, (centerx, centery), int(SPACE/2)-4)

    def board_to_pixel_coord(self, x, y):
        return XMARGIN + x*SPACE+int(SPACE/2), \
            YMARGIN + y*SPACE+int(SPACE/2)

    def check_for_quit(self):
        for event in pygame.event.get((QUIT, KEYUP)):
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                text = 'Do you really want to quit?'
                text_surf = BIGFONT.render(text, True, WHITE, RED)
                text_rect = text_surf.get_rect()
                text_rect.center = (int(WINDOWWIDTH/2), int(WINDOWHEIGHT/2)+50)

                yes_surf = BIGFONT.render('Yes', True, WHITE, RED)
                yes_rect = yes_surf.get_rect()
                yes_rect.center = (int(WINDOWWIDTH/2)-60, int(WINDOWHEIGHT/2)+90)

                no_surf = BIGFONT.render('No', True, WHITE, RED)
                no_rect = no_surf.get_rect()
                no_rect.center = (int(WINDOWWIDTH/2)+60, int(WINDOWHEIGHT/2)+90)

                while True:
                    self.check_for_quit()
                    for event in pygame.event.get():
                        if event.type == MOUSEBUTTONUP:
                            mousex, mousey = event.pos
                            if yes_rect.collidepoint((mousex, mousey)):
                                pygame.quit()
                                sys.exit()
                            elif no_rect.collidepoint((mousex, mousey)):
                                return True

                    self.display.blit(text_surf, text_rect)
                    self.display.blit(yes_surf, yes_rect)
                    self.display.blit(no_surf, no_rect)
                    pygame.display.update()
                    self.clock.tick(FPS)


def main():
    game = Game('board.jpg', 'background.jpg')

    return game


if __name__ == '__main__':
    main()
