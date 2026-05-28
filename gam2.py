# =========================================================
# ADVANCED BOARD GAMES HUB
# FULL WORKING CODE
# =========================================================
# INSTALL:
# pip install pygame-ce

import pygame
import random
import sys

pygame.init()

# =========================================================
# WINDOW
# =========================================================
WIDTH = 1280
HEIGHT = 720
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Advanced Board Games Hub")

clock = pygame.time.Clock()

# =========================================================
# COLORS
# =========================================================
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
GRAY = (60, 60, 60)

BLUE = (52, 152, 219)
GREEN = (46, 204, 113)
RED = (231, 76, 60)
YELLOW = (241, 196, 15)
PURPLE = (155, 89, 182)

# =========================================================
# FONTS
# =========================================================
TITLE_FONT = pygame.font.SysFont("arial", 58, bold=True)
FONT = pygame.font.SysFont("arial", 30)
SMALL_FONT = pygame.font.SysFont("arial", 22)

# =========================================================
# BUTTON CLASS
# =========================================================
class Button:

    def __init__(self, x, y, w, h, text, color):

        self.rect = pygame.Rect(x, y, w, h)

        self.text = text
        self.color = color

    def draw(self, surface):

        mouse = pygame.mouse.get_pos()

        hover = (
            min(self.color[0] + 25, 255),
            min(self.color[1] + 25, 255),
            min(self.color[2] + 25, 255)
        )

        current = hover if self.rect.collidepoint(mouse) else self.color

        pygame.draw.rect(
            surface,
            current,
            self.rect,
            border_radius=15
        )

        txt = FONT.render(self.text, True, WHITE)
        txt_rect = txt.get_rect(center=self.rect.center)

        surface.blit(txt, txt_rect)

    def clicked(self, event):

        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )

# =========================================================
# PARTICLES
# =========================================================
particles = []

def create_particles(x, y):

    for _ in range(20):

        particles.append([
            [x, y],
            [random.randint(-5, 5), random.randint(-5, 5)],
            random.randint(4, 8)
        ])

def update_particles():

    for particle in particles[:]:

        particle[0][0] += particle[1][0]
        particle[0][1] += particle[1][1]

        particle[2] -= 0.2

        pygame.draw.circle(
            screen,
            YELLOW,
            (int(particle[0][0]), int(particle[0][1])),
            int(max(particle[2], 0))
        )

        if particle[2] <= 0:
            particles.remove(particle)

# =========================================================
# SCENE
# =========================================================
scene = "menu"

# =========================================================
# TIC TAC TOE
# =========================================================
ttt_board = [["" for _ in range(3)] for _ in range(3)]

ttt_winner = None

ttt_mode = "easy"

def reset_ttt():

    global ttt_board, ttt_winner

    ttt_board = [["" for _ in range(3)] for _ in range(3)]

    ttt_winner = None

def draw_ttt():

    screen.fill(BLACK)

    title = TITLE_FONT.render(
        f"Tic Tac Toe ({ttt_mode.upper()})",
        True,
        WHITE
    )

    screen.blit(title, (300, 30))

    start_x = 450
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

            txt = FONT.render(ttt_board[row][col], True, BLUE)

            txt_rect = txt.get_rect(center=rect.center)

            screen.blit(txt, txt_rect)

    if ttt_winner:

        txt = TITLE_FONT.render(
            f"{ttt_winner} Wins!",
            True,
            GREEN
        )

        screen.blit(txt, (420, 560))

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

def ai_move_easy():

    empty = []

    for row in range(3):
        for col in range(3):

            if ttt_board[row][col] == "":
                empty.append((row, col))

    if empty:

        row, col = random.choice(empty)

        ttt_board[row][col] = "O"

def ai_move_medium():

    global ttt_winner

    # WIN MOVE
    for row in range(3):
        for col in range(3):

            if ttt_board[row][col] == "":

                ttt_board[row][col] = "O"

                check_ttt()

                if ttt_winner == "O":
                    return

                ttt_board[row][col] = ""
                ttt_winner = None

    # BLOCK PLAYER
    for row in range(3):
        for col in range(3):

            if ttt_board[row][col] == "":

                ttt_board[row][col] = "X"

                check_ttt()

                if ttt_winner == "X":

                    ttt_board[row][col] = "O"

                    ttt_winner = None

                    return

                ttt_board[row][col] = ""

                ttt_winner = None

    ai_move_easy()

def click_ttt(pos):

    global ttt_winner

    start_x = 450
    start_y = 180
    size = 100

    x, y = pos

    if start_x <= x <= start_x + 300 and start_y <= y <= start_y + 300:

        col = (x - start_x) // size
        row = (y - start_y) // size

        if ttt_board[row][col] == "" and ttt_winner is None:

            ttt_board[row][col] = "X"

            create_particles(x, y)

            check_ttt()

            if ttt_winner is None:

                if ttt_mode == "easy":
                    ai_move_easy()

                elif ttt_mode == "medium":
                    ai_move_medium()

                elif ttt_mode == "hard":
                    ai_move_medium()

                check_ttt()

# =========================================================
# SNAKE GAME
# =========================================================
snake = [(100, 100)]

snake_dir = (20, 0)

food = (400, 300)

snake_over = False

snake_mode = "easy"

snake_speed = {
    "easy": 10,
    "medium": 6,
    "hard": 3
}

def reset_snake():

    global snake, snake_dir, food, snake_over

    snake = [(100, 100)]

    snake_dir = (20, 0)

    food = (
        random.randint(0, WIDTH // 20 - 1) * 20,
        random.randint(0, HEIGHT // 20 - 1) * 20
    )

    snake_over = False

def update_snake():

    global snake, food, snake_over

    if snake_over:
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

        snake_over = True

        return

    snake.insert(0, new_head)

    if new_head == food:

        create_particles(food[0], food[1])

        food = (
            random.randint(0, WIDTH // 20 - 1) * 20,
            random.randint(0, HEIGHT // 20 - 1) * 20
        )

    else:
        snake.pop()

def draw_snake():

    screen.fill(BLACK)

    title = TITLE_FONT.render(
        f"Snake ({snake_mode.upper()})",
        True,
        GREEN
    )

    screen.blit(title, (380, 20))

    for part in snake:

        pygame.draw.rect(
            screen,
            GREEN,
            (part[0], part[1], 20, 20),
            border_radius=5
        )

    pygame.draw.rect(
        screen,
        RED,
        (food[0], food[1], 20, 20),
        border_radius=5
    )

    score = FONT.render(
        f"Score: {len(snake)-1}",
        True,
        WHITE
    )

    screen.blit(score, (20, 120))

    rule = SMALL_FONT.render(
        "Rules: Avoid walls and yourself",
        True,
        YELLOW
    )

    screen.blit(rule, (20, 170))

    if snake_over:

        txt = TITLE_FONT.render(
            "GAME OVER",
            True,
            RED
        )

        screen.blit(txt, (420, 320))

# =========================================================
# MEMORY GAME
# =========================================================
memory_mode = "easy"

def generate_memory():

    if memory_mode == "easy":
        pairs = 8

    elif memory_mode == "medium":
        pairs = 12

    else:
        pairs = 18

    values = list(range(1, pairs + 1)) * 2

    random.shuffle(values)

    return values

memory_values = generate_memory()

memory_cards = []

for i in range(len(memory_values)):

    memory_cards.append({
        "value": memory_values[i],
        "revealed": False
    })

selected = []

def reset_memory():

    global memory_values
    global memory_cards
    global selected

    memory_values = generate_memory()

    memory_cards = []

    for i in range(len(memory_values)):

        memory_cards.append({
            "value": memory_values[i],
            "revealed": False
        })

    selected = []

def draw_memory():

    screen.fill(BLACK)

    title = TITLE_FONT.render(
        f"Memory Match ({memory_mode.upper()})",
        True,
        PURPLE
    )

    screen.blit(title, (260, 20))

    cols = 6

    size = 90

    start_x = 300
    start_y = 140

    for i, card in enumerate(memory_cards):

        row = i // cols
        col = i % cols

        rect = pygame.Rect(
            start_x + col * size,
            start_y + row * size,
            80,
            80
        )

        pygame.draw.rect(
            screen,
            PURPLE,
            rect,
            border_radius=10
        )

        if card["revealed"]:

            txt = FONT.render(
                str(card["value"]),
                True,
                WHITE
            )

            txt_rect = txt.get_rect(center=rect.center)

            screen.blit(txt, txt_rect)

def click_memory(pos):

    global selected

    cols = 6
    size = 90

    start_x = 300
    start_y = 140

    for i, card in enumerate(memory_cards):

        row = i // cols
        col = i % cols

        rect = pygame.Rect(
            start_x + col * size,
            start_y + row * size,
            80,
            80
        )

        if rect.collidepoint(pos):

            if not card["revealed"] and len(selected) < 2:

                card["revealed"] = True

                selected.append(i)

                create_particles(pos[0], pos[1])

    if len(selected) == 2:

        a, b = selected

        if memory_cards[a]["value"] != memory_cards[b]["value"]:

            pygame.time.delay(400)

            memory_cards[a]["revealed"] = False
            memory_cards[b]["revealed"] = False

        selected = []

# =========================================================
# BUTTONS
# =========================================================
btn_ttt = Button(100, 220, 300, 80, "Tic Tac Toe", BLUE)

btn_snake = Button(500, 220, 300, 80, "Snake", GREEN)

btn_memory = Button(900, 220, 300, 80, "Memory Match", PURPLE)

btn_exit = Button(500, 380, 300, 80, "Exit", RED)

back_btn = Button(20, 20, 120, 50, "Back", GRAY)

reset_btn = Button(1140, 20, 120, 50, "Reset", YELLOW)

easy_btn = Button(100, 620, 200, 60, "Easy", GREEN)

medium_btn = Button(350, 620, 200, 60, "Medium", YELLOW)

hard_btn = Button(600, 620, 200, 60, "Hard", RED)

# =========================================================
# MENU
# =========================================================
def draw_menu():

    screen.fill(BLACK)

    title = TITLE_FONT.render(
        "ADVANCED BOARD GAMES HUB",
        True,
        WHITE
    )

    screen.blit(title, (160, 60))

    btn_ttt.draw(screen)
    btn_snake.draw(screen)
    btn_memory.draw(screen)

    btn_exit.draw(screen)

# =========================================================
# MAIN LOOP
# =========================================================
running = True

snake_timer = 0

while running:

    clock.tick(FPS)

    snake_timer += 1

    if scene == "snake":

        if snake_timer > snake_speed[snake_mode]:

            update_snake()

            snake_timer = 0

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

        # =================================================
        # MENU
        # =================================================
        if scene == "menu":

            if btn_ttt.clicked(event):
                scene = "ttt"

            if btn_snake.clicked(event):
                scene = "snake"

            if btn_memory.clicked(event):
                scene = "memory"

            if btn_exit.clicked(event):
                running = False

        # =================================================
        # TIC TAC TOE
        # =================================================
        elif scene == "ttt":

            if event.type == pygame.MOUSEBUTTONDOWN:
                click_ttt(event.pos)

            if easy_btn.clicked(event):
                ttt_mode = "easy"

            if medium_btn.clicked(event):
                ttt_mode = "medium"

            if hard_btn.clicked(event):
                ttt_mode = "hard"

            if back_btn.clicked(event):
                scene = "menu"

            if reset_btn.clicked(event):
                reset_ttt()

        # =================================================
        # SNAKE
        # =================================================
        elif scene == "snake":

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_UP:
                    snake_dir = (0, -20)

                elif event.key == pygame.K_DOWN:
                    snake_dir = (0, 20)

                elif event.key == pygame.K_LEFT:
                    snake_dir = (-20, 0)

                elif event.key == pygame.K_RIGHT:
                    snake_dir = (20, 0)

            if easy_btn.clicked(event):
                snake_mode = "easy"

            if medium_btn.clicked(event):
                snake_mode = "medium"

            if hard_btn.clicked(event):
                snake_mode = "hard"

            if back_btn.clicked(event):
                scene = "menu"

            if reset_btn.clicked(event):
                reset_snake()

        # =================================================
        # MEMORY
        # =================================================
        elif scene == "memory":

            if event.type == pygame.MOUSEBUTTONDOWN:
                click_memory(event.pos)

            if easy_btn.clicked(event):

                memory_mode = "easy"

                reset_memory()

            if medium_btn.clicked(event):

                memory_mode = "medium"

                reset_memory()

            if hard_btn.clicked(event):

                memory_mode = "hard"

                reset_memory()

            if back_btn.clicked(event):
                scene = "menu"

            if reset_btn.clicked(event):
                reset_memory()

    # =====================================================
    # DRAW
    # =====================================================
    if scene == "menu":

        draw_menu()

    elif scene == "ttt":

        draw_ttt()

        easy_btn.draw(screen)
        medium_btn.draw(screen)
        hard_btn.draw(screen)

        back_btn.draw(screen)
        reset_btn.draw(screen)

    elif scene == "snake":

        draw_snake()

        easy_btn.draw(screen)
        medium_btn.draw(screen)
        hard_btn.draw(screen)

        back_btn.draw(screen)
        reset_btn.draw(screen)

    elif scene == "memory":

        draw_memory()

        easy_btn.draw(screen)
        medium_btn.draw(screen)
        hard_btn.draw(screen)

        back_btn.draw(screen)
        reset_btn.draw(screen)

    update_particles()

    pygame.display.update()

pygame.quit()
sys.exit()
