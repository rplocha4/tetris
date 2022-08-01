import random

import pygame

pygame.init()

BLOCK_SIZE = 30
WINDOW_WIDTH, WINDOW_HEIGHT = 600, 700
GAME_WIDTH, GAME_HEIGHT = 300, 600
TOP_LEFT_X = BLOCK_SIZE
TOP_LEFT_Y = WINDOW_HEIGHT - GAME_HEIGHT - BLOCK_SIZE
WINDOW_BACKGROUND_COLOR = 'black'
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

last = pygame.time.get_ticks()
cooldown = 600


I = [["..SSSS.."],
     ["....S..."
      "....S..."
      "....S..."
      "....S..."]]

T = [["....S..."
      "...SSS.."],
     ["....S..."
      "....SS.."
      "....S..."]]
SQUARE = [
    ["...SS..."
     "...SS..."]]
Z = [["....S..."
      "...SS..."
      "...S...."],
     ["...SS..."
      "....SS.."]]
S = [["....S..."
      "....SS.."
      ".....S.."],
     ["...SS..."
      "..SS...."]]
L = [["...SS..."
      "....S..."
      "....S..."],
     ["........"
      "....S..."
      "..SSS..."]]

SHAPES = [S, Z, SQUARE, L, T, I]


def create_shape(shape):
    created_shape = []
    rows = len(shape[0]) // 8
    columns = 8
    # for i, row in enumerate(shape):
    #     for j, el in enumerate(row):
    for i in range(rows):
        for j in range(columns):
            if shape[0][i * columns + j] == "S":
                created_shape.append(pygame.Rect(TOP_LEFT_X + (j + 1) * BLOCK_SIZE, TOP_LEFT_Y + i * BLOCK_SIZE,
                                                 BLOCK_SIZE, BLOCK_SIZE))
    return created_shape


def draw_grid():
    for i in range(TOP_LEFT_X, GAME_WIDTH + TOP_LEFT_X + BLOCK_SIZE, BLOCK_SIZE):
        pygame.draw.line(WINDOW, 'white', (i, TOP_LEFT_Y), (i, GAME_HEIGHT + TOP_LEFT_Y))

    for i in range(TOP_LEFT_Y, GAME_HEIGHT + TOP_LEFT_Y + BLOCK_SIZE, BLOCK_SIZE):
        pygame.draw.line(WINDOW, 'white', (TOP_LEFT_X, i), (GAME_WIDTH + TOP_LEFT_X, i))


def draw_shape(shape):
    for rect in shape:
        pygame.draw.rect(WINDOW, 'blue', rect)


def draw(current_shape):
    WINDOW.fill(WINDOW_BACKGROUND_COLOR)
    FONT = pygame.font.SysFont('indigo', 40 + 15)
    tetris_label = FONT.render("TETRIS", True, "white")
    WINDOW.blit(tetris_label, (WINDOW_WIDTH / 2 - tetris_label.get_width() / 2, TOP_LEFT_Y // 2 -
                               tetris_label.get_height() // 2))


    draw_shape(current_shape)

    draw_grid()
    pygame.display.update()


def main():
    run = True
    clock = pygame.time.Clock()
    current_shape = create_shape(random.choice(SHAPES)[0])
    next_shape = create_shape(random.choice(SHAPES)[0])

    while run:
        clock.tick()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        global last
        now = pygame.time.get_ticks()
        if now - last >= cooldown:
            last = now
            current_shape = next_shape
            next_shape = create_shape(random.choice(SHAPES)[0])

        draw(current_shape)

    pygame.quit()


if __name__ == "__main__":
    main()
