from utils import *

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
diagonals = [[r + c for r, c in zip(rows, cols)], [r + c for r, c in zip(rows[::-1], cols)]]
unitlist = row_units + column_units + square_units + diagonals

# TODO: Update the unit list to add the new diagonal units
unitlist = unitlist

# Must be called after all units (including diagonals) are added to the unitlist
units = extract_units(unitlist, boxes)
peers = extract_peers(units, boxes)


def grid2values(grid):
    """Convert grid string into {<box>: <value>} dict with '.' value for empties.

    Args:
        grid: Sudoku grid in string form, 81 characters long
    Returns:
        Sudoku grid in dictionary form:
        - keys: Box labels, e.g. 'A1'
        - values: Value in corresponding box, e.g. '8', or '.' if it is empty.
    """
    di = dict()
    for i in range(len(boxes)):
        if grid[i] == '.':
            di[boxes[i]] = '123456789'
        else:
            di[boxes[i]] = grid[i]
    return di


def naked_twins(values):
    origin = values.copy()
    for i in boxes:
        for p in peers[i]:
            if sorted(origin[i]) == sorted(origin[p]) and len(origin[i]) == 2:
                for t in set(peers[i]).intersection(peers[p]):
                    for digit in origin[i]:
                        values[t] = values[t].replace(digit, '')
                        # print(display(values))
                        # print('box::'+i, 'peer:'+p, 'replace'+t)
                        # print('+'*70)
    return values


def eliminate(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    unique_value = [i[0] for i in values.items() if len(i[1]) == 1]
    for i in unique_value:
        num = values[i]
        for p in peers[i]:
            values[p] = ''.join(i for i in values[p] if i != num)
    return values


def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit

    return values


def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)
        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)
        # Execute naked_twins
        values = naked_twins(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values == False:
        return False
    if len([box for box in values.keys() if len(values[box]) == 1]) == 81:
        return values
        # Choose one of the unfilled squares with the fewest possibilities
    l, k = min([(len(values[i]), i) for i in boxes if len(values[i]) > 1])

    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for v in values[k]:
        new_sudoku = values.copy()
        new_sudoku[k] = v
        intent = search(new_sudoku)
        if intent:
            return intent


def solve(grid):
    """Find the solution to a Sudoku puzzle using search and constraint propagation

    Parameters
    ----------
    grid(string)
        a string representing a sudoku grid.

        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    Returns
    -------
    dict or False
        The dictionary representation of the final sudoku grid or False if no solution exists.
    """
    values = grid2values(grid)
    values = search(values)
    return values


if __name__ == "__main__":
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    naked_twins = '5.9.2..1.4...56...8..9.3..5.87..25..654....82..15684971.82.5...7..68...3.4..7.8..'
    test_udacity = '9.1....8.8.5.7..4.2.4....6...7......5..............83.3..6......9................'
    display(grid2values(diag_sudoku_grid))
    result = solve(diag_sudoku_grid)
    display(result)

    try:
        import PySudoku

        PySudoku.play(grid2values(diag_sudoku_grid), result, history)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
