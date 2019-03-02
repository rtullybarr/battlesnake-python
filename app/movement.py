import numpy as np
import math


UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3


# checks if two points are equal
def points_equal(p1, p2):
    return p1["x"] == p2["x"] and p1["y"] == p2["y"]


def distance(p1, p2):
    return math.sqrt(math.pow(p1["x"] - p2["x"], 2) + math.pow(p1["y"] - p2["y"], 2))


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


def move_towards(head, point):
    # returns weights for directions to move towards a point
    directions = [0.1, 0.1, 0.1, 0.1]
    # above
    if head["y"] < point["y"]:
        directions[DOWN] = 1.0

    # below
    if head["y"] > point["y"]:
        directions[UP] = 1.0

    # to the left
    if head["x"] < point["x"]:
        directions[RIGHT] = 1.0

    if head["x"] > point["x"]:
        directions[LEFT] = 1.0

    return directions


# not really a movement function, but turns the world into a grid that's easier to work with
EMPTY = 0.0
SNAKE = 1.0
FOOD = 2.0
VISITED = 3.0


def get_grid(data):
    grid = np.zeros((data["width"], data["height"]))

    for snake in data["board"]["snakes"]:
        if snake["health"] <= 0:
            continue
        for i, point in enumerate(snake["body"]["data"]):
            grid[point["x"], point["y"]] = SNAKE

    for food in data["food"]["data"]:
        grid[food["x"], food["y"]] = FOOD

    return grid
