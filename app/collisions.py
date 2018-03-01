
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3


# checks if two points are equal
def points_equal(p1, p2):
    return p1["x"] == p2["x"] and p1["y"] == p2["y"]


# returns a new point that has been shifted one step in the given direction.
def move_point(point, direction):
    new_point = dict(point)
    if direction == UP:
        new_point["y"] -= 1
    if direction == DOWN:
        new_point["y"] += 1
    if direction == LEFT:
        new_point["x"] -= 1
    if direction == RIGHT:
        new_point["x"] += 1
    return new_point

# set of weighting fuctions designed to help us avoid collisions.
def avoid_walls(data):
    criteria = {"goal": "avoid_walls", "weight": 0.5}
    # walls: places with x, y outside the game area

    # where we are
    us = data["you"]
    # first point in list is our head.
    our_head = us["body"]["data"][0]

    # possible directions we can move
    directions = [1.0, 1.0, 1.0, 1.0]

    if our_head["x"] + 1 >= data["width"]:
        directions[RIGHT] = 0.0

    if our_head["x"] - 1 < 0:
        directions[LEFT] = 0.0

    if our_head["y"] + 1 >= data["height"]:
        directions[DOWN] = 0.0

    if our_head["y"] - 1 < 0:
        directions[UP] = 0.0

    # normalize weighting matrix
    if sum(directions) == 0:
        criteria["direction_values"] = [0.0, 0.0, 0.0, 0.0]
    else:
        criteria["direction_values"] = [x / sum(directions) for x in directions]

    return criteria


def avoid_other_snakes(data):
    criteria = {"goal": "avoid_other_snakes", "weight": 0.5}
    # walls: places with x, y outside the game area

    # where we are
    us = data["you"]
    # first point in list is our head.
    us_points = us["body"]["data"]
    our_head = us_points[0]

    # spots we could move:

    moves = [move_point(our_head, UP), move_point(our_head, DOWN),
             move_point(our_head, LEFT), move_point(our_head, RIGHT)]

    # other snakes
    other_snakes = data["snakes"]["data"]
    # avoid our own body too
    other_snakes.append(us)

    # possible directions we can move
    directions = [1.0, 1.0, 1.0, 1.0]

    for snake in other_snakes:
        snake_points = snake["body"]["data"]
        for index, point in enumerate(snake_points):

            # special handling for enemy snake heads
            if index == 0 and not points_equal(our_head, point):

                weight = 0.0
                if len(snake_points) < len(us_points):
                    weight = 2.0

                for i in range(4):
                    for j in range(4):
                        if points_equal(moves[i], move_point(point, j)):
                            directions[i] = weight

            for i in range(4):
                if points_equal(moves[i], point):
                    directions[i] = 0.0

    # normalize and return
    if sum(directions) == 0:
        criteria["direction_values"] = [0.0, 0.0, 0.0, 0.0]
    else:
        criteria["direction_values"] = [x / sum(directions) for x in directions]

    return criteria
