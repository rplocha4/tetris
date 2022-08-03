import random
import time

import pygame

pygame.init()

BLOCK_SIZE = 30
WINDOW_WIDTH, WINDOW_HEIGHT = 600, 700
GAME_WIDTH, GAME_HEIGHT = 300, 600
TOP_LEFT_X = BLOCK_SIZE
TOP_LEFT_Y = WINDOW_HEIGHT - GAME_HEIGHT - BLOCK_SIZE
BORDER_GRID_COLOR = 'blue'
GRID_COLOR = 'grey'
WINDOW_BACKGROUND_COLOR = 'black'
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

last = pygame.time.get_ticks()
delay = 500

I = [["SSSS"],
     [".S.."
      ".S.."
      ".S.."
      ".S.."]]

T = [[".S.."
      "SSS."],
     [".S.."
      ".SS."
      ".S.."],
     ["...."
      "SSS."
      ".S.."],
     [".S.."
      "SS.."
      ".S.."]]

SQUARE = [
    ["SS.."
     "SS.."]]

Z = [[".S.."
      "SS.."
      "S..."],
     ["SS.."
      ".SS."]]

S = [["S..."
      "SS.."
      ".S.."],
     [".SS."
      "SS.."],
     # ["S..."
     #  "SS.."
     #  ".S.."],
     # [".SS."
     #  "SS.."],
     ]
L = [["SS.."
      ".S.."
      ".S.."],
     ["...."
      "..S."
      "SSS."],
     ["S..."
      "S..."
      "SS.."],
     ["SSS."
      "S..."
      "...."]
     ]
L_m = [["SS.."
        "S..."
        "S..."],
       ["SSS."
        "..S."],
       [".S.."
        ".S.."
        "SS.."],
       ["S..."
        "SSS."]]

SHAPES = [S, Z, SQUARE, L, T, I, L_m]
COLORS = ["green", "red", "yellow", "orange", "purple", "cyan", "blue"]


# SHAPES = [L_m]


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


def auto_move_down(shape):
    global last
    now = pygame.time.get_ticks()
    if now - last >= delay:
        last = now
        for box in shape:
            box.y += BLOCK_SIZE


def move_fast_down(shape):
    for box in shape:
        box.y += BLOCK_SIZE


def move_to_floor(current_shape_rects, background):
    while not detect_other_shapes(background, current_shape_rects) and not detect_floor(current_shape_rects):
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
    return not detect_right_wall(current_shape) and not detect_shapes_collision_on_moving_right(background_boxes,
                                                                                                current_shape)


def can_move_left(background_boxes, current_shape):
    return not detect_left_wall(current_shape) and not detect_shapes_collision_on_moving_left(background_boxes,
                                                                                              current_shape)


def detect_shapes_collision_on_moving_right(background_boxes, current_shape):
    for line in background_boxes.values():

        for box1 in line:
            for box in current_shape:
                if box.y == box1.y and box.x + box.width == box1.x:
                    return True
    return False


def detect_shapes_collision_on_moving_left(background_boxes, current_shape):
    for line in background_boxes.values():
        for box1 in line:
            for box in current_shape:
                if box.y == box1.y and box.x == box1.x + box1.width:
                    return True
    return False


# def create_shape(shape, color, current_x=TOP_LEFT_X):
#     created_shape = []
#     rows = len(shape[0]) // 8
#     columns = 8
#     for i in range(rows):
#         for j in range(columns):
#             if shape[0][i * columns + j] == "S":
#                 created_shape.append(Block(current_x + (j + 1) * BLOCK_SIZE, TOP_LEFT_Y + i * BLOCK_SIZE,
#                                            BLOCK_SIZE, BLOCK_SIZE, color))
#     return created_shape


def create_shape(shape, color, current_x=GAME_WIDTH // 2 - BLOCK_SIZE, current_y=TOP_LEFT_Y):
    created_shape = []
    rows = len(shape[0]) // 4
    columns = 4
    for i in range(rows):
        for j in range(columns):
            if shape[0][i * columns + j] == "S":
                created_shape.append(Block(current_x + j * BLOCK_SIZE, current_y + i * BLOCK_SIZE,
                                           BLOCK_SIZE, BLOCK_SIZE, color))
    return created_shape


def out_of_bounds_x_left(shape):
    for box in shape:
        if box.x < TOP_LEFT_X:
            return True
    return False


def out_of_bounds_x_right(shape):
    for box in shape:
        if box.x >= TOP_LEFT_X + GAME_WIDTH:
            return True
    return False


def rotate_shape(x, y, shape, shape_rects, color, current_shape_position, background):
    next_position = current_shape_position + 1 if current_shape_position + 1 < len(shape) else 0
    if SHAPES.index(shape) == 4 and next_position == 2 or SHAPES.index(shape) == 5 and next_position == 0:
        x -= BLOCK_SIZE
    new_shape = create_shape(shape[next_position], color, x, y)
    if not out_of_bounds_x_left(new_shape) and not detect_shapes_collision_on_moving_left(background, new_shape) \
            and not out_of_bounds_x_right(new_shape) and not detect_shapes_collision_on_moving_right(background,
                                                                                                     new_shape):
        return new_shape, next_position
    return shape_rects, current_shape_position


def create_background_dict():
    coords_dict = {}
    for i in range(TOP_LEFT_Y, GAME_HEIGHT + TOP_LEFT_Y + BLOCK_SIZE, BLOCK_SIZE):
        coords_dict[i] = []

    return coords_dict


def check_for_line(background):
    new_background = background
    found_line = False
    for y_val, line in background.items():
        if len(line) == GAME_WIDTH / BLOCK_SIZE:
            # print(y_val, line)
            remove_line(y_val, background)
            new_background = move_lines_down(y_val, background)
            found_line = True

    return new_background, found_line


def move_lines_down(y, background):
    for y_val, line in background.items():
        if y > y_val:
            for box in line:
                box.y += BLOCK_SIZE

    new_background = create_background_dict()
    for line in background.values():
        for box in line:
            new_background[box.y].append(box)
    return new_background


def remove_line(y_val, background):
    # debug

    # for y, line in background.items():
    #     for box in line:
    #         if y == y_val:
    #             box.color = 'white'
    #
    # draw_background(background)
    # pygame.display.update()
    # time.sleep(1)
    remove_animation(y_val, background, 'green')
    remove_animation(y_val, background, 'white')
    remove_animation(y_val, background, 'green')

    background[y_val] = []


def remove_animation(y_val, background, color):
    for y, line in background.items():
        for box in line:
            if y == y_val:
                box.color = color

    draw_background(background)
    draw_grid()
    pygame.display.update()
    time.sleep(0.2)


def read_best_score():
    with open("best_score", 'r') as f:
        return f.read()


def save_new_score(score):
    with open("best_score", 'w') as f:
        f.write(str(score))


def get_min_x(current_shape_rects):
    min_x = current_shape_rects[0].x
    for box in current_shape_rects:
        if box.x < min_x:
            min_x = box.x
    return min_x


def can_spawn(background):
    for line in background.values():
        for box1 in line:
            if box1.x == GAME_WIDTH // 2 - BLOCK_SIZE and box1.y <= TOP_LEFT_Y:
                return False
    return True


def reset_game(score, best_score):
    time.sleep(1)
    if score > int(best_score):
        best_score = score
        save_new_score(score)

    background_boxes = create_background_dict()
    current_shape = random.choice(SHAPES)
    next_shape = random.choice(SHAPES)

    return 0, best_score, background_boxes, current_shape, next_shape


def draw_score(score, best_score):
    if score < 10000:
        FONT = pygame.font.SysFont('indigo', 50)
    else:
        FONT = pygame.font.SysFont('indigo', 40)

    if int(best_score) < 10000:
        BEST_FONT = pygame.font.SysFont('indigo', 30)
    else:
        BEST_FONT = pygame.font.SysFont('indigo', 20)

    score_label = FONT.render(f"Score: {score} ", True, "white")
    WINDOW.blit(score_label, (GAME_WIDTH + 3 * BLOCK_SIZE, WINDOW_HEIGHT // 2 - 250))

    best_score_label = BEST_FONT.render(f"Best Score: {best_score} ", True, "white")
    WINDOW.blit(best_score_label, (GAME_WIDTH + 3 * BLOCK_SIZE, WINDOW_HEIGHT - BLOCK_SIZE))


def draw_next_shape(next_shape):
    FONT = pygame.font.SysFont('indigo', 32)
    next_label = FONT.render("NEXT SHAPE: ", True, "white")
    WINDOW.blit(next_label, (GAME_WIDTH + 3 * BLOCK_SIZE, WINDOW_HEIGHT // 2 - next_label.get_height()//2 - 2 * BLOCK_SIZE))

    # pygame.draw.line(WINDOW, 'white', (GAME_WIDTH + 2 * BLOCK_SIZE, WINDOW_HEIGHT // 2 - 150),
    #                  (GAME_WIDTH + 3 * BLOCK_SIZE + 180, WINDOW_HEIGHT // 2 - 150), width=3)
    # pygame.draw.line(WINDOW, 'white', (GAME_WIDTH + 2 * BLOCK_SIZE, WINDOW_HEIGHT // 2),
    #                  (GAME_WIDTH + 3 * BLOCK_SIZE + 180, WINDOW_HEIGHT // 2), width=3)
    #
    # pygame.draw.line(WINDOW, 'white', (GAME_WIDTH + 2 * BLOCK_SIZE, WINDOW_HEIGHT // 2),
    #                  (GAME_WIDTH + 2 * BLOCK_SIZE, WINDOW_HEIGHT // 2 - 150), width=3)
    #
    # pygame.draw.line(WINDOW, 'white', (GAME_WIDTH + 3 * BLOCK_SIZE + 180, WINDOW_HEIGHT // 2),
    #                  (GAME_WIDTH + 3 * BLOCK_SIZE + 180, WINDOW_HEIGHT // 2 - 150), width=3)

    rows = len(next_shape[0][0]) // 4
    columns = 4
    for i in range(rows):
        for j in range(columns):
            if next_shape[0][0][i * columns + j] == "S":
                pygame.draw.rect(WINDOW, COLORS[SHAPES.index(next_shape)],
                                 pygame.Rect(GAME_WIDTH + j * BLOCK_SIZE + (WINDOW_WIDTH - BLOCK_SIZE
                                                                            - GAME_WIDTH) // 2,
                                             WINDOW_HEIGHT // 2 + 50 + i * BLOCK_SIZE - 2 * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))


def draw_grid():
    for i in range(TOP_LEFT_X + BLOCK_SIZE, GAME_WIDTH + TOP_LEFT_X + BLOCK_SIZE, BLOCK_SIZE):
        pygame.draw.line(WINDOW, GRID_COLOR, (i, TOP_LEFT_Y), (i, GAME_HEIGHT + TOP_LEFT_Y), width=3)

    for i in range(TOP_LEFT_Y + BLOCK_SIZE, GAME_HEIGHT + TOP_LEFT_Y + BLOCK_SIZE, BLOCK_SIZE):
        pygame.draw.line(WINDOW, GRID_COLOR, (TOP_LEFT_X, i), (GAME_WIDTH + TOP_LEFT_X, i), width=3)

    pygame.draw.line(WINDOW, BORDER_GRID_COLOR, (TOP_LEFT_X, TOP_LEFT_Y), (GAME_WIDTH + TOP_LEFT_X, TOP_LEFT_Y),
                     width=5)
    pygame.draw.line(WINDOW, BORDER_GRID_COLOR, (TOP_LEFT_X, GAME_HEIGHT + TOP_LEFT_Y),
                     (GAME_WIDTH + TOP_LEFT_X, GAME_HEIGHT
                      + TOP_LEFT_Y), width=5)

    pygame.draw.line(WINDOW, BORDER_GRID_COLOR, (TOP_LEFT_X, TOP_LEFT_Y), (TOP_LEFT_X, GAME_HEIGHT + TOP_LEFT_Y),
                     width=5)
    pygame.draw.line(WINDOW, BORDER_GRID_COLOR, (GAME_WIDTH + TOP_LEFT_X, TOP_LEFT_Y),
                     (GAME_WIDTH + TOP_LEFT_X, GAME_HEIGHT
                      + TOP_LEFT_Y), width=5)


def draw_shape(shape):
    for box in shape:
        rect = pygame.Rect(box.x, box.y, box.width, box.height)
        pygame.draw.rect(WINDOW, box.color, rect)


def draw_background(background):
    for line in background.values():
        for box in line:
            rect = pygame.Rect(box.x, box.y, box.width, box.height)
            pygame.draw.rect(WINDOW, box.color, rect)


def draw(current_shape, background_boxes, next_shape, score, best_score):
    WINDOW.fill(WINDOW_BACKGROUND_COLOR)
    FONT = pygame.font.SysFont('indigo', 65)
    tetris_label = FONT.render("TETRIS", True, "white")
    WINDOW.blit(tetris_label, (WINDOW_WIDTH / 2 - tetris_label.get_width() / 2, TOP_LEFT_Y // 2 -
                               tetris_label.get_height() // 2))

    draw_shape(current_shape)
    draw_background(background_boxes)
    draw_score(score, best_score)

    draw_next_shape(next_shape)
    draw_grid()
    pygame.display.update()


def main():
    score = 0
    best_score = read_best_score()
    run = True
    current_shape_position = 0
    background_boxes = create_background_dict()

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
                if event.key == pygame.K_r:
                    score, best_score, background_boxes, current_shape, next_shape = reset_game(score, best_score)
                    current_shape_rects = create_shape(current_shape[0], COLORS[SHAPES.index(current_shape)])

                if can_move_right(background_boxes, current_shape_rects):
                    if event.key == pygame.K_RIGHT:
                        move_right(current_shape_rects)
                if can_move_left(background_boxes, current_shape_rects):
                    if event.key == pygame.K_LEFT:
                        move_left(current_shape_rects)
                if event.key == pygame.K_DOWN:
                    move_fast_down(current_shape_rects)
                    score += 1
                if event.key == pygame.K_SPACE:
                    score += 20 - (current_shape_rects[0].y - TOP_LEFT_Y) // BLOCK_SIZE
                    move_to_floor(current_shape_rects, background_boxes)

                if event.key == pygame.K_UP:
                    min_x = get_min_x(current_shape_rects)
                    current_shape_rects, current_shape_position = rotate_shape(min_x, current_shape_rects[0].y,
                                                                               current_shape, current_shape_rects,
                                                                               COLORS[SHAPES.index(current_shape)],
                                                                               current_shape_position, background_boxes)
        auto_move_down(current_shape_rects)

        if detect_floor(current_shape_rects) or detect_other_shapes(background_boxes, current_shape_rects):
            for box in current_shape_rects:
                background_boxes[box.y].append(box)

            current_shape = next_shape
            if can_spawn(background_boxes):
                next_shape = random.choice(SHAPES)
                current_shape_position = 0
                current_shape_rects = create_shape(current_shape[0], COLORS[SHAPES.index(current_shape)])
                background_boxes, found_line = check_for_line(background_boxes)
                if found_line:
                    score += 100
            else:
                score, best_score, background_boxes, current_shape, next_shape = reset_game(score, best_score)
                current_shape_rects = create_shape(current_shape[0], COLORS[SHAPES.index(current_shape)])

        draw(current_shape_rects, background_boxes, next_shape, score, best_score)

    if int(score) > int(best_score):
        save_new_score(score)
    pygame.quit()


if __name__ == "__main__":
    main()
