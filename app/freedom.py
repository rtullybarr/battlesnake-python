import movement
import numpy as np
import collections


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


def reachable_area(head, grid):

    # replace with queue impl
    unvisited = collections.deque()
    unvisited.append(head)
    visited_area = 0

    while len(unvisited) > 0:
        point = unvisited.pop()

        empty_or_food = True

        shape = grid.shape
        if point["x"] < 0 or point["x"] >= shape[0]:
            empty_or_food = False

        if point["y"] < 0 or point["y"] >= shape[1]:
            empty_or_food = False

        if grid[point["x"]][point["y"]] == movement.SNAKE:
            empty_or_food = False

        if grid[point["x"]][point["y"]] == movement.VISITED:
            empty_or_food = False

        if empty_or_food:
            grid[point["x"]][point["y"]] = movement.VISITED
            visited_area += 1

            for i in range(4):
                new_point = movement.move_point(point, i)

                empty_or_food = True

                shape = grid.shape
                if point["x"] < 0 or point["x"] >= shape[0]:
                    empty_or_food = False

                if point["y"] < 0 or point["y"] >= shape[1]:
                    empty_or_food = False

                if grid[point["x"]][point["y"]] == movement.SNAKE:
                    empty_or_food = False

                if grid[point["x"]][point["y"]] == movement.VISITED:
                    empty_or_food = False

                if empty_or_food:
                    unvisited.append(new_point)

    return visited_area

