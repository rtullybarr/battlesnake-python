import movement
import numpy as np
import collections


def move_to_most_space(data, weight):
    criteria = {"goal": "move_to_most_space", "weight": weight}

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


def reachable_area(head, grid):

    # replace with queue impl
    unvisited = collections.deque()
    unvisited.append(head)
    visited_area = 0

    while len(unvisited) > 0:
        point = unvisited.pop()

        shape = grid.shape
        if point["x"] < 0 or point["x"] >= shape[0]:
            continue

        if point["y"] < 0 or point["y"] >= shape[1]:
            continue

        if grid[point["x"]][point["y"]] == movement.SNAKE:
            continue

        if grid[point["x"]][point["y"]] == movement.VISITED:
            continue

        grid[point["x"]][point["y"]] = movement.VISITED
        visited_area += 1

        for i in range(4):
            new_point = movement.move_point(point, i)

            shape = grid.shape
            if new_point["x"] < 0 or new_point["x"] >= shape[0]:
                continue

            if new_point["y"] < 0 or new_point["y"] >= shape[1]:
                continue

            if grid[new_point["x"]][new_point["y"]] == movement.SNAKE:
                continue

            if grid[new_point["x"]][new_point["y"]] == movement.VISITED:
                continue

            # limit to within 8 points around our head to avoid timing out.
            if abs(head["x"] - new_point["x"]) > 8:
                continue

            if abs(head["y"] - new_point["y"]) > 8:
                continue

            unvisited.append(new_point)

    return visited_area
