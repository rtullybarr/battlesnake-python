import app.main as main
import time
import app.movement as movement


def run_tests(data):

    start = time.time()

    print("make sure move throws no errors")
    print(main.execute_move(data))

    grid = movement.get_grid(data)

    end = time.time()

    print(str.format("took {0:.1f} ms", (end - start)*1000))


if __name__ == "__main__":

    # test_data = {
    #   "food": {
    #     "data": [
    #       {
    #         "object": "point",
    #         "x": 0,
    #         "y": 9
    #       }
    #     ],
    #     "object": "list"
    #   },
    #   "height": 100,
    #   "id": 1,
    #   "object": "world",
    #   "snakes": {
    #     "data": [
    #       {
    #         "body": {
    #           "data": [
    #             {
    #               "object": "point",
    #               "x": 13,
    #               "y": 19
    #             },
    #             {
    #               "object": "point",
    #               "x": 13,
    #               "y": 18
    #             },
    #             {
    #               "object": "point",
    #               "x": 13,
    #               "y": 17
    #             }
    #           ],
    #           "object": "list"
    #         },
    #         "health": 100,
    #         "id": "58a0142f-4cd7-4d35-9b17-815ec8ff8e70",
    #         "length": 3,
    #         "name": "Sonic Snake",
    #         "object": "snake",
    #         "taunt": "Gotta go fast"
    #       },
    #       {
    #         "body": {
    #           "data": [
    #             {
    #               "object": "point",
    #               "x": 8,
    #               "y": 15
    #             },
    #             {
    #               "object": "point",
    #               "x": 7,
    #               "y": 15
    #             },
    #             {
    #               "object": "point",
    #               "x": 6,
    #               "y": 15
    #             }
    #           ],
    #           "object": "list"
    #         },
    #         "health": 100,
    #         "id": "48ca23a2-dde8-4d0f-b03a-61cc9780427e",
    #         "length": 3,
    #         "name": "Typescript Snake",
    #         "object": "snake",
    #         "taunt": ""
    #       }
    #     ],
    #     "object": "list"
    #   },
    #   "turn": 0,
    #   "width": 100,
    #   "you": {
    #     "body": {
    #       "data": [
    #         {
    #           "object": "point",
    #           "x": 8,
    #           "y": 15
    #         },
    #         {
    #           "object": "point",
    #           "x": 7,
    #           "y": 15
    #         },
    #         {
    #           "object": "point",
    #           "x": 6,
    #           "y": 15
    #         }
    #       ],
    #       "object": "list"
    #     },
    #     "health": 100,
    #     "id": "48ca23a2-dde8-4d0f-b03a-61cc9780427e",
    #     "length": 3,
    #     "name": "Typescript Snake",
    #     "object": "snake",
    #     "taunt": ""
    #   }
    # }

    test_data = {
      "game": {
        "id": "game-id-string"
      },
      "turn": 1,
      "board": {
        "height": 11,
        "width": 11,
        "food": [{
          "x": 1,
          "y": 3
        }],
        "snakes": [{
          "id": "snake-id-string",
          "name": "Sneky Snek",
          "health": 100,
          "body": [{
            "x": 1,
            "y": 3
          }]
        }]
      },
      "you": {
        "id": "snake-id-string",
        "name": "Sneky Snek",
        "health": 100,
        "body": [{
          "x": 1,
          "y": 3
        }]
      }
    }

    run_tests(test_data)
