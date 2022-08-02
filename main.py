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
COLORS = ["green", "red", "yellow", "orange", "purple", "cyan"]
# SHAPES = [SQUARE]


class Block:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color


def detect_floor(shape):
    for box in shape:
        if box.y + box.height >= TOP_LEFT_Y + GAME_HEIGHT:
            return True
    return False


def detect_other_shapes(background_boxes, current_shape):
    for line in background_boxes.values():
        for box1 in line:
            for box in current_shape:
                if box.y + box.height == box1.y and box.x == box1.x:
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


def move_to_floor(current_shape_rects, background):
    while not detect_floor(current_shape_rects) and not detect_other_shapes(background, current_shape_rects):
        for box in current_shape_rects:
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
    for line in background_boxes.values():

        for box1 in line:
            for box in current_shape:
                if box.y == box1.y and box.x + box.width == box1.x:
                    return False
    return True


def detect_shapes_collision_on_moving_left(background_boxes, current_shape):
    for line in background_boxes.values():
        for box1 in line:
            for box in current_shape:
                if box.y == box1.y and box.x == box1.x + box1.width:
                    return False
    return True


def create_shape(shape, color):
    created_shape = []
    rows = len(shape[0]) // 8
    columns = 8
    for i in range(rows):
        for j in range(columns):
            if shape[0][i * columns + j] == "S":
                created_shape.append(Block(TOP_LEFT_X + (j + 1) * BLOCK_SIZE, TOP_LEFT_Y + i * BLOCK_SIZE,
                                                 BLOCK_SIZE, BLOCK_SIZE, color))
    return created_shape


def create_dict():
    dict = {}
    for i in range(TOP_LEFT_Y, GAME_HEIGHT + TOP_LEFT_Y, BLOCK_SIZE):
        dict[i] = []

    return dict


def check_for_line(background):
    new_background = background
    for y_val, line in background.items():
        if len(line) == GAME_WIDTH / BLOCK_SIZE:
            # print(y_val, line)
            remove_line(y_val, background)
            new_background = move_lines_down(y_val, background)

    return new_background


def move_lines_down(y, background):
    for y_val, line in background.items():
        if y > y_val:
            for box in line:
                box.y += BLOCK_SIZE

    new_background = create_dict()
    for line in background.values():
        for box in line:
            new_background[box.y].append(box)
    return new_background


def remove_line(y_val, background):
    background[y_val] = []


def draw_next_shape(next_shape):
    FONT = pygame.font.SysFont('indigo', 32)
    next_label = FONT.render("NEXT SHAPE: ", True, "white")
    WINDOW.blit(next_label, (GAME_WIDTH + 3 * BLOCK_SIZE, WINDOW_HEIGHT // 2 - 200))

    pygame.draw.line(WINDOW, 'white', (GAME_WIDTH + 2 * BLOCK_SIZE, WINDOW_HEIGHT // 2 - 150),
                     (GAME_WIDTH + 3 * BLOCK_SIZE + 180, WINDOW_HEIGHT // 2 - 150), width=3)
    pygame.draw.line(WINDOW, 'white', (GAME_WIDTH + 2 * BLOCK_SIZE, WINDOW_HEIGHT // 2),
                     (GAME_WIDTH + 3 * BLOCK_SIZE + 180, WINDOW_HEIGHT // 2), width=3)

    pygame.draw.line(WINDOW, 'white', (GAME_WIDTH + 2 * BLOCK_SIZE, WINDOW_HEIGHT // 2),
                     (GAME_WIDTH + 2 * BLOCK_SIZE, WINDOW_HEIGHT // 2 - 150), width=3)

    pygame.draw.line(WINDOW, 'white', (GAME_WIDTH + 3 * BLOCK_SIZE + 180, WINDOW_HEIGHT // 2),
                     (GAME_WIDTH + 3 * BLOCK_SIZE + 180, WINDOW_HEIGHT // 2 - 150), width=3)

    rows = len(next_shape[0][0]) // 8
    columns = 8
    for i in range(rows):
        for j in range(columns):
            if next_shape[0][0][i * columns + j] == "S":
                pygame.draw.rect(WINDOW, COLORS[SHAPES.index(next_shape)], pygame.Rect(GAME_WIDTH + BLOCK_SIZE + j * BLOCK_SIZE,
                                                             WINDOW_HEIGHT // 2 - 100 + i * BLOCK_SIZE, BLOCK_SIZE,
                                                             BLOCK_SIZE))


def draw_grid():
    for i in range(TOP_LEFT_X, GAME_WIDTH + TOP_LEFT_X + BLOCK_SIZE, BLOCK_SIZE):
        pygame.draw.line(WINDOW, 'white', (i, TOP_LEFT_Y), (i, GAME_HEIGHT + TOP_LEFT_Y))

    for i in range(TOP_LEFT_Y, GAME_HEIGHT + TOP_LEFT_Y + BLOCK_SIZE, BLOCK_SIZE):
        pygame.draw.line(WINDOW, 'white', (TOP_LEFT_X, i), (GAME_WIDTH + TOP_LEFT_X, i))


def draw_shape(shape):
    for box in shape:
        rect = pygame.Rect(box.x, box.y, box.width, box.height)
        pygame.draw.rect(WINDOW, box.color, rect)


def draw_background(background):
    for line in background.values():
        for box in line:
            rect = pygame.Rect(box.x, box.y, box.width, box.height)
            pygame.draw.rect(WINDOW, box.color, rect)


def draw(current_shape, background_boxes, next_shape):
    WINDOW.fill(WINDOW_BACKGROUND_COLOR)
    FONT = pygame.font.SysFont('indigo', 65)
    tetris_label = FONT.render("TETRIS", True, "white")
    WINDOW.blit(tetris_label, (WINDOW_WIDTH / 2 - tetris_label.get_width() / 2, TOP_LEFT_Y // 2 -
                               tetris_label.get_height() // 2))

    draw_shape(current_shape)
    draw_background(background_boxes)

    draw_next_shape(next_shape)
    draw_grid()
    pygame.display.update()


def main():
    run = True
    current_shape_size = 0
    background_boxes = create_dict()

    clock = pygame.time.Clock()
    current_shape = random.choice(SHAPES)
    next_shape = random.choice(SHAPES)
    current_shape_rects = create_shape(current_shape[0], COLORS[SHAPES.index(current_shape)])

    while run:
        clock.tick()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                if can_move_right(background_boxes, current_shape_rects):
                    if event.key == pygame.K_RIGHT:
                        move_right(current_shape_rects)
                if can_move_left(background_boxes, current_shape_rects):
                    if event.key == pygame.K_LEFT:
                        move_left(current_shape_rects)
                if event.key == pygame.K_DOWN:
                    move_fast_down(current_shape_rects)
                if event.key == pygame.K_SPACE:
                    move_to_floor(current_shape_rects, background_boxes)

        move_down(current_shape_rects)
        if detect_floor(current_shape_rects) or detect_other_shapes(background_boxes, current_shape_rects):
            for box in current_shape_rects:
                background_boxes[box.y].append(box)
            current_shape = next_shape
            next_shape = random.choice(SHAPES)
            current_shape_rects = create_shape(current_shape[0], COLORS[SHAPES.index(current_shape)])
            background_boxes = check_for_line(background_boxes)

        draw(current_shape_rects, background_boxes, next_shape)

    pygame.quit()


if __name__ == "__main__":
    main()
