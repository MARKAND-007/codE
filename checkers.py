import pygame
import sys

# -----------------------------
# CONFIG
# -----------------------------

WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# Colors
WHITE = (240, 217, 181)
BROWN = (181, 136, 99)
RED = (220, 20, 60)
BLACK = (30, 30, 30)
BLUE = (50, 150, 255)
GOLD = (255, 215, 0)
GREEN = (0, 255, 0)

pygame.init()
FONT = pygame.font.SysFont("arial", 28)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Checkers")


# -----------------------------
# PIECE CLASS
# -----------------------------

class Piece:
    PADDING = 15
    OUTLINE = 3

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False

    def make_king(self):
        self.king = True

    def move(self, row, col):
        self.row = row
        self.col = col

    def draw(self, win):
        x = self.col * SQUARE_SIZE + SQUARE_SIZE // 2
        y = self.row * SQUARE_SIZE + SQUARE_SIZE // 2
        radius = SQUARE_SIZE // 2 - self.PADDING

        pygame.draw.circle(win, BLUE, (x, y), radius + self.OUTLINE)
        pygame.draw.circle(win, self.color, (x, y), radius)

        if self.king:
            pygame.draw.circle(win, GOLD, (x, y), 15)

    def __repr__(self):
        return str(self.color)


# -----------------------------
# BOARD CLASS
# -----------------------------

class Board:
    def __init__(self):
        self.board = []
        self.red_left = 12
        self.black_left = 12
        self.create_board()

    def draw_squares(self, win):
        win.fill(WHITE)

        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(
                    win,
                    BROWN,
                    (row * SQUARE_SIZE,
                     col * SQUARE_SIZE,
                     SQUARE_SIZE,
                     SQUARE_SIZE)
                )

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])

            for col in range(COLS):
                if (row + col) % 2 == 1:
                    if row < 3:
                        self.board[row].append(Piece(row, col, BLACK))

                    elif row > 4:
                        self.board[row].append(Piece(row, col, RED))

                    else:
                        self.board[row].append(None)
                else:
                    self.board[row].append(None)

    def draw(self, win):
        self.draw_squares(win)

        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]

                if piece:
                    piece.draw(win)

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = (
            self.board[row][col],
            self.board[piece.row][piece.col],
        )

        piece.move(row, col)

        if row == 0 and piece.color == RED:
            piece.make_king()

        if row == ROWS - 1 and piece.color == BLACK:
            piece.make_king()

    def get_piece(self, row, col):
        return self.board[row][col]

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = None

            if piece.color == RED:
                self.red_left -= 1
            else:
                self.black_left -= 1

    def winner(self):
        if self.red_left <= 0:
            return "BLACK"

        if self.black_left <= 0:
            return "RED"

        return None

    def get_valid_moves(self, piece):
        moves = {}

        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == RED or piece.king:
            moves.update(
                self._traverse_left(row - 1, max(row - 3, -1), -1,
                                    piece.color, left)
            )
            moves.update(
                self._traverse_right(row - 1, max(row - 3, -1), -1,
                                     piece.color, right)
            )

        if piece.color == BLACK or piece.king:
            moves.update(
                self._traverse_left(row + 1, min(row + 3, ROWS), 1,
                                    piece.color, left)
            )
            moves.update(
                self._traverse_right(row + 1, min(row + 3, ROWS), 1,
                                     piece.color, right)
            )

        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []

        for r in range(start, stop, step):

            if left < 0:
                break

            current = self.board[r][left]

            if current is None:

                if skipped and not last:
                    break

                elif skipped:
                    moves[(r, left)] = last + skipped

                else:
                    moves[(r, left)] = last

                if last:
                    row = max(r - 3, -1) if step == -1 else min(r + 3, ROWS)

                    moves.update(
                        self._traverse_left(
                            r + step, row, step,
                            color, left - 1,
                            skipped=last
                        )
                    )

                    moves.update(
                        self._traverse_right(
                            r + step, row, step,
                            color, left + 1,
                            skipped=last
                        )
                    )

                break

            elif current.color == color:
                break

            else:
                last = [current]

            left -= 1

        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []

        for r in range(start, stop, step):

            if right >= COLS:
                break

            current = self.board[r][right]

            if current is None:

                if skipped and not last:
                    break

                elif skipped:
                    moves[(r, right)] = last + skipped

                else:
                    moves[(r, right)] = last

                if last:
                    row = max(r - 3, -1) if step == -1 else min(r + 3, ROWS)

                    moves.update(
                        self._traverse_left(
                            r + step, row, step,
                            color, right - 1,
                            skipped=last
                        )
                    )

                    moves.update(
                        self._traverse_right(
                            r + step, row, step,
                            color, right + 1,
                            skipped=last
                        )
                    )

                break

            elif current.color == color:
                break

            else:
                last = [current]

            right += 1

        return moves


# -----------------------------
# GAME CLASS
# -----------------------------

class Game:
    def __init__(self, win):
        self.win = win
        self.selected = None
        self.board = Board()
        self.turn = RED
        self.valid_moves = {}

    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def reset(self):
        self.__init__(self.win)

    def select(self, row, col):

        if self.selected:
            result = self.move(row, col)

            if not result:
                self.selected = None
                self.select(row, col)

        piece = self.board.get_piece(row, col)

        if piece and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True

        return False

    def move(self, row, col):
        piece = self.board.get_piece(row, col)

        if self.selected and piece is None and (row, col) in self.valid_moves:

            self.board.move(self.selected, row, col)

            skipped = self.valid_moves[(row, col)]

            if skipped:
                self.board.remove(skipped)

            self.change_turn()

        else:
            return False

        return True

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move

            pygame.draw.circle(
                self.win,
                GREEN,
                (
                    col * SQUARE_SIZE + SQUARE_SIZE // 2,
                    row * SQUARE_SIZE + SQUARE_SIZE // 2
                ),
                15
            )

    def change_turn(self):
        self.valid_moves = {}

        if self.turn == RED:
            self.turn = BLACK
        else:
            self.turn = RED

    def winner(self):
        return self.board.winner()


# -----------------------------
# HELPER FUNCTIONS
# -----------------------------

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


# -----------------------------
# MAIN LOOP
# -----------------------------

def main():
    clock = pygame.time.Clock()
    game = Game(WIN)

    running = True

    while running:
        clock.tick(60)

        winner = game.winner()

        if winner:
            print(winner, "WINS!")
            running = False

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

        game.update()

    pygame.quit()
    sys.exit()


main()
