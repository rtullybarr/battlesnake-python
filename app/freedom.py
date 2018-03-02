import movement
import numpy as np


def move_to_most_space(data):
    criteria = {"goal": "move_to_most_space", "weight": 0.2}

    directions = [1.0, 1.0, 1.0, 1.0]

    head = data["you"]["body"]["data"][0]
    grid = movement.get_grid(data)

    for i in range(4):
        directions[i] = float(reachable_area(movement.move_point(head, i), np.copy(grid)))

    if sum(directions) == 0:
        criteria["direction_values"] = [0.0, 0.0, 0.0, 0.0]
    else:
        criteria["direction_values"] = [x / sum(directions) for x in directions]

    return criteria


def reachable_area(point, grid):

    # base cases
    shape = grid.shape
    if point["x"] < 0 or point["x"] >= shape[0]:
        return 0

    if point["y"] < 0 or point["y"] >= shape[1]:
        return 0

    if grid[point["x"]][point["y"]] == movement.SNAKE or grid[point["x"]][point["y"]] == movement.VISITED:
        return 0

    # mark this point as visited
    grid[point["x"]][point["y"]] = movement.VISITED
    # count ourselves
    area = 1

    for i in range(4):
        area += reachable_area(movement.move_point(point, i), grid)

    return area
