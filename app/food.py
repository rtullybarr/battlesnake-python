import movement
from movement import UP, DOWN, LEFT, RIGHT


def nearest_food_simple(data, weight):
    criteria = {"goal": "nearest_food_simple", "weight": weight}
    # picks closest food and gives direction towards it.
    food = data["food"]["data"]
    head = data["you"]["body"]["data"][0]
    width = data["width"]
    height = data["height"]

    min_dist = width * height
    nearest_food = None

    for point in food:
        distance = movement.distance(head, point)
        if distance < min_dist:
            min_dist = distance
            nearest_food = point

    directions = [0.1, 0.1, 0.1, 0.1]
    if nearest_food is not None:
        directions = movement.move_towards(head, nearest_food)

    criteria["direction_values"] = directions

    return criteria

def nearest_food_a_star(data, food_weight):
    criteria = {"goal": "find_nearet_food", "weight": food_weight} # TODO: we could vary weight depending on our snake's health

    # where we are
    us = data["you"]
    # first point in list is our head.
    our_head = us["body"]["data"][0]

    # possible directions we can move
    directions = [1.0, 1.0, 1.0, 1.0]


    # normalize weighting matrix
    if sum(directions) == 0:
        criteria["direction_values"] = [0.0, 0.0, 0.0, 0.0]
    else:
        criteria["direction_values"] = [x / sum(directions) for x in directions]

    return criteria

def a_star(start, goal):
    closedList = [] # Squares we don't need to consider anymore
    openList = PriorityQueue() # Squares we do need to consider
    openList.put((0, start))
    cameFrom = {}

    while not openList.empty():
        current = openList.get() # Remove square with lowest f score
        closedList.append(current) # add current square to closed list

        # If we added the destination to the closed list, we've found a path
        if any(current['x'] == p['x'] and current['y'] == p['y'] for p in closedList):
            break

        # Get all adjacent squares
        if current == goal:
            break

         for i in range(4):
            new_point = movement.move_point(current, i)

            shape = grid.shape
            if new_point["x"] < 0 or new_point["x"] >= shape[0]:
                continue

            if new_point["y"] < 0 or new_point["y"] >= shape[1]:
                continue

            if grid[new_point["x"]][new_point["y"]] == movement.SNAKE:
                continue

        if current in closedList
        


# to calculate g, add 1 to G of its parent
    # G is movement cost from start point to current square
    # H is estimated movement cost from the current square to the destination (heuristic)

# F is score of each square. F = G + H
def manhattan

    if current 