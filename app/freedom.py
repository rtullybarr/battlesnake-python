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


def empty_or_food(point, grid):
    shape = grid.shape
    if point["x"] < 0 or point["x"] >= shape[0]:
        return False

    if point["y"] < 0 or point["y"] >= shape[1]:
        return False

    if grid[point["x"]][point["y"]] == movement.SNAKE:
        return False

    if grid[point["x"]][point["y"]] == movement.VISITED:
        return False

    return True


def reachable_area(head, grid):

    # replace with queue impl
    unvisited = list()
    unvisited.append(head)
    visited_area = 0

    while len(unvisited) > 0:
        point = unvisited.pop()

        if empty_or_food(point, grid):
            grid[point["x"]][point["y"]] = movement.VISITED
            visited_area += 1

            for i in range(4):
                new_point = movement.move_point(point, i)
                if empty_or_food(new_point, grid):
                    unvisited.append(new_point)

    return visited_area

