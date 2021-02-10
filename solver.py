#!/usr/bin/python3
import threading
import time

import numpy as np

SLEEPTIME = 0.01


class Solver(threading.Thread):
    def __init__(self, grid, slow=False):
        super().__init__()
        self.grid = np.asarray(grid).reshape((9, 9))
        self.grid_solvable = self.grid == 0
        solvable_fields = np.where(self.grid_solvable == True)
        self.solvables = list(zip(solvable_fields[0], solvable_fields[1]))
        if self.solvables:
            self.field_start = self.solvables[0]
            self.field_end = self.solvables[-1]
            self.field = self.field_start
        else:
            self.field = None
        self.slow = slow
        self.stopped = threading.Event()

    def run(self):
        while self.field and not self.stopped.is_set():

            value = self.grid[self.field[0], self.field[1]]
            # if value was already 9 when backtracking, backtrack again
            if value == 9:
                self.grid[self.field[0], self.field[1]] = 0
                self.field = self.get_solvable(next=False)
            
            row = self.get_row(self.field)
            column = self.get_column(self.field)
            block = self.get_block(self.field)

            for n in range(value + 1, 10):

                # slow mode
                if self.slow:
                    time.sleep(SLEEPTIME)

                # check sudoku rules
                if n not in row and n not in column and n not in block:
                    self.grid[self.field[0], self.field[1]] = n
                    self.field = self.get_solvable(next=True)
                    break
                elif n == 9:  # no number works here → backtrack
                    self.grid[self.field[0], self.field[1]] = 0
                    self.field = self.get_solvable(next=False)
                    break

                # just used for visualization in gui
                self.grid[self.field[0], self.field[1]] = n

    def stop(self):
        self.stopped.set()

    @property
    def solution(self):
        return self.grid.tolist()

    def get_solvable(self, next=True):
        # get the next/previous solvable field
        idx = self.solvables.index(self.field)
        if next and idx != len(self.solvables) - 1:
            return self.solvables[idx + 1]
        elif not next and idx != 0:
            return self.solvables[idx - 1]
        # return None if idx not in self.solvables → unsolvable or already solved
        return None

    def get_row(self, field):
        return self.grid[field[0], 0:9]

    def get_column(self, field):
        return self.grid[0:9, field[1]]

    def get_block(self, field):
        block = (field[0] // 3, field[1] // 3)
        return self.grid[
            block[0] * 3 : block[0] * 3 + 3, block[1] * 3 : block[1] * 3 + 3
        ]


# running solver as main
if __name__ == "__main__":
    example_grid = [
        [0, 2, 7, 0, 5, 0, 0, 1, 3],
        [9, 1, 5, 0, 0, 0, 6, 0, 7],
        [0, 8, 3, 0, 1, 0, 0, 0, 0],
        [0, 6, 0, 1, 2, 9, 0, 3, 0],
        [0, 3, 2, 8, 0, 5, 4, 7, 0],
        [5, 0, 8, 3, 0, 4, 0, 0, 0],
        [0, 0, 1, 2, 0, 0, 0, 0, 5],
        [0, 0, 0, 0, 8, 1, 0, 2, 6],
        [0, 0, 0, 7, 4, 0, 8, 0, 0],
    ]
    solver = Solver(example_grid)
    solver.start()
    solver.join()
    print("Solution of example:")
    print(solver.grid)
