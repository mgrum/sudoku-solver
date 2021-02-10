#!/usr/bin/python3
import os
import sys

from solver import Solver


def check_rows(lines):
    grid = []
    for line in lines:
        try:
            numbers = [int(n) for n in line.strip().split()]
        except ValueError:
            # line is not made of numbers
            return None
        if not len(numbers) == 9:
            # line is not exactly 9 numbers
            return None
        grid.append(numbers)
    return grid


def get_grids(lines):
    grids = dict()
    idx = 0
    while idx < len(lines) - 8:
        grid = check_rows(lines[idx : idx + 9])
        if grid:
            # save grid with line number (idx) where it starts
            grids[idx] = grid
            # skip the processed lines of the grid
            idx += 9
        else:
            idx += 1
    return grids


def write_solution(filename: str, lines, solutions):
    filename_split = list(os.path.split(os.path.abspath(filename)))
    filename_split[-1] = "Solution_" + filename_split[-1]
    filename = os.path.join(filename_split[0], filename_split[1])
    # replace unsolved grids with solved grids
    for idx_start, grid in solutions.items():
        for idx in range(len(grid)):
            lines[idx_start + idx] = " ".join(map(str, grid[idx]))
            # lines[idx_start + idx] = grid[idx]  # debugging purposes
    # save file in same format as original file
    print("Writing solutions to: " + filename)
    with open(filename, "w") as file:
        for line in lines:
            if "\n" in line:
                file.write(line)
            else:
                file.write("%s\n" % line)


def main(args):
    solutions = dict()
    count_f = 0
    if args:
        for filename in args:
            count_f += 1
            print("Start solving file " + str(count_f) + "/" + str(len(args)))
            with open(filename) as file:
                lines = file.readlines()
                grids = get_grids(lines)

                # create solver threads
                solvers = {idx: Solver(grid) for idx, grid in grids.items()}
                # wait for all threads to complete solving
                count_g = 0
                for solver in solvers.values():
                    solver.start()
                for solver in solvers.values():
                    solver.join()
                    count_g += 1
                    print(
                        filename
                        + " "
                        + str(count_g)
                        + "/"
                        + str(len(grids))
                        + " solved."
                    )
                # replace grids with solved grids
                grids = {idx: solver.solution for idx, solver in solvers.items()}

                write_solution(filename, lines, grids)


# running cli as main
if __name__ == "__main__":
    main(sys.argv[1:])
