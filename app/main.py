import bottle
import os
import collisions


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

    print("data received: ")
    print(data)
    
    directions = ['up', 'down', 'left', 'right']
    direction_weights = choose_direction(data)
    print direction_weights

    # get index of maximum value in direction_weights
    index = direction_weights.index(min(direction_weights))

    return {
        'move': directions[index],
        'taunt': 'noodly noodly'
    }


def choose_direction(data):
    # pick a direction to move
    weights = []

    # The direction weights and decision weights added at the same time,
    weights += collisions.avoid_walls(data)
    weights += collisions.avoid_other_snakes(data)

    return combine_weights(weights)


def combine_weights(weights):
    # combine weights produced by each factor according to their weight
    combined_weights = [1, 1, 1, 1]

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
