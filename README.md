# Sudoku Solver

This is a Sudoku solver using a backtracking algorithm in python.

It comes as a **command-line-interface (cli)** version or a **graphical-user-interface (gui)** version.

Requirements:
* Python 3.6+
* Pygame
* Numpy

## GUI

Start the gui application with:

<pre>
python gui.py
</pre>

Interaction with the GUI:
* Navigate in the Sudoku grid with **mouse clicks**, **arrow keys** or **TAB**
* Enter numbers in the selected cell with **0-9**
* Load a given example Sudoku with **E**
* Reset the Sudoku grid with **R**
* Solve the Sudoku fast with **RETURN**/**ENTER**
* Solve the Sudoku slow with **SPACEBAR**
* Cancel ongoing solving with **ESC**

**Important information:**

The GUI will noch check for valid input, so the application will try to solve any given Sudoku until it finds a solution or all possible values have been tried (this can take a long time for unsolvable input).

## CLI

The cli version can solve multiple Sudokus of multiple files. The filenames must be arguments when starting the application.

Start the cli application with:
<pre>
python cli.py <b>data/examples_1.txt data/examples_2.txt</b>
</pre>

The input data must be formated like this:

<pre>
Easy (any text can be here)
0 2 7 0 5 0 0 1 3
9 1 5 0 0 0 6 0 7
0 8 3 0 1 0 0 0 0 
0 6 0 1 2 9 0 3 0
0 3 2 8 0 5 4 7 0
5 0 8 3 0 4 0 0 0
0 0 1 2 0 0 0 0 5
0 0 0 0 8 1 0 2 6
0 0 0 7 4 0 8 0 0

Medium (as long as the grids are seperated)
0 9 0 0 0 0 5 3 0
7 0 0 8 1 0 0 4 0
...
</pre>

The cli application will write a new file with solved Sudokus in the same directory as the input files (e.g. `data\Solution_examples_1.txt`).