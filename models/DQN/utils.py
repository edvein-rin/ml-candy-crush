import random
import numpy as np

def arr_to_tuple(arr):
    tupArr = [tuple(elem) for elem in arr]
    return tuple(tupArr)


def is_end_state(state):
    return state[1] == 0


def actions(state, rows, cols):
    actions = []
    grid = state[0]
    for i in range(rows):
        for j in range(cols):
            if is_valid_move(grid, rows, cols, (i, j), (i, j + 1)):
                coord1 = (i, j)
                coord2 = (i, j + 1)
                actions.append((coord1, coord2))
            elif is_valid_move(grid, rows, cols, (i, j), (i + 1, j)):
                coord1 = (i, j)
                coord2 = (i + 1, j)
                actions.append((coord1, coord2))
    return actions


def cascade_coordinates(grid, rows, cols):
    coords = set()
    for i in range(rows):
        for j in range(cols):
            colorRowsSet, colorColsSet = explore_coordinates(grid, rows, cols, i, j)
            colorAllSet = set()
            if len(colorRowsSet) >= 3:
                colorAllSet = colorRowsSet
            if len(colorColsSet) >= 3:
                colorAllSet = colorAllSet.union(colorColsSet)
            if len(colorAllSet) > len(coords):
                coords = colorAllSet
    return coords


def cascade(grid, rows, cols, colors):
    def drop_columns(grid, colsToRowsMap):
      for col in colsToRowsMap:
          currRows = colsToRowsMap[col]
          minRow = currRows[0]
          maxRow = currRows[1]
          diff = maxRow - minRow + 1
          for i in range(minRow):
              grid[minRow - 1 - i + diff, col] = grid[minRow - 1 - i, col]
          for i in range(diff):
              grid[i, col] = random.randint(1, colors)
      return

    turnScore = 0
    combo = 1
    while True:
        coords = cascade_coordinates(grid, rows, cols)
        cascadeSize = len(coords)
        if cascadeSize < 3:
            break
        addScore = 10 * (cascadeSize**2 - cascadeSize) * combo
        turnScore += addScore
        combo += 1
        colsToRowsMap = {}
        for coord in coords:
            if coord[1] not in colsToRowsMap:
                colsToRowsMap[coord[1]] = [coord[0], coord[0]]
            else:
                currRows = colsToRowsMap[coord[1]]
                currRowMin = currRows[0]
                currRowMax = currRows[1]
                if coord[0] < currRowMin:
                    currRows[0] = coord[0]
                elif coord[0] > currRowMax:
                    currRows[1] = coord[0]
        drop_columns(grid, colsToRowsMap)
    return grid, turnScore



def is_valid_move(grid, rows, cols, coord1, coord2):
    def is_valid_coordinate(coord):
        row, col = coord
        return 0 <= row < len(grid) and 0 <= col < len(grid[0])

    if coord1 == coord2:
        return False

    if is_valid_coordinate(coord1) and is_valid_coordinate(coord2):
        row_diff = abs(coord1[0] - coord2[0])
        col_diff = abs(coord1[1] - coord2[1])

        if (row_diff == 1 and coord1[1] == coord2[1]) or (col_diff == 1 and coord1[0] == coord2[0]):
            grid_copy = np.copy(grid)
            grid_copy[coord1], grid_copy[coord2] = grid_copy[coord2], grid_copy[coord1]

            color_rows_set1, color_cols_set1 = explore_coordinates(grid_copy, rows, cols, coord1[0], coord1[1])
            if len(color_rows_set1) >= 3 or len(color_cols_set1) >= 3:
                return True

            color_rows_set2, color_cols_set2 = explore_coordinates(grid_copy, rows, cols, coord2[0], coord2[1])
            if len(color_rows_set2) >= 3 or len(color_cols_set2) >= 3:
                return True

    return False


def explore_coordinates(grid, rows, cols, i, j):
    color = grid[i, j]
    colorRowsSet = set([(i, j)])
    colorColsSet = set([(i, j)])
    # explore above
    for row in range(i):
        if color != grid[i - row - 1, j]:
            break
        colorRowsSet.add((i - row - 1, j))
    # explore below
    for row in range(i + 1, rows):
        if color != grid[row, j]:
            break
        colorRowsSet.add((row, j))
    # explore left
    for col in range(j):
        if color != grid[i, j - col - 1]:
            break
        colorColsSet.add((i, j - col - 1))
    # explore right
    for col in range(j + 1, cols):
        if color != grid[i, col]:
            break
        colorColsSet.add((i, col))
    return colorRowsSet, colorColsSet