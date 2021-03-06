from app.movement import UP, DOWN, LEFT, RIGHT, points_equal, move_point, move_towards, distance


# set of weighting fuctions designed to help us avoid collisions.
def avoid_walls(data, weight):
    criteria = {"goal": "avoid_walls", "weight": weight}
    # walls: places with x, y outside the game area

    # where we are
    us = data["you"]
    board = data["board"]
    # first point in list is our head.
    our_head = us["body"][0]

    # possible directions we can move
    directions = [1.0, 1.0, 1.0, 1.0]

    if our_head["x"] + 1 >= board["width"]:
        directions[RIGHT] = 0.0

    if our_head["x"] - 1 < 0:
        directions[LEFT] = 0.0

    if our_head["y"] + 1 >= board["height"]:
        directions[DOWN] = 0.0

    if our_head["y"] - 1 < 0:
        directions[UP] = 0.0

    # normalize weighting matrix
    if sum(directions) == 0:
        criteria["direction_values"] = [0.0, 0.0, 0.0, 0.0]
    else:
        criteria["direction_values"] = [x / sum(directions) for x in directions]

    return criteria


def avoid_other_snakes(data, weight):
    criteria = {"goal": "avoid_other_snakes", "weight": weight}
    # walls: places with x, y outside the game area

    # where we are
    us = data["you"]
    # first point in list is our head.
    us_points = us["body"]
    our_head = us_points[0]

    # spots we could move:

    moves = [move_point(our_head, UP), move_point(our_head, DOWN),
             move_point(our_head, LEFT), move_point(our_head, RIGHT)]

    other_snakes = []
    # other snakes
    for snake in data["board"]["snakes"]:
        if snake["health"] > 0:
            # If snake is dead, we don't need to avoid it
            other_snakes.append(snake)

    # possible directions we can move
    directions = [1.0, 1.0, 1.0, 1.0]

    for snake in other_snakes:
        snake_points = snake["body"]
        # note: tail is always safe
        for index in range(len(snake_points)):

            # special handling for enemy snake heads
            if index == 0 and not points_equal(our_head, snake_points[index]):

                # weight if other snake is bigger than us
                weight = 0.1
                if len(snake_points) < len(us_points):
                    # weight if other snake is smaller than us
                    weight = 2.0

                for i in range(4):
                    for j in range(4):
                        # be more conservative about enemy snake heads
                        if distance(moves[i], move_point(snake_points[index], j)) < 2.2:
                            if weight == 0.1 and points_equal(moves[i], move_point(snake_points[index], j)):
                                # don't die
                                directions[i] = 0.0
                            else:
                                directions[i] = weight

            for i in range(4):
                if points_equal(moves[i], snake_points[index]):
                    directions[i] = 0.0

    # normalize and return
    if sum(directions) == 0:
        criteria["direction_values"] = [0.0, 0.0, 0.0, 0.0]
    else:
        criteria["direction_values"] = [x / sum(directions) for x in directions]

    return criteria


def follow_tail(data, weight):
    criteria = {"goal": "follow_our_tail", "weight": weight}

    head = data["you"]["body"][0]
    tail = data["you"]["body"][-1]

    directions = move_towards(head, tail)

    # normalize and return
    if sum(directions) == 0:
        criteria["direction_values"] = [0.0, 0.0, 0.0, 0.0]
    else:
        criteria["direction_values"] = [x / sum(directions) for x in directions]

    return criteria
