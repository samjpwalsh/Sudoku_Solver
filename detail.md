**Solving Sudoku Puzzles: Implementation using a Backtracking Depth-First Search with Constraint Satisfaction**

Assignment for the University of Bath as part of MSc in Artificial Intelligence


_**Summary:**_

At a high level, my Sudoku solver is formed of two key components, a Backtracking Depth-First Search algorithm, to 
traverse the tree of different states that the Sudoku could be in, and Constraint Satisfaction, to reduce the size of
the tree. This factored representation of the problem allows us to solve Sudokus much more efficiently than if each 
Sudoku state were treated in an atomic way with Backtracking Depth-First Search alone.

1. **Constraint Satisfaction and Propagation:** This code sets a possible value for a specified cell within the Sudoku grid, 
from a range of possible values that the cell can take. Then for each other cell on the same row, column and 3x3 square, 
the code removes the set value from the possible values that those cells can take. There are separate pieces of code 
which do this both for the setting of initial values (from the Sudoku's starting configuration) and for setting values 
within the Backtracking algorithm, which will be explained in more detail in the Code Walkthrough section. 
Implementing a Constraint Satisfaction component removes a significant number of possible numbers that the Backtracking
algorithm needs to try for each cell, vastly reducing the search space and so improving efficiency.

2. **Backtracking:** My code implements a reasonably standard Backtracking Depth-First Search, using a Minimum-Remaining 
Value heuristic to improve efficiency, as cells with no possible values are identified immediately, removing the
possibility of the algorithm continuing to search a configuration which is guaranteed not to find the goal state. There
are further improvements that could be made to this implementation of Backtracking Search, which I will explore in the
final section.


_**Code Walkthrough:**_

In this section, I will walk through my code systematically, explaining each class and function in turn:

1. **Class: PartialSudoku** - This class is the core of the algorithm, defining the structure which is manipulated
through Constraint Propagation and Backtracking. There are 2 key attributes of instances of the class that should be 
kept in mind, as these are the structures which store the key variables for the algorithm. The first, **self.final_values** 
is a 9x9 numpy array representing the Sudoku puzzle, where each cell has a value of -1 unless a value has been set for 
it by the algorithm. The second, **self.possible_values** is a 9x9x9 numpy array, where the 3rd dimension represents the 
possible values that a cell in the 9x9 grid could take. These values are initially the numbers 1-9 for each cell, but 
Constraint Propagation reduces these possibilities. Both attributes specify dtype=int8, which keeps the space
requirements of the arrays as small as possible (we are only using single digit integers, so do not have to worry about
loss of precision here). Numbers 2-7 below describe functions within the PartialSudoku class, whereas Numbers 8-11 
describe functions outside the class.

2. **Function: is_goal** - This simply checks whether the 9x9 Sudoku grid is complete, ie has a value been assigned to
every square.

3. **Function: is_invalid** - This checks whether any cell has no possible values. Which can only be the case if
constraints have been propagated from other cells such that the state cannot be part of a valid solution

4. **Function: get_final_state** - Returns the final values in a 9x9 array if the sudoku is complete, otherwise returning
a 9x9 grid populated with -1 in each cell, denoting that there is no valid solution, as per the specification.

5. **Function: single_value_cells** - A function which adds efficiency to Constraint Propagation. This function iterates
through the cells to identify cells that have no final value, and exactly one possible value, returning a list of tuples
with the single value cells coordinates on the Sudoku grid. This is used as part of the function below to set those values
without having to expand another node in the Depth-First Search.

6. **Function: set_value** - This function is where value setting and Constraint Propagation takes place. Firstly there
is a failsafe which verifies that the value to be set is part of the possible values for a given cell, then a copy of
the current state of the sudoku is taken (which is necessary to be able to backtrack to earlier points). The possible
and final value of the cell are then updated. For example if we were setting the value of (0,5) = 6, the final value
would be updated to 6, and the possible values would change to a 1x9 array filled with 6's. Once the value is set, this
is propagated to each other cell in the row, column and 3x3 square. This code changes the possible value array of each other
cell, removing the value and replacing it with 0. To maximise efficiency, the process of doing this checks each cell 
only once. When propagating the constraint to the row, the possible values of all cells in the row are 
updated (except the cell for which the value was set). When propagating to the column, the same is done (as the only
place that the row and column overlap is the cell where the value was set). When propagating to the 3x3 square, only cells
which do not share a column or row with the updated cell have their possible values changed (as if they did share a row or
column, the possible values would already have been updated).
The final part of this function identifies any cells which, as a result of constraint propagation, now only have one possible
value. These cells are updated and constraints propagated in the same way, which reduces the search space for the Backtracking
algorithm.

7. **Function: set_value_initial** - This function is the same as the one above, but is only used to set values and 
propagate constraints of the starting Sudoku array (ie to provide a starting point for the algorithm).

8. **Function: pick_cell** - From now on, these functions are not part of the PartialSudoku class, but are used in the
Backtracking Depth-First Search algorithm. This function narrows the range of nodes for the algorithm to choose next
by identifying the cell with the fewest remaining possible values. (This implements the Minimum-Remaining Value 
heuristic described in the first section).

9. **Function: order_values** - Once a cell has been chosen, this function defines which node the algorithm should
choose first by selecting a possible value for the cell. In this implementation, this function does not order the values based on
any heuristic, it leaves the (nonzero) values as they are ordered (which in practice will be the low to high). This could
be randomised or a heuristic chosen to improve future performance, which will form part of the next section.

10. **Function: depth_first_search** - This is a recursive function that does most of the heavy lifting. Initially a cell
and values are picked using the two functions above, then the first possible value for that cell is tried 
(and constraints propagated etc as per the set_value function), if the state is valid (ie no cell has 0 possible values),
then this will run again, picking the next cell and trying a value, and so on until either a goal state is found, 
or an invalid state is reached, at which point the algorithm backtracks to the last state that was valid, and tries another value.
This continues until a goal state is found (which will be returned), or no valid state is found after all possible values are tried,
in which case the function returns None.

11. **Function: sudoku_solver** - This function brings together all the elements, first checking if the array passed in
to the function is a valid board (9x9 and only empty squares or numbers 1-9), then setting up a PartialSudoku instance
with the initial values from the board passed in (which returns a 9x9 array filled with -1 if the starting board can
be identified as invalid immediately). Then the Backtracking Depth First Search is performed. If the output is None, then
the 9x9 array of -1s is returned, otherwise the goal state is returned.

_**Results and further improvements:**_

From the test Sudokus given, on my PC almost all the very easy to medium boards are solved within 0.015 seconds each. The
hard Sudokus take longer, with hard Sudoku 14 taking the longest at approximately 4.1 seconds. The combination of
Backtracking Depth-First Search with Constraint Satisfaction appears to be a very efficient way of solving these problems,
but there are a couple of areas where I would like to develop and improve my implementation:

1. **order_values:** When deciding on the order in which the algorithm chooses values for a particular cell, I could use
a Least-Constraining value heuristic, which would choose the value which removes the fewest possible values from other
cells. This may increase efficiency as values that constrain other values less are more likely to be correct.

2. **depth_first_search:** My algorithm is an implementation of chronological backtracking, whereby if a value chosen leads
to an invalid state, the algorithm backtracks to the last valid state and continues on. I could make an improvement here
with a Backjumping algorithm by maintaining a set of conflicting assignments for each variable. When an invalid 
state is reached, rather than going back to the last valid state, the algorithm would then go back instead to the last 
state where a conflicting variable was assigned.


