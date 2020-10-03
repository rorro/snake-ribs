from ribs import *
from dataclasses import dataclass
import random

# Asset dictionary for holding all your assets.
assets = {}
PART_WIDTH = 10

def clamp(val, low, high):
    return min(max(val, low), high)

@dataclass
class Corner:
    x: int
    y: int

@dataclass
class Snake:
    apple_pos: tuple
    corners = [Corner(100, 100), Corner(100, 150)]
    direction = (0, 1)
    speed = 150

def spawn_apple(size):
    x = random.randint(0, size[0]) - PART_WIDTH
    y = random.randint(0, size[1]) - PART_WIDTH

    return x, y

def draw_apple(snake):
    window = pg.display.get_surface()
    pg.draw.circle(window, pg.Color(255, 0, 0), snake.apple_pos, PART_WIDTH)

def update_snake(snake, delta):
    new_direction = snake.direction

    if key_pressed("w") or key_pressed(pg.K_UP):
        if snake.direction != (0, 1):
            new_direction = (0, -1)
    elif key_pressed("a") or key_pressed(pg.K_LEFT):
        if snake.direction != (1, 0):
            new_direction = (-1, 0)
    elif key_pressed("s") or key_pressed(pg.K_DOWN):
        if snake.direction != (0, -1):
            new_direction = (0, 1)
    elif key_pressed("d") or key_pressed(pg.K_RIGHT):
        if snake.direction != (-1, 0):
            new_direction = (1, 0)

    if new_direction != snake.direction:
        snake.corners.append(Corner(snake.corners[-1].x, snake.corners[-1].y))
        snake.direction = new_direction

    # update head
    snake.corners[-1].x += int(snake.direction[0] * snake.speed * delta)
    snake.corners[-1].y += int(snake.direction[1] * snake.speed * delta)

    # update tail
    snake.corners[0].x += int(clamp(snake.corners[1].x - snake.corners[0].x, -1, 1) * snake.speed * delta)
    snake.corners[0].y += int(clamp(snake.corners[1].y - snake.corners[0].y, -1, 1) * snake.speed * delta)

    if snake.corners[0].x == snake.corners[1].x and snake.corners[0].y == snake.corners[1].y:
        del snake.corners[0]

    if got_apple(snake):
        snake.apple_pos = spawn_apple(pg.display.get_window_size())
        if snake.corners[1].x > snake.corners[0].x:
            snake.corners[0].x -= 50
        elif snake.corners[1].x < snake.corners[0].x:
            snake.corners[0].x += 50
        elif snake.corners[1].y > snake.corners[0].y:
            snake.corners[0].y -= 50
        elif snake.corners[1].y < snake.corners[0].y:
            snake.corners[0].y += 50

def got_apple(snake):
    dx = snake.apple_pos[0] - snake.corners[-1].x
    dy = snake.apple_pos[1] - snake.corners[-1].y

    return abs(dx) < PART_WIDTH and abs(dy) < PART_WIDTH


def draw_snake(snake):
    window = pg.display.get_surface()

    r = random.randint(0,255)
    g = random.randint(0,255)
    b = random.randint(0,255)
    col = (r,g,b)

    for a,b in zip(snake.corners, snake.corners[1:]):

        if a.y - b.y == 0 and b.x > a.x:
            pg.draw.rect(window,pg.Color(col),
                        (a.x - PART_WIDTH/2, a.y - PART_WIDTH/2, b.x-a.x, PART_WIDTH))

        if a.y - b.y == 0 and b.x < a.x:
            pg.draw.rect(window,pg.Color(col),
                        (b.x - PART_WIDTH/2, a.y - PART_WIDTH/2, a.x-b.x, PART_WIDTH))

        elif a.x - b.x == 0 and b.y > a.y:
            pg.draw.rect(window,pg.Color(col),
                        (a.x - PART_WIDTH/2, a.y - PART_WIDTH/2, PART_WIDTH, b.y-a.y))

        elif a.x - b.x == 0 and b.y < a.y:
            pg.draw.rect(window,pg.Color(col),
                        (a.x - PART_WIDTH/2, b.y - PART_WIDTH/2, PART_WIDTH, a.y-b.y))



def init():
    pass

def update():
    """The program starts here"""
    # Initialization (only runs on start/restart)
    snake = Snake(spawn_apple(pg.display.get_window_size()))

    # Main update loop
    while True:
        update_snake(snake, delta())
        draw_snake(snake)
        draw_apple(snake)

        # Main loop ends here, put your code above this line
        yield


# This has to be at the bottom, because of python reasons.
if __name__ == "__main__":
   start_game(init, update)
