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


def detect_floor(shape):
    for box in shape:
        if box.y + box.height >= TOP_LEFT_Y + GAME_HEIGHT:
            return True
    return False


def detect_other_shapes(background_boxes, current_shape):
    for box1 in background_boxes:
        for box in current_shape:
            if box.y + box.height >= box1.y and box.x == box1.x:
                return True
    return False


def move_down(shape):
    global last
    now = pygame.time.get_ticks()
    if now - last >= cooldown:
        last = now
        for box in shape:
            box.y += BLOCK_SIZE


def move_fast_down(shape):
    for box in shape:
        box.y += BLOCK_SIZE


def move_right(shape):
    for box in shape:
        box.x += BLOCK_SIZE


def move_left(shape):
    for box in shape:
        box.x -= BLOCK_SIZE


def detect_left_wall(shape):
    for box in shape:
        if box.x <= TOP_LEFT_X:
            return True
    return False


def detect_right_wall(shape):
    for box in shape:
        if box.x + box.width >= TOP_LEFT_X + GAME_WIDTH:
            return True
    return False


def can_move_right(background_boxes, current_shape):
    return not detect_right_wall(current_shape) and detect_shapes_collision_on_moving_right(background_boxes,
                                                                                            current_shape)

def can_move_left(background_boxes, current_shape):
    return not detect_left_wall(current_shape) and detect_shapes_collision_on_moving_left(background_boxes,
                                                                                          current_shape)



def detect_shapes_collision_on_moving_right(background_boxes, current_shape):
    for box1 in background_boxes:
        for box in current_shape:
            if box.y == box1.y and box.x + box.width >= box1.x:
                return False
    return True


def detect_shapes_collision_on_moving_left(background_boxes, current_shape):
    for box1 in background_boxes:
        for box in current_shape:
            if box.y == box1.y and box.x <= box1.x + box1.width:
                return False
    return True


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


def draw(current_shape, background_boxes):
    WINDOW.fill(WINDOW_BACKGROUND_COLOR)
    FONT = pygame.font.SysFont('indigo', 65)
    tetris_label = FONT.render("TETRIS", True, "white")
    WINDOW.blit(tetris_label, (WINDOW_WIDTH / 2 - tetris_label.get_width() / 2, TOP_LEFT_Y // 2 -
                               tetris_label.get_height() // 2))

    draw_shape(current_shape)
    for box in background_boxes:
        pygame.draw.rect(WINDOW, 'blue', box)
    draw_grid()
    pygame.display.update()


def main():
    run = True
    background_boxes = []

    clock = pygame.time.Clock()
    current_shape = create_shape(random.choice(SHAPES)[0])
    next_shape = create_shape(random.choice(SHAPES)[0])

    while run:
        clock.tick()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if can_move_right(background_boxes, current_shape):
                    if event.key == pygame.K_RIGHT:
                        move_right(current_shape)
                if can_move_left(background_boxes, current_shape):
                    if event.key == pygame.K_LEFT:
                        move_left(current_shape)
                if event.key == pygame.K_DOWN:
                    move_fast_down(current_shape)

        move_down(current_shape)
        if detect_floor(current_shape) or detect_other_shapes(background_boxes, current_shape):
            for box in current_shape:
                background_boxes.append(box)
            current_shape = next_shape
            next_shape = create_shape(random.choice(SHAPES)[0])

        draw(current_shape, background_boxes)

    pygame.quit()


if __name__ == "__main__":
    main()
