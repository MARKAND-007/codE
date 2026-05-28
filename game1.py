# INSTALL:
# pip install pygame-ce

import pygame
import random
import sys

pygame.init()

# ==================================================
# SETTINGS
# ==================================================
WIDTH = 1200
HEIGHT = 750
FPS = 60

WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
GRAY = (50, 50, 50)
BLUE = (52, 152, 219)
GREEN = (46, 204, 113)
RED = (231, 76, 60)
YELLOW = (241, 196, 15)
PURPLE = (155, 89, 182)
ORANGE = (230, 126, 34)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Board Games Hub")

clock = pygame.time.Clock()

font = pygame.font.SysFont("arial", 28)
small_font = pygame.font.SysFont("arial", 20)
large_font = pygame.font.SysFont("arial", 55)

# ==================================================
# BUTTON CLASS
# ==================================================
class Button:
    def __init__(self, x, y, w, h, text, color):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color

    def draw(self, surface):
        mouse = pygame.mouse.get_pos()

        hover = (
            min(self.color[0] + 30, 255),
            min(self.color[1] + 30, 255),
            min(self.color[2] + 30, 255),
        )

        current = hover if self.rect.collidepoint(mouse) else self.color

        pygame.draw.rect(surface, current, self.rect, border_radius=15)

        txt = font.render(self.text, True, WHITE)
        txt_rect = txt.get_rect(center=self.rect.center)
        surface.blit(txt, txt_rect)

    def clicked(self, event):
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )

# ==================================================
# GLOBALS
# ==================================================
current_scene = "menu"

# ==================================================
# TIC TAC TOE
# ==================================================
ttt_board = [["" for _ in range(3)] for _ in range(3)]
ttt_player = "X"
ttt_winner = None

def reset_ttt():
    global ttt_board, ttt_player, ttt_winner
    ttt_board = [["" for _ in range(3)] for _ in range(3)]
    ttt_player = "X"
    ttt_winner = None

def draw_ttt():
    screen.fill(BLACK)

    title = large_font.render("Tic Tac Toe", True, WHITE)
    screen.blit(title, (420, 40))

    start_x = 420
    start_y = 180
    size = 100

    for row in range(3):
        for col in range(3):
            rect = pygame.Rect(
                start_x + col * size,
                start_y + row * size,
                size,
                size
            )

            pygame.draw.rect(screen, WHITE, rect, 3)

            text = font.render(ttt_board[row][col], True, BLUE)
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)

    if ttt_winner:
        txt = large_font.render(f"{ttt_winner} Wins!", True, GREEN)
        screen.blit(txt, (430, 550))
    else:
        txt = font.render(f"Turn: {ttt_player}", True, YELLOW)
        screen.blit(txt, (520, 550))

def check_ttt():
    global ttt_winner

    for row in ttt_board:
        if row[0] == row[1] == row[2] != "":
            ttt_winner = row[0]

    for col in range(3):
        if ttt_board[0][col] == ttt_board[1][col] == ttt_board[2][col] != "":
            ttt_winner = ttt_board[0][col]

    if ttt_board[0][0] == ttt_board[1][1] == ttt_board[2][2] != "":
        ttt_winner = ttt_board[0][0]

    if ttt_board[0][2] == ttt_board[1][1] == ttt_board[2][0] != "":
        ttt_winner = ttt_board[0][2]

def click_ttt(pos):
    global ttt_player

    start_x = 420
    start_y = 180
    size = 100

    x, y = pos

    if start_x <= x <= start_x + 300 and start_y <= y <= start_y + 300:
        col = (x - start_x) // size
        row = (y - start_y) // size

        if ttt_board[row][col] == "" and ttt_winner is None:
            ttt_board[row][col] = ttt_player
            check_ttt()
            ttt_player = "O" if ttt_player == "X" else "X"

# ==================================================
# SNAKE GAME
# ==================================================
snake = [(100, 100)]
snake_dir = (20, 0)
food = (300, 300)
snake_game_over = False

def reset_snake_game():
    global snake, snake_dir, food, snake_game_over

    snake = [(100, 100)]
    snake_dir = (20, 0)
    food = (
        random.randint(0, WIDTH // 20 - 1) * 20,
        random.randint(0, HEIGHT // 20 - 1) * 20
    )
    snake_game_over = False

def draw_snake_game():
    screen.fill(BLACK)

    title = large_font.render("Snake Game", True, GREEN)
    screen.blit(title, (420, 20))

    for segment in snake:
        pygame.draw.rect(screen, GREEN, (segment[0], segment[1], 20, 20))

    pygame.draw.rect(screen, RED, (food[0], food[1], 20, 20))

    score = font.render(f"Score: {len(snake) - 1}", True, WHITE)
    screen.blit(score, (20, 100))

    if snake_game_over:
        txt = large_font.render("GAME OVER", True, RED)
        screen.blit(txt, (420, 350))

def update_snake():
    global snake, food, snake_game_over

    if snake_game_over:
        return

    head_x, head_y = snake[0]
    dx, dy = snake_dir

    new_head = (head_x + dx, head_y + dy)

    if (
        new_head[0] < 0 or
        new_head[0] >= WIDTH or
        new_head[1] < 0 or
        new_head[1] >= HEIGHT or
        new_head in snake
    ):
        snake_game_over = True
        return

    snake.insert(0, new_head)

    if new_head == food:
        food = (
            random.randint(0, WIDTH // 20 - 1) * 20,
            random.randint(0, HEIGHT // 20 - 1) * 20,
        )
    else:
        snake.pop()

# ==================================================
# CONNECT FOUR
# ==================================================
ROWS = 6
COLS = 7

cf_board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
cf_player = 1

def reset_cf():
    global cf_board, cf_player

    cf_board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    cf_player = 1

def draw_cf():
    screen.fill(BLACK)

    title = large_font.render("Connect Four", True, YELLOW)
    screen.blit(title, (400, 20))

    start_x = 300
    start_y = 120
    size = 80

    for row in range(ROWS):
        for col in range(COLS):

            pygame.draw.rect(
                screen,
                BLUE,
                (start_x + col * size,
                 start_y + row * size,
                 size,
                 size)
            )

            color = BLACK

            if cf_board[row][col] == 1:
                color = RED
            elif cf_board[row][col] == 2:
                color = YELLOW

            pygame.draw.circle(
                screen,
                color,
                (start_x + col * size + 40,
                 start_y + row * size + 40),
                30
            )

def click_cf(pos):
    global cf_player

    x, y = pos

    start_x = 300
    size = 80

    if 300 <= x <= 860:
        col = (x - start_x) // size

        for row in range(ROWS - 1, -1, -1):
            if cf_board[row][col] == 0:
                cf_board[row][col] = cf_player
                cf_player = 2 if cf_player == 1 else 1
                break

# ==================================================
# MEMORY GAME
# ==================================================
memory_values = list(range(1, 9)) * 2
random.shuffle(memory_values)

memory_tiles = []

for i in range(16):
    memory_tiles.append({
        "value": memory_values[i],
        "revealed": False
    })

selected = []

def reset_memory():
    global memory_values, memory_tiles, selected

    memory_values = list(range(1, 9)) * 2
    random.shuffle(memory_values)

    memory_tiles = []

    for i in range(16):
        memory_tiles.append({
            "value": memory_values[i],
            "revealed": False
        })

    selected = []

def draw_memory():
    screen.fill(BLACK)

    title = large_font.render("Memory Match", True, PURPLE)
    screen.blit(title, (400, 20))

    start_x = 350
    start_y = 150
    size = 100

    for i, tile in enumerate(memory_tiles):

        row = i // 4
        col = i % 4

        rect = pygame.Rect(
            start_x + col * size,
            start_y + row * size,
            90,
            90
        )

        pygame.draw.rect(screen, PURPLE, rect, border_radius=10)

        if tile["revealed"]:
            txt = font.render(str(tile["value"]), True, WHITE)
            txt_rect = txt.get_rect(center=rect.center)
            screen.blit(txt, txt_rect)

def click_memory(pos):
    global selected

    start_x = 350
    start_y = 150
    size = 100

    for i, tile in enumerate(memory_tiles):

        row = i // 4
        col = i % 4

        rect = pygame.Rect(
            start_x + col * size,
            start_y + row * size,
            90,
            90
        )

        if rect.collidepoint(pos):

            if not tile["revealed"] and len(selected) < 2:
                tile["revealed"] = True
                selected.append(i)

    if len(selected) == 2:

        a, b = selected

        if memory_tiles[a]["value"] != memory_tiles[b]["value"]:
            pygame.time.delay(500)

            memory_tiles[a]["revealed"] = False
            memory_tiles[b]["revealed"] = False

        selected = []

# ==================================================
# BUTTONS
# ==================================================
btn_ttt = Button(120, 200, 250, 70, "Tic Tac Toe", BLUE)
btn_snake = Button(450, 200, 250, 70, "Snake Game", GREEN)
btn_cf = Button(780, 200, 250, 70, "Connect Four", YELLOW)

btn_memory = Button(120, 350, 250, 70, "Memory Match", PURPLE)
btn_exit = Button(450, 350, 250, 70, "Exit", RED)

back_btn = Button(20, 20, 120, 50, "Back", GRAY)
reset_btn = Button(1050, 20, 120, 50, "Reset", ORANGE)

# ==================================================
# MENU
# ==================================================
def draw_menu():
    screen.fill(BLACK)

    title = large_font.render("BOARD GAMES HUB", True, WHITE)
    screen.blit(title, (300, 60))

    sub = font.render("Classic Game Collection", True, GRAY)
    screen.blit(sub, (450, 130))

    btn_ttt.draw(screen)
    btn_snake.draw(screen)
    btn_cf.draw(screen)
    btn_memory.draw(screen)
    btn_exit.draw(screen)

# ==================================================
# MAIN LOOP
# ==================================================
running = True
snake_timer = 0

while running:

    clock.tick(FPS)

    snake_timer += 1

    if current_scene == "snake_game" and snake_timer > 8:
        update_snake()
        snake_timer = 0

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # ================= MENU =================
        if current_scene == "menu":

            if btn_ttt.clicked(event):
                current_scene = "ttt"

            if btn_snake.clicked(event):
                current_scene = "snake_game"

            if btn_cf.clicked(event):
                current_scene = "cf"

            if btn_memory.clicked(event):
                current_scene = "memory"

            if btn_exit.clicked(event):
                running = False

        # ================= TIC TAC TOE =================
        elif current_scene == "ttt":

            if event.type == pygame.MOUSEBUTTONDOWN:
                click_ttt(event.pos)

            if back_btn.clicked(event):
                current_scene = "menu"

            if reset_btn.clicked(event):
                reset_ttt()

        # ================= SNAKE GAME =================
        elif current_scene == "snake_game":

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_UP:
                    snake_dir = (0, -20)

                elif event.key == pygame.K_DOWN:
                    snake_dir = (0, 20)

                elif event.key == pygame.K_LEFT:
                    snake_dir = (-20, 0)

                elif event.key == pygame.K_RIGHT:
                    snake_dir = (20, 0)

            if back_btn.clicked(event):
                current_scene = "menu"

            if reset_btn.clicked(event):
                reset_snake_game()

        # ================= CONNECT FOUR =================
        elif current_scene == "cf":

            if event.type == pygame.MOUSEBUTTONDOWN:
                click_cf(event.pos)

            if back_btn.clicked(event):
                current_scene = "menu"

            if reset_btn.clicked(event):
                reset_cf()

        # ================= MEMORY GAME =================
        elif current_scene == "memory":

            if event.type == pygame.MOUSEBUTTONDOWN:
                click_memory(event.pos)

            if back_btn.clicked(event):
                current_scene = "menu"

            if reset_btn.clicked(event):
                reset_memory()

    # ==================================================
    # DRAW SCENES
    # ==================================================
    if current_scene == "menu":
        draw_menu()

    elif current_scene == "ttt":
        draw_ttt()
        back_btn.draw(screen)
        reset_btn.draw(screen)

    elif current_scene == "snake_game":
        draw_snake_game()
        back_btn.draw(screen)
        reset_btn.draw(screen)

    elif current_scene == "cf":
        draw_cf()
        back_btn.draw(screen)
        reset_btn.draw(screen)

    elif current_scene == "memory":
        draw_memory()
        back_btn.draw(screen)
        reset_btn.draw(screen)

    pygame.display.update()

pygame.quit()
sys.exit()
