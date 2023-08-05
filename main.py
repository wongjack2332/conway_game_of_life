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

# pylint: disable=no-member

pygame.init()

GRID_X, GRID_Y = 30, 30
GRID_SIZE = 20
WIDTH, HEIGHT = GRID_X * GRID_SIZE, GRID_Y * GRID_SIZE
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

FPS = 3

GRID_COLOUR = (0, 0, 0)


def scan_grid():
    last_grid = copy.deepcopy(grid)
    for y, v in enumerate(last_grid):
        for x, w in enumerate(v):
            neighbours = get_neighbours(x, y, last_grid)
            live = w
            if neighbours == 3 and not live:
                rects.append((x, y))
                grid[y][x] = True
                print(x, y, "added")
            elif (neighbours < 2 or neighbours > 3) and live:
                grid[y][x] = False
                print(x, y, "removed")
                rects.remove((x, y))
    return last_grid


def plot_grid(x, y):
    grid[y][x] = True
    return x, y


def draw_rect(x, y):
    x_coord = x * GRID_SIZE
    y_coord = y * GRID_SIZE
    rect = pygame.Rect(x_coord, y_coord, GRID_SIZE, GRID_SIZE)
    pygame.draw.rect(SCREEN, GRID_COLOUR, rect)


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


grid = [[False for i in range(GRID_X)] for i in range(GRID_Y)]

clock = pygame.time.Clock()

seed = ((1, 1), (2, 2), (2, 3), (1, 3), (0, 3))
rects = [plot_grid(*i) for i in seed]
print(rects)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    SCREEN.fill((255, 255, 255))
    draw_grid(SCREEN)

    for i in rects:
        draw_rect(*i)

    scan_grid()
    pygame.display.update()
    clock.tick(FPS)


# TODO: create graphical control mode
