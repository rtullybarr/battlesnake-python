
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3


# set of weighting fuctions designed to help us avoid collisions.
def avoid_walls(data):
    criteria = {"goal": "avoid_walls", "weight": 0.5}
    # walls: places with x, y outside the game area

    # where we are
    us = data["you"]
    # first point in list is our head.
    head_location = us["body"]["data"][0]

    # possible directions we can move
    directions = [1.0, 1.0, 1.0, 1.0]

    if head_location["x"] + 1 >= data["width"]:
        directions[RIGHT] = 0.0

    if head_location["x"] - 1 < 0:
        directions[LEFT] = 0.0

    if head_location["y"] + 1 >= data["height"]:
        directions[DOWN] = 0.0

    if head_location["y"] - 1 < 0:
        directions[UP] = 0.0

    # normalize weighting matrix
    criteria["direction_values"] = [x / sum(directions) for x in directions]
    return criteria


def avoid_other_snakes(data):
    criteria = {"goal": "avoid_other_snakes", "weight": 0.5}
    # walls: places with x, y outside the game area

    # where we are
    us = data["you"]
    # first point in list is our head.
    us_points = us["body"]["data"]
    head_location = us_points[0]

    # spots we could move:

    moves = [(head_location["x"], head_location["y"] - 1),  # up
             (head_location["x"], head_location["y"] + 1),  # down
             (head_location["x"] - 1, head_location["y"]),  # left
             (head_location["x"] + 1, head_location["y"])]  # right

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
            if index == 0:

                weight = 0
                if len(snake_points) < len(us_points):
                    weight = 2

                for i in range(4):
                    # they move up
                    if moves[i][0] == point["x"] and moves[i][1] == point["y"] - 1:
                        directions[i] = weight

                    # they move down
                    if moves[i][0] == point["x"] and moves[i][1] == point["y"] + 1:
                        directions[i] = weight

                    # they move left
                    if moves[i][0] == point["x"] - 1 and moves[i][1] == point["y"]:
                        directions[i] = weight

                    # they move right
                    if moves[i][0] == point["x"] + 1 and moves[i][1] == point["y"]:
                        directions[i] = weight

            for i in range(4):
                if moves[i][0] == point["x"] and moves[i][1] == point["y"]:
                    directions[i] = 0

    # normalize and return
    criteria["direction_values"] = [x / sum(directions) for x in directions]
    return criteria
