"""
    created by Jack Wong
`   2023-07-26
----------------------------------------------------------------
Conway Game of Life

Rules:
1. Any live cell with fewer than two live neighbours dies, as if by underpopulation.
2. Any live cell with two or three live neighbours lives on to the next generation.
3. Any live cell with more than three live neighbours dies, as if by overpopulation.
4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.

Sketch:
func plot_grid(x, y) plots to coordinate of grid based on grid size and xy coordinates
    fill space with a rect
    populate space on 2D array for the grid
function get_neighbours(x, y) returns number of neighbours for given grid coordinate

TODO:
- optimise, is it necessary to scan all cells for neighbours?
    IDEA: only need to scan all neighbouring cells of live cells
    - optimisation of neighbour search as well

"""


import pygame
import sys
import copy
import random

# pylint: disable=no-member

pygame.init()

GRID_X, GRID_Y = 30, 30
GRID_SIZE = 20
WIDTH, HEIGHT = GRID_X * GRID_SIZE, GRID_Y * GRID_SIZE
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
STEP = pygame.USEREVENT + 1
SIMULATION_FPS = 5
KEY_LAG_MS = 500

FPS = 60

GRID_COLOUR = (0, 0, 0)


def delay():
    pygame.time.delay(KEY_LAG_MS)


def set_seed():
    # mouse_states = pygame.mouse.get_pressed()
    # if mouse_states[0]:
    mouse_pos = pygame.mouse.get_pos()
    x, y = mouse_pos[0] // GRID_SIZE, mouse_pos[1] // GRID_SIZE
    grid[y][x] = not grid[y][x]
    if grid[y][x]:
        rects.append((x, y))
    else:
        rects.remove((x, y))
    # delay()'


def randomize_array():
    for i, v in enumerate(grid):
        for j in range(len(v)):
            grid[i][j] = random.randint(0, 1)
            if grid[i][j] == 1:
                rects.append((j, i))
    print(grid)


def scan_grid():
    last_grid = copy.deepcopy(grid)
    for y, v in enumerate(last_grid):
        for x, w in enumerate(v):
            neighbours = get_neighbours(x, y, last_grid)
            live = w
            if neighbours == 3 and not live:
                rects.append((x, y))
                grid[y][x] = True
            elif (neighbours < 2 or neighbours > 3) and live:
                grid[y][x] = False
                rects.remove((x, y))
    # return last_grid


def plot_grid(x, y):
    grid[y][x] = True
    return x, y


def draw_rect(x, y):
    x_coord = x * GRID_SIZE
    y_coord = y * GRID_SIZE
    rect = pygame.Rect(x_coord, y_coord, GRID_SIZE, GRID_SIZE)
    pygame.draw.rect(SCREEN, GRID_COLOUR, rect)


def get_mode(start_simulation):
    keys = pygame.key.get_pressed()

    if keys[pygame.K_RETURN]:
        start_simulation = not start_simulation
        delay()
    return start_simulation


def get_neighbours(x, y, G):
    counts = 0
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if (
                not (dx == 0 and dy == 0)
                and x + dx in range(GRID_X)
                and y + dy in range(GRID_Y)
                and G[y + dy][x + dx]
            ):
                counts += 1
    return counts


def draw_grid(screen):
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(screen, GRID_COLOUR, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, GRID_COLOUR, (0, y), (WIDTH, y))


start_simulation = False
grid = [[False for i in range(GRID_X)] for i in range(GRID_Y)]

pygame.time.set_timer(STEP, 1000 // SIMULATION_FPS)

clock = pygame.time.Clock()
rects = []

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == STEP and start_simulation:
            scan_grid()
        if event.type == pygame.MOUSEBUTTONUP and not start_simulation:
            set_seed()
            # randomize_array()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                randomize_array()

    SCREEN.fill((255, 255, 255))
    draw_grid(SCREEN)

    for i in rects:
        draw_rect(*i)

    # if not start_simulation:
    #     set_seed()
    start_simulation = get_mode(start_simulation)
    pygame.display.update()
    clock.tick(FPS)
