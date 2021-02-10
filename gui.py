#!/usr/bin/python3
import pygame
import pygame.display
import pygame.draw
import pygame.font
from pygame.locals import *

from solver import Solver

# screen variables
CELLSIZE_BASE = 9
CELLSIZE_MULTIPLIER = 5
CELLSIZE = CELLSIZE_BASE * CELLSIZE_MULTIPLIER
BLOCKSIZE = CELLSIZE * 3
GRIDSIZE_X = 9 * CELLSIZE_BASE * CELLSIZE_MULTIPLIER
GRIDSIZE_Y = 9 * CELLSIZE_BASE * CELLSIZE_MULTIPLIER
# color variables
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHTGRAY = (190, 198, 212)
DARKGRAY = (226, 231, 237)
BLUE = (187, 222, 251)
# example grid data
EXAMPLE_DATA = [
    [0, 9, 0, 0, 0, 0, 5, 3, 0],
    [7, 0, 0, 8, 1, 0, 0, 4, 0],
    [0, 0, 0, 5, 0, 0, 8, 0, 7],
    [0, 0, 4, 0, 6, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 7, 0, 3],
    [0, 0, 7, 4, 5, 0, 9, 6, 2],
    [9, 4, 0, 0, 0, 6, 1, 8, 0],
    [0, 0, 6, 0, 8, 2, 0, 0, 0],
]


class Grid:
    def __init__(self, screen) -> None:
        self.screen = screen
        self.font = pygame.font.Font(None, 28)
        self.data = self.data = [[0 for _ in range(9)] for _ in range(9)]
        self.data_recovery = None

        self.rectangles = [
            [
                pygame.Rect(x * CELLSIZE, y * CELLSIZE, CELLSIZE, CELLSIZE)
                for x in range(9)
            ]
            for y in range(9)
        ]

    def draw_numbers(self):
        for y in range(9):
            for x in range(9):
                value = self.data[y][x]
                if value != 0:
                    text = self.font.render(str(value), True, BLACK)
                    rect = self.rectangles[y][x]
                    text_rect = text.get_rect(center=(rect.centerx, rect.centery))
                    self.screen.blit(text, text_rect)

    def draw_lines(self):
        screen = self.screen
        # draw thin lines
        for x in range(CELLSIZE, GRIDSIZE_X, CELLSIZE):
            pygame.draw.line(screen, LIGHTGRAY, (x, 0), (x, GRIDSIZE_Y))
        for y in range(CELLSIZE, GRIDSIZE_Y, CELLSIZE):
            pygame.draw.line(screen, LIGHTGRAY, (0, y), (GRIDSIZE_X, y))

        # draw thick lines
        for x in range(0, GRIDSIZE_X + BLOCKSIZE, BLOCKSIZE):
            pygame.draw.line(screen, BLACK, (x, 0), (x, GRIDSIZE_Y), width=2)
        for y in range(0, GRIDSIZE_Y + BLOCKSIZE, BLOCKSIZE):
            pygame.draw.line(screen, BLACK, (0, y), (GRIDSIZE_X, y), width=2)

    def highlight_selected(self, field):
        x, y = field
        selected_rect = self.rectangles[y][x]
        pygame.draw.rect(self.screen, BLUE, selected_rect)

    def highlight_locked(self):
        for y in range(9):
            for x in range(9):
                if self.data_recovery[y][x] != 0:
                    locked_rect = self.rectangles[y][x]
                    pygame.draw.rect(self.screen, DARKGRAY, locked_rect)

    def reset_data(self):
        self.data = [[0 for _ in range(9)] for _ in range(9)]


def calc_selection(current_field, movement):
    x = current_field[0] + movement[0]
    y = current_field[1] + movement[1]
    if 0 <= x <= 8 and 0 <= y <= 8:
        return (x, y)
    else:
        while not (0 <= x <= 8) or not (0 <= y <= 8):
            if x >= 8 and y >= 8:
                x, y = 0, 0
            elif x <= 0 and y <= 0:
                x, y = 8, 8
            elif x > 8:
                x, y = 0, y + 1
            elif y > 8:
                x, y = x + 1, 0
            elif x < 0:
                x, y = 8, y - 1
            elif y < 0:
                x, y = x - 1, 8
        return (x, y)


def main():
    # initialize pygame
    pygame.init()
    pygame.display.set_caption("Sudoku Solver")

    # create screen
    screen = pygame.display.set_mode((GRIDSIZE_X + 2, GRIDSIZE_Y + 2))
    screen.fill((255, 255, 255))

    # setup variables
    running = True
    grid = Grid(screen)
    solver = None
    selection = None

    # setup event dictionaries
    keys_num = {
        K_0: 0,
        K_1: 1,
        K_2: 2,
        K_3: 3,
        K_4: 4,
        K_5: 5,
        K_6: 6,
        K_7: 7,
        K_8: 8,
        K_9: 9,
        K_KP0: 0,
        K_KP1: 1,
        K_KP2: 2,
        K_KP3: 3,
        K_KP4: 4,
        K_KP5: 5,
        K_KP6: 6,
        K_KP7: 7,
        K_KP8: 8,
        K_KP9: 9,
        K_BACKSPACE: 0,
        K_DELETE: 0,
    }
    keys_cmd = {
        K_ESCAPE: "cancel",
        K_RETURN: "fast",
        K_KP_ENTER: "fast",
        K_SPACE: "slow",
        K_r: "reset",
        K_e: "example",
    }
    keys_nav = {
        K_UP: (0, -1),
        K_DOWN: (0, 1),
        K_LEFT: (-1, 0),
        K_RIGHT: (1, 0),
        K_TAB: (1, 0),
    }

    # start main loop
    while running:
        # handle events
        for event in pygame.event.get():
            # quit
            if event.type == pygame.QUIT:
                running = False
                if solver:
                    solver.stop()
            # mouse selection
            if event.type == pygame.MOUSEBUTTONDOWN and not solver:
                # Set the x, y postions of the mouse click
                x, y = event.pos
                if x < GRIDSIZE_X and y < GRIDSIZE_Y:
                    x = x // (CELLSIZE_BASE * CELLSIZE_MULTIPLIER)
                    y = y // (CELLSIZE_BASE * CELLSIZE_MULTIPLIER)
                    if selection == (x, y):
                        selection = None
                    else:
                        selection = (x, y)
            # keypress
            if event.type == KEYDOWN:
                # press number
                if event.key in keys_num and selection and not solver:
                    x, y = selection
                    grid.data[y][x] = keys_num[event.key]
                # press command
                elif event.key in keys_cmd:
                    if keys_cmd[event.key] == "fast" and not solver:
                        grid.data_recovery = grid.data[:]
                        selection = None
                        solver = Solver(grid.data)
                        solver.start()
                    elif keys_cmd[event.key] == "slow" and not solver:
                        grid.data_recovery = grid.data[:]
                        selection = None
                        solver = Solver(grid.data, slow=True)
                        solver.start()
                    elif (
                        keys_cmd[event.key] == "cancel"
                        and solver
                        and grid.data_recovery
                    ):
                        solver.stop()
                        solver.join()
                        solver = None
                        grid.data = grid.data_recovery[:]
                        grid.data_recovery = None
                    elif keys_cmd[event.key] == "reset" and not solver:
                        grid.reset_data()
                    elif keys_cmd[event.key] == "example" and not solver:
                        grid.data = EXAMPLE_DATA
                # press navigation
                elif event.key in keys_nav and not solver:
                    if selection is None:
                        selection = (0, 0)
                    else:
                        if event.key == K_TAB and event.mod & KMOD_SHIFT:
                            selection = calc_selection(selection, (-1, 0))
                        else:
                            selection = calc_selection(selection, keys_nav[event.key])

        # redraw screen
        screen.fill(WHITE)
        if selection:
            grid.highlight_selected(selection)
        if solver:
            grid.data = solver.solution
            grid.highlight_locked()
            if solver.field:
                grid.highlight_selected((solver.field[1], solver.field[0]))
        if solver and not solver.is_alive():
            solver = None
        grid.draw_numbers()
        grid.draw_lines()
        pygame.display.update()


# running gui as main
if __name__ == "__main__":
    main()
