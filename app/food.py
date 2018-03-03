import movement


def nearest_food_simple(data):
    criteria = {"goal": "nearest_food_simple", "weight": 0.1}
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
