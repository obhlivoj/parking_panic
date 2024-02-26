"""
parking_panic.py

Implementation of the Parking Panic game using Pygame.

Modules:
- pygame: Provides functionality for creating games and multimedia applications using Pygame.
- panic: A custom module containing functions specific to the Parking Panic game.
- engine: A custom module containing game engine functions.
- intro: A custom module containing functions related to the game intro screen.

Constants:
- SIZE: The size of each game field.
- RECT_X: The x-coordinate of the top-left corner of the gameboard rectangle.
- RECT_Y: The y-coordinate of the top-left corner of the gameboard rectangle.
- N_FIELD: The number of game fields.
- EXIT_SIZE: The size of the exit field.
- EXIT_N: The number of exit fields.
- window_size: The size of the game window.

Author: Vojtech Obhlidal
Year: 2023
"""

if __name__ == "__main__":
    import sys
    from copy import deepcopy

    import pygame
    # pylint: disable=no-member

    from src import pygame_module as panic
    from src import engine
    from src import intro_screen as intro

    SIZE = 100
    RECT_X = 30
    RECT_Y = 30
    N_FIELD = 6
    EXIT_SIZE = 80
    EXIT_N = 2
    window_size = (N_FIELD*SIZE + 2*RECT_X +
                   EXIT_SIZE, N_FIELD*SIZE + 2*RECT_Y)

    info = {
        "SIZE": SIZE,
        "RECT_X": RECT_X,
        "RECT_Y": RECT_Y,
        "N_FIELD": N_FIELD,
        "EXIT_SIZE": EXIT_SIZE,
        "EXIT_N": EXIT_N,
        "WINDOW": window_size,
    }
    pygame.init()
    # Set the size of the window
    window_size = (info["N_FIELD"]*info["SIZE"] + 2*info["RECT_X"] +
                   info["EXIT_SIZE"], info["N_FIELD"]*info["SIZE"] + 2*info["RECT_Y"])

    # Create the window, set the title of the window
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Parking Panic")

    screen, n, park, matrix, max_lvl, cars = panic.init_game(info, screen)
    record_dicc = engine.read_recs()

    true_cars = deepcopy(cars)

    # Run the game loop
    success = 0
    moves = 0
    list_movements = []

    panic.render_counter_and_level(moves, info, n, max_lvl, screen)

    exit_field = pygame.Rect(info["RECT_X"] + info["N_FIELD"]*info["SIZE"],
                             info["RECT_Y"] + info["EXIT_N"]*info["SIZE"], info["EXIT_SIZE"], info["SIZE"])

    selected = None
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:  # Left mouse button clicked
                # Get the position of the mouse click
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Calculate the field coordinates
                if RECT_X < mouse_x <= RECT_X + N_FIELD*SIZE and RECT_Y < mouse_y <= RECT_Y + N_FIELD*SIZE:
                    field_x = (mouse_x - RECT_X) // SIZE
                    field_y = (mouse_y - RECT_Y) // SIZE

                    # Print the field coordinates
                    id_car = panic.find_car(cars, (field_x, field_y))
                    selected = id_car

            elif event.type == pygame.MOUSEMOTION and selected is not None:
                dx, dy = event.rel
                x, y = cars[selected]["xy"]
                if cars[selected]["dir"] == "H":
                    cars[selected]["xy"] = (x + dx, y)
                else:
                    cars[selected]["xy"] = (x, y + dy)

                panic.redraw_motion(info, cars, screen)
                panic.render_counter_and_level(moves, info, n, max_lvl, screen)

            elif event.type == pygame.MOUSEBUTTONUP:
                if selected is None:
                    continue
                selected = None

                # Get the position
                mouse_x, mouse_y = pygame.mouse.get_pos()
                new_coords = None
                response = None

                new_field_x, new_field_y = None, None
                if RECT_X < mouse_x <= (RECT_X + N_FIELD*SIZE) and RECT_Y < mouse_y <= (RECT_Y + N_FIELD*SIZE):
                    new_field_x = (mouse_x - RECT_X) // SIZE
                    new_field_y = (mouse_y - RECT_Y) // SIZE

                elif exit_field.collidepoint((mouse_x, mouse_y)):
                    new_field_x = 6
                    new_field_y = 2

                if new_field_x is not None and new_field_y is not None:
                    if new_field_x != field_x or new_field_y != field_y:
                        if true_cars[id_car]["dir"] == "H":
                            if new_field_x > field_x:
                                new_coords = (field_x+1, field_y)
                                response = true_cars[id_car]["id"].lower()
                                new_pos = panic.shift_car(
                                    true_cars[id_car]["coords"], "x+")
                            elif new_field_x < field_x:
                                new_coords = (field_x-1, field_y)
                                response = true_cars[id_car]["id"].upper()
                                new_pos = panic.shift_car(
                                    true_cars[id_car]["coords"], "x-")
                        else:
                            if new_field_y > field_y:
                                new_coords = (field_x, field_y+1)
                                response = true_cars[id_car]["id"].lower()
                                new_pos = panic.shift_car(
                                    true_cars[id_car]["coords"], "y+")
                            elif new_field_y < field_y:
                                new_coords = (field_x, field_y-1)
                                response = true_cars[id_car]["id"].upper()
                                new_pos = panic.shift_car(
                                    true_cars[id_car]["coords"], "y-")

                        if response:
                            moved, success, moves, matrix = engine.engine_step(
                                response, park, list_movements, moves)
                            # engine.print_matrix(matrix)

                            if moved:
                                true_cars[id_car]["coords"] = new_pos
                                true_cars[id_car]["block_pos"] = new_pos[0]
                                true_cars[id_car]["xy"] = panic.get_xy_from_pos(
                                    info, true_cars[id_car])

                cars = deepcopy(true_cars)
                panic.redraw_board(info, true_cars, screen)
                panic.render_counter_and_level(moves, info, n, max_lvl, screen)

        if success == 1:
            intro.congratulate(info, screen)
            recrod_dicc = engine.update_recs(moves, record_dicc, n)

            success = 0
            moves = 0
            list_movements = []
            screen, n, park, matrix, max_lvl, cars = panic.init_game(
                info, screen)
            true_cars = deepcopy(cars)
            panic.render_counter_and_level(moves, info, n, max_lvl, screen)

        pygame.display.update()
