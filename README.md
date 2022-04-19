# Sudoku Solver

- This algorithm takes a 9x9 numpy array as input, if the array is a valid and solvable sudoku puzzle (with zeros in place of blank cells) it returns the solved puzzle, otherwise it returns a 9x9 array of zeros.
- The algorithm uses a backtracking depth first search, along with constraint satisfaction to find a valid solution.
