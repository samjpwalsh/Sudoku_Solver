import numpy as np
import copy

class PartialSudoku:

    def __init__(self):
        self.final_values = np.full((9, 9), -1, dtype=np.int8)
        self.possible_values = np.full((9, 9, 9), range(1, 10), dtype=np.int8)

    def is_goal(self):
        return all(value != -1 for value in np.nditer(self.final_values))

    def is_invalid(self):
        for i in range(9):
            for j in range(9):
                if all(value == 0 for value in self.possible_values[i][j]):
                    return True

    def get_final_state(self):
        if self.is_goal():
            return self.final_values
        else:
            return np.full((9, 9), -1, dtype=np.int8)

    def single_value_cells(self):
        cells = []
        for row_index in range(9):
            for column_index in range(9):
                if np.count_nonzero(self.possible_values[row_index][column_index]) == 1 and \
                        self.final_values[row_index][column_index] == -1:
                    cells.append((row_index, column_index))
        return cells

    def set_value(self, row, column, value):
        if value not in self.possible_values[row][column]:
            return None

        state = copy.deepcopy(self)
        # update final value
        state.possible_values[row][column] = np.array(value)
        state.final_values[row][column] = np.array(value)
        # propagate to row
        for i in [x for x in range(9) if x != column]:
            state.possible_values[row][i] = np.where(state.possible_values[row][i] == value, 0,
                                                     state.possible_values[row][i])

        # propagate to column
        for i in [x for x in range(9) if x != row]:
            state.possible_values[i][column] = np.where(state.possible_values[i][column] == value, 0,
                                                        state.possible_values[i][column])

        # propagate to 3x3 grid
        for i in [x for x in range(9) if x // 3 == row // 3 and x != row]:
            for j in [y for y in range(9) if y // 3 == column // 3 and y != column]:
                state.possible_values[i][j] = np.where(state.possible_values[i][j] == value, 0,
                                                       state.possible_values[i][j])

        # update final values for cells with only one possible value
        for cell in state.single_value_cells():
            if np.count_nonzero(state.possible_values[cell[0]][cell[1]]) != 0:
                row = cell[0]
                column = cell[1]
                value = state.possible_values[cell[0]][cell[1]][np.nonzero(state.possible_values[cell[0]][cell[1]])]
                # update final value
                state.possible_values[row][column] = np.array(value)
                state.final_values[row][column] = np.array(value)
                # propagate to row
                for i in [x for x in range(9) if x != column]:
                    state.possible_values[row][i] = np.where(state.possible_values[row][i] == value, 0,
                                                             state.possible_values[row][i])
                # propagate to column
                for i in [x for x in range(9) if x != row]:
                    state.possible_values[i][column] = np.where(state.possible_values[i][column] == value, 0,
                                                                state.possible_values[i][column])
                # propagate to 3x3 grid
                for i in [x for x in range(9) if x // 3 == row // 3 and x != row]:
                    for j in [y for y in range(9) if y // 3 == column // 3 and y != column]:
                        state.possible_values[i][j] = np.where(state.possible_values[i][j] == value, 0,
                                                               state.possible_values[i][j])

        return state

    def set_value_initial(self, row, column, value):
        if value not in self.possible_values[row][column]:
            return None

        state = copy.deepcopy(self)
        # update final value
        state.possible_values[row][column] = np.array(value)
        state.final_values[row][column] = np.array(value)
        # propagate to row
        for i in [x for x in range(9) if x != column]:
            state.possible_values[row][i] = np.where(state.possible_values[row][i] == value, 0,
                                                     state.possible_values[row][i])

        # propagate to column
        for i in [x for x in range(9) if x != row]:
            state.possible_values[i][column] = np.where(state.possible_values[i][column] == value, 0,
                                                        state.possible_values[i][column])

        # propagate to 3x3 grid
        for i in [x for x in range(9) if x // 3 == row // 3 and x != row]:
            for j in [y for y in range(9) if y // 3 == column // 3 and y != column]:
                state.possible_values[i][j] = np.where(state.possible_values[i][j] == value, 0,
                                                       state.possible_values[i][j])

        return state

def pick_cell(partial_sudoku):
    candidate_cells = []
    for i in range(9):
        for j in range(9):
            if partial_sudoku.final_values[i][j] == -1:
                candidate_cells.append((i, j))

    if candidate_cells == []:
        return False

    min_value_cell = candidate_cells[0]

    for cell in candidate_cells:
        if np.count_nonzero(partial_sudoku.possible_values[cell[0]][cell[1]]) < np.count_nonzero(
                partial_sudoku.possible_values[min_value_cell[0]][min_value_cell[1]]):
            min_value_cell = cell
    return min_value_cell

def order_values(partial_sudoku, row, column):
    values = partial_sudoku.possible_values[row][column][partial_sudoku.possible_values[row][column] != 0]
    return values

def depth_first_search(partial_sudoku):

    cell = pick_cell(partial_sudoku)
    if not cell:
        return partial_sudoku

    values = order_values(partial_sudoku, cell[0], cell[1])

    for value in values:
        updated_state = partial_sudoku.set_value(cell[0], cell[1], value)
        if updated_state.is_goal():
            return updated_state
        if not updated_state.is_invalid():
            deep_state = depth_first_search(updated_state)
            if deep_state is not None and deep_state.is_goal():
                return deep_state
    return None

def sudoku_solver(sudoku):
    if np.size(sudoku, axis=0) != 9 or np.size(sudoku, axis=1) != 9:
        raise ValueError("Invalid starting Sudoku grid size")
    for value in np.nditer(sudoku):
        if value > 9 or value < 0:
            raise ValueError("Starting Sudoku contains numbers other than 0-9")
    setup_sudoku = PartialSudoku()
    for i in range(9):
        for j in range(9):
            if sudoku[i][j] != 0:
                if setup_sudoku is not None:
                    setup_sudoku = setup_sudoku.set_value_initial(i, j, sudoku[i][j])
                else:
                    return PartialSudoku().get_final_state()

    sudoku_in_progress = depth_first_search(setup_sudoku)
    if sudoku_in_progress is not None:
        solved_sudoku = sudoku_in_progress.get_final_state()
    else:
        return PartialSudoku().get_final_state()

    return solved_sudoku


# testing

if __name__ == "__main__":

    # Easy Sudoku
    sudoku_test_1 = np.array([[0, 0, 0, 3, 2, 8, 7, 1, 9],
                     [3, 8, 7, 9, 1, 6, 4, 5, 2],
                     [2, 9,1, 4, 5, 7, 6, 3, 8],
                     [5, 6, 3, 2, 9, 1, 8, 7, 4],
                     [0, 7, 8, 6, 4, 5, 1, 2, 3],
                     [1, 2, 4, 8, 7, 3, 5, 9, 6],
                     [7, 3, 9, 5, 6, 4, 2, 8, 1],
                     [8, 5, 6, 1, 3, 2, 9, 0, 7],
                     [4, 1, 2, 7, 8, 9, 3, 6, 5]])

    # Medium Sudoku
    sudoku_test_2 = np.array([[0, 8, 5, 0, 1, 3, 0, 0, 9],
                              [6, 3, 4, 0, 0, 2, 1, 7, 5],
                              [0, 2, 0, 5, 7, 4, 0, 3, 0],
                              [2, 4, 8, 3, 6, 7, 9, 5, 1],
                              [9, 6, 0, 4, 5, 8, 0, 2, 3],
                              [3, 5, 7, 2, 0, 0, 4, 8, 0],
                              [5, 7, 3, 1, 0, 0, 8, 9, 2],
                              [4, 9, 6, 0, 2, 5, 3, 1, 0],
                              [8, 1, 2, 0, 3, 9, 5, 6, 4]])
    
    # Hard Sudoku
    sudoku_test_3 = np.array([[9, 0, 7, 0, 0, 0, 6, 5, 1],
                              [1, 0, 5, 0, 9, 0, 0, 8, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 5, 0, 4, 0, 0, 0, 0, 0],
                              [0, 2, 0, 0, 0, 0, 0, 4, 0],
                              [0, 0, 1, 0, 0, 6, 0, 0, 0],
                              [0, 0, 8, 6, 0, 0, 0, 3, 0],
                              [0, 0, 4, 1, 0, 0, 9, 0, 0],
                              [0, 0, 9, 0, 5, 0, 0, 6, 0]])

    print(sudoku_solver(sudoku_test_1))
    print("\n")
    print(sudoku_solver(sudoku_test_2))
    print("\n")
    print(sudoku_solver(sudoku_test_3))
