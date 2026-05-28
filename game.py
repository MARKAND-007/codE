import pygame
import random
import sys

pygame.init()

# =========================
# SETTINGS
# =========================
WIDTH = 1200
HEIGHT = 700
FPS = 60

WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
GRAY = (50, 50, 50)
BLUE = (52, 152, 219)
GREEN = (46, 204, 113)
RED = (231, 76, 60)
YELLOW = (241, 196, 15)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Board Games Hub")
clock = pygame.time.Clock()

font = pygame.font.SysFont("arial", 30)
small_font = pygame.font.SysFont("arial", 22)
large_font = pygame.font.SysFont("arial", 60)

# =========================
# BUTTON CLASS
# =========================
class Button:
    def __init__(self, x, y, w, h, text, color):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color

    def draw(self, surface):
        mouse = pygame.mouse.get_pos()

        hover_color = (
            min(self.color[0] + 20, 255),
            min(self.color[1] + 20, 255),
            min(self.color[2] + 20, 255),
        )

        current = hover_color if self.rect.collidepoint(mouse) else self.color

        pygame.draw.rect(surface, current, self.rect, border_radius=15)

        text_surface = font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def clicked(self, event):
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )

# =========================
# SCENE MANAGER
# =========================
current_scene = "menu"

# =========================
# TIC TAC TOE
# =========================
board = [["" for _ in range(3)] for _ in range(3)]
player = "X"
winner = None

def reset_tictactoe():
    global board, player, winner
    board = [["" for _ in range(3)] for _ in range(3)]
    player = "X"
    winner = None


def draw_tictactoe():
    screen.fill(BLACK)

    title = large_font.render("Tic Tac Toe", True, WHITE)
    screen.blit(title, (420, 30))

    start_x = 400
    start_y = 150
    cell = 120

    for row in range(3):
        for col in range(3):
            rect = pygame.Rect(start_x + col * cell, start_y + row * cell, cell, cell)
            pygame.draw.rect(screen, WHITE, rect, 3)

            text = font.render(board[row][col], True, BLUE)
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)

    if winner:
        result = large_font.render(f"Winner: {winner}", True, GREEN)
        screen.blit(result, (420, 550))
    else:
        turn = font.render(f"Turn: {player}", True, YELLOW)
        screen.blit(turn, (520, 550))


def check_winner():
    global winner

    for row in board:
        if row[0] == row[1] == row[2] != "":
            winner = row[0]

    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != "":
            winner = board[0][col]

    if board[0][0] == board[1][1] == board[2][2] != "":
        winner = board[0][0]

    if board[0][2] == board[1][1] == board[2][0] != "":
        winner = board[0][2]


def tictactoe_click(pos):
    global player

    start_x = 400
    start_y = 150
    cell = 120

    x, y = pos

    if start_x <= x <= start_x + 360 and start_y <= y <= start_y + 360:
        col = (x - start_x) // cell
        row = (y - start_y) // cell

        if board[row][col] == "" and winner is None:
            board[row][col] = player
            check_winner()
            player = "O" if player == "X" else "X"

# =========================
# SNAKE & LADDERS
# =========================
player_pos = 1

dice_value = 1

snakes = {
    99: 54,
    70: 55,
    52: 42,
    25: 2,
    95: 72,
}

ladders = {
    6: 25,
    11: 40,
    60: 85,
    46: 90,
    17: 69,
}


def reset_snake():
    global player_pos
    player_pos = 1


def draw_board_snake():
    screen.fill(BLACK)

    title = large_font.render("Snake & Ladders", True, WHITE)
    screen.blit(title, (350, 10))

    size = 60
    start_x = 250
    start_y = 80

    number = 100

    for row in range(10):
        cols = range(10) if row % 2 == 0 else range(9, -1, -1)

        for col in cols:
            x = start_x + col * size
            y = start_y + row * size

            pygame.draw.rect(screen, WHITE, (x, y, size, size), 2)

            num_text = small_font.render(str(number), True, WHITE)
            screen.blit(num_text, (x + 5, y + 5))

            if number == player_pos:
                pygame.draw.circle(screen, RED, (x + 30, y + 30), 18)

            number -= 1

    dice_text = font.render(f"Dice: {dice_value}", True, YELLOW)
    screen.blit(dice_text, (900, 200))

    roll_button.draw(screen)

    if player_pos >= 100:
        win_text = large_font.render("YOU WIN!", True, GREEN)
        screen.blit(win_text, (850, 400))


def move_player():
    global player_pos, dice_value

    if player_pos < 100:
        dice_value = random.randint(1, 6)
        player_pos += dice_value

        if player_pos in snakes:
            player_pos = snakes[player_pos]

        if player_pos in ladders:
            player_pos = ladders[player_pos]

        if player_pos > 100:
            player_pos = 100

# =========================
# MENU BUTTONS
# =========================
btn_tic = Button(430, 220, 340, 70, "Tic Tac Toe", BLUE)
btn_snake = Button(430, 320, 340, 70, "Snake & Ladders", GREEN)
btn_exit = Button(430, 420, 340, 70, "Exit", RED)

back_button = Button(20, 20, 140, 50, "Back", GRAY)
reset_button = Button(1020, 20, 150, 50, "Reset", BLUE)
roll_button = Button(900, 280, 180, 70, "Roll Dice", GREEN)

# =========================
# DRAW MENU
# =========================
def draw_menu():
    screen.fill(BLACK)

    title = large_font.render("BOARD GAMES HUB", True, WHITE)
    screen.blit(title, (300, 80))

    subtitle = font.render("Classic Games Collection", True, GRAY)
    screen.blit(subtitle, (420, 150))

    btn_tic.draw(screen)
    btn_snake.draw(screen)
    btn_exit.draw(screen)

# =========================
# MAIN LOOP
# =========================
running = True

while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # ================= MENU =================
        if current_scene == "menu":
            if btn_tic.clicked(event):
                current_scene = "tic"

            if btn_snake.clicked(event):
                current_scene = "snake"

            if btn_exit.clicked(event):
                running = False

        # ================= TIC TAC TOE =================
        elif current_scene == "tic":
            if event.type == pygame.MOUSEBUTTONDOWN:
                tictactoe_click(event.pos)

            if back_button.clicked(event):
                current_scene = "menu"

            if reset_button.clicked(event):
                reset_tictactoe()

        # ================= SNAKE =================
        elif current_scene == "snake":
            if roll_button.clicked(event):
                move_player()

            if back_button.clicked(event):
                current_scene = "menu"

            if reset_button.clicked(event):
                reset_snake()

    # ================= DRAW =================
    if current_scene == "menu":
        draw_menu()

    elif current_scene == "tic":
        draw_tictactoe()
        back_button.draw(screen)
        reset_button.draw(screen)

    elif current_scene == "snake":
        draw_board_snake()
        back_button.draw(screen)
        reset_button.draw(screen)

    pygame.display.update()

pygame.quit()
sys.exit()
