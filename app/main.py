import bottle
import os
import collisions
import random


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
    
    directions = ['up', 'down', 'left', 'right']
    direction_weights = get_direction_weights(data)
    print(direction_weights)

    # get index of maximum value in direction_weights
    index = choose_direction(direction_weights)

    print(index)
    return {
        'move': directions[index],
        'taunt': 'noodly noodly'
    }


def choose_direction(weights):
    best_weight = max(weights)
    good_directions = [i for i, x in enumerate(weights) if x == best_weight]

    # If multiple equivalent directions exist, pick one at random.
    return random.choice(good_directions)


def get_direction_weights(data):
    # pick a direction to move
    weights = list()

    # The direction weights and decision weights added at the same time,
    weights.append(collisions.avoid_walls(data))
    #weights.append(collisions.avoid_other_snakes(data))

    print(weights)

    return combine_weights(weights)


def combine_weights(weights):
    # combine weights produced by each factor according to their weight
    combined_weights = [1.0, 1.0, 1.0, 1.0]

    for criteria in weights:
        criteria_weight = criteria["weight"]
        direction_values = criteria["direction_values"]
        direction_values = [x*criteria_weight for x in direction_values]
        combined_weights = [x*y for x, y in zip(combined_weights, direction_values)]

    return combined_weights


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug=True)
