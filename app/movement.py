import numpy as np


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


# not really a movement function, but turns the world into a grid that's easier to work with
EMPTY = 0.0
SNAKE = 1.0
FOOD = 2.0
VISITED = 3.0


def get_grid(data):
    grid = np.zeros((data["width"], data["height"]))

    for snake in data["snakes"]["data"]:
        for i, point in enumerate(snake["body"]["data"]):
            grid[point["x"], point["y"]] = SNAKE

    for food in data["food"]["data"]:
        grid[food["x"], food["y"]] = FOOD

    return grid
