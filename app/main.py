import bottle
import os
import random

import collisions
import freedom
import food


@bottle.route('/')
def static():
    return "the server is running"


@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.post('/start')
def start():
    data = bottle.request.json

    head_url = '%s://%s/static/fhead.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    return {
        'color': '#FF0000',
        'taunt': 'noodly noodly',
        'head_url': head_url,
        'name': 'danger-noodle',
        'head_type': 'tongue',
        'tail_type': 'freckled',
        'secondary_color': '#FFFF00'
    }


@bottle.post('/move')
def move():
    data = bottle.request.json

    return execute_move(data)

    
def execute_move(data):
    
    directions = ['up', 'down', 'left', 'right']
    direction_weights = get_direction_weights(data)
    weights_string = str.format("up: {0:.2f}, down: {1:.2f}, left: {2:.2f}, right: {3:.2f}",
                            direction_weights[0], direction_weights[1], direction_weights[2], direction_weights[3])
    print(weights_string)

    # get index of maximum value in direction_weights
    max_weight, index = choose_direction(direction_weights)

    if max_weight == 0:
        return {
            'move': directions[index],
            'taunt': 'x___x'
        }

    return {
        'move': directions[index],
        'taunt': weights_string
    }


def choose_direction(weights):
    best_weight = max(weights)
    good_directions = [i for i, x in enumerate(weights) if x == best_weight]

    # If multiple equivalent directions exist, pick one at random.
    return best_weight, random.choice(good_directions)


def get_direction_weights(data):
    # pick a direction to move
    weights = list()

    # The direction weights and decision weights added at the same time,
    weights.append(collisions.avoid_walls(data, 1))
    weights.append(collisions.avoid_other_snakes(data, 10))
    weights.append(freedom.move_to_most_space(data, 8))
    weights.append(food.nearest_food_simple(data, 3))

    return combine_weights_add(weights)


def combine_weights_multiply(weights):
    # combine weights produced by each factor according to their weight
    combined_weights = [1.0, 1.0, 1.0, 1.0]

    for criteria in weights:
        criteria_weight = criteria["weight"]
        direction_values = criteria["direction_values"]
        direction_values = [x*criteria_weight for x in direction_values]
        combined_weights = [x*y for x, y in zip(combined_weights, direction_values)]

    if sum(combined_weights) == 0:
        return [0.0, 0.0, 0.0, 0.0]

    return [x/sum(combined_weights) for x in combined_weights]


def combine_weights_add(weights):
    # combine weights produced by each factor according to their weight
    combined_weights = [1.0, 1.0, 1.0, 1.0]

    for criteria in weights:
        criteria_weight = criteria["weight"]
        direction_values = criteria["direction_values"]
        direction_values = [x*criteria_weight for x in direction_values]
        combined_weights = [x+y for x, y in zip(combined_weights, direction_values)]
        # propagate zeros
        combined_weights = [0 if x == 0 or y == 0 else x for x, y in zip(combined_weights, direction_values)]

    if sum(combined_weights) == 0:
        return [0.0, 0.0, 0.0, 0.0]

    return [x/sum(combined_weights) for x in combined_weights]


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug=True)
