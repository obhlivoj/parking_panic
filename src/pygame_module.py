"""
pygame_module.py

This module contains functions related to the Parking Panic game. It provides functionality for planting and updating cars on the gameboard, redrawing the gameboard with updated car positions, finding cars occupying specific coordinates, shifting car positions, rendering counters and levels on the screen, and calculating pixel coordinates from block positions.

The module includes the following functions:

- update_car_dict: Updates the coordinates of a car based on its image position and size.
- plant_cars: Plants and displays cars on the gameboard for the Parking Panic game.
- redraw_board: Redraws the gameboard with the updated positions of cars.
- redraw_motion: Redraws the gameboard with the updated positions of cars.
- find_car: Finds the ID of the car occupying the specified field coordinates.
- shift_car: Shifts the coordinates of a car in the specified direction.
- render_counter_and_level: Renders and displays the move counter and level number on the game screen.
- get_xy_from_pos: Calculates the pixel coordinates from the block position of a car.

Each function includes detailed docstrings explaining its purpose, arguments, and return values.

Author: Vojtech Obhlidal
Year: 2023
"""

from string import ascii_uppercase
from typing import List, Dict, Tuple, Union, Any

import numpy as np
import pygame

from . import intro_screen as intro
from . import engine


def init_game(info: Dict[str, int], screen: pygame.Surface) -> Tuple[pygame.Surface, int, str, List[List[int]], int, Dict[int, Dict[str, int]]]:
    """
    Initialize the game and display the intro screen.

    Args:
        info: A dictionary containing information about the game settings.
        screen: The Pygame screen object.

    Returns:
        A tuple containing the necessary game information.

    The 'info' dictionary should contain the following keys:
    - 'N_FIELD' (int): The number of fields in each row/column of the gameboard.
    - 'SIZE' (int): The size (width/height) of each gameboard cell.
    - 'RECT_X' (int): The x-coordinate of the top-left corner of the gameboard rectangle.
    - 'RECT_Y' (int): The y-coordinate of the top-left corner of the gameboard rectangle.
    - 'EXIT_SIZE' (int): The size (width/height) of the exit field.
    - 'EXIT_N' (int): The row number of the exit field.

    The function performs the following tasks:
    1. Reads the high scores from the records file.
    2. Shows the intro screen and retrieves the selected level.
    3. Initializes the gameboard and sets the initial game state.
    4. Plants the cars on the gameboard.
    5. Returns the necessary game information.
    """
    recs = engine.read_recs()

    n = intro.show_intro_screen(info, recs, screen)

    park, matrix, level_park = engine.start_intro_menu(n)
    max_lvl = recs[str(n)]
    # engine.print_matrix(matrix)

    gameboard_base(info, screen)
    cars = plant_cars(info, level_park, screen)

    return screen, n, park, matrix, max_lvl, cars


def graphicalMatrix(cars: List[str]) -> Dict[int, Dict[str, int]]:
    """
    Generates a graphical representation of cars on a matrix.

    Args:
        cars: A list of cars represented by strings in the format "direction x y size".

    Returns:
        A dictionary containing information about each car's graphical representation.

    The 'cars' list should follow the following conventions:
    - Each car is represented by a string in the format "direction x y size", where:
        - 'direction' is either "H" (horizontal) or "V" (vertical) to indicate the car's orientation.
        - 'x' and 'y' represent the starting position of the car on the matrix (1-based indexing).
        - 'size' indicates the length of the car in terms of matrix cells it occupies.
    - The first car in the list is considered the target car and is always positioned horizontally.
    - Subsequent cars can be positioned horizontally or vertically, with their orientation randomly determined.
    - The 'rotate' value is randomly set to 180 degrees for horizontally positioned cars (excluding the first car)
      and randomly set to 270 or 90 degrees for vertically positioned cars.

    The function returns a dictionary where each car is assigned a unique identifier (ID) represented by uppercase letters,
    and the information about each car's graphical representation is provided in a nested dictionary. The nested dictionary
    includes the following keys:
    - 'id': The unique identifier of the car.
    - 'dir': The orientation of the car ("H" for horizontal, "V" for vertical).
    - 'rot': The rotation angle in degrees (0, 90, 180, or 270).
    - 'block_pos': The starting position of the car on the matrix (0-based indexing).
    - 'size': The length of the car in terms of matrix cells it occupies.
    """

    cars_info = {}
    for ind, car in enumerate(cars):
        if car[0] == "H" and ind != 0:
            rotate = 180 if np.random.random() > 0.5 else 0
        elif car[0] == "V":
            rotate = 270 if np.random.random() > 0.5 else 90
        else:
            rotate = 0

        block_pos = (int(car[1])-1, int(car[2])-1)
        size = int(car[3])

        cars_info[ind] = {
            "id": ascii_uppercase[ind],
            "dir": car[0],
            "rot": rotate,
            "block_pos": block_pos,
            "size": size,
        }

    return cars_info


def gameboard_base(info: Dict[str, int], screen: pygame.Surface):
    """
    Initializes and displays the base gameboard for the Parking Panic game.

    Args:
        info: A dictionary containing information about the gameboard dimensions and settings.
        screen: The Pygame screen object on which to draw the gameboard.

    The 'info' dictionary should contain the following keys:
    - 'N_FIELD' (int): The number of fields in each row/column of the gameboard.
    - 'SIZE' (int): The size (width/height) of each gameboard cell.
    - 'RECT_X' (int): The x-coordinate of the top-left corner of the gameboard rectangle.
    - 'RECT_Y' (int): The y-coordinate of the top-left corner of the gameboard rectangle.
    - 'EXIT_SIZE' (int): The size (width/height) of the exit field.
    - 'EXIT_N' (int): The row number of the exit field.

    The function performs the following tasks:
    1. Sets the size of the game window based on the gameboard dimensions and other settings.
    2. Creates the game window and sets its title.
    3. Fills the screen with a black color.
    4. Sets the dimensions and creates the gameboard rectangle using the provided settings.
    5. Draws the gameboard rectangle on the screen using a grey color.
    6. Creates and draws the exit field on the screen.
    7. Sets the font properties and renders the "EXIT" text.
    8. Positions and blits the text on the screen.
    9. Draws horizontal and vertical lines to divide the gameboard cells using a white color.
    10. Updates the display to show the initial gameboard.
    """
    # Set colors
    black_color = pygame.Color(0, 0, 0)
    grey_color = pygame.Color(128, 128, 128)
    line_color = pygame.Color(255, 255, 255)

    screen.fill(black_color)

    # Set rectangle dimensions, create gameboard rectangle
    rect_width, rect_height = info["N_FIELD"] * \
        info["SIZE"], info["N_FIELD"]*info["SIZE"]
    rect = pygame.Rect(info["RECT_X"], info["RECT_Y"], rect_width, rect_height)
    pygame.draw.rect(screen, grey_color, rect)

    # Create an exit
    exit_field = pygame.Rect(info["RECT_X"] + info["N_FIELD"]*info["SIZE"],
                             info["RECT_Y"] + info["EXIT_N"]*info["SIZE"], info["EXIT_SIZE"], info["SIZE"])
    pygame.draw.rect(screen, grey_color, exit_field)
    # Set font properties, text content
    font = pygame.font.Font(None, 40)
    text_surface = font.render("EXIT", True, (255, 255, 255))

    text_x = info["RECT_X"] + info["N_FIELD"]*info["SIZE"] + info["SIZE"]/10
    text_y = info["RECT_Y"] + info["EXIT_N"]*info["SIZE"] + info["SIZE"]/2.6
    screen.blit(text_surface, (text_x, text_y))

    # Draw horizontal lines
    for y in range(0, (info["N_FIELD"]+1)*info["SIZE"], info["SIZE"]):
        pygame.draw.line(screen, line_color, (info["RECT_X"], info["RECT_Y"]+y),
                         (info["RECT_X"]+info["N_FIELD"]*info["SIZE"], info["RECT_Y"]+y), 1)
    # Draw vertical lines
    for x in range(0, (info["N_FIELD"]+1)*info["SIZE"], info["SIZE"]):
        pygame.draw.line(screen, line_color, (info["RECT_X"]+x, info["RECT_Y"]),
                         (info["RECT_X"]+x, info["RECT_Y"]+info["N_FIELD"]*info["SIZE"]), 1)

    # Update the display
    # pygame.display.update()


def get_coords(info: Dict[str, int], coords: Tuple[int, int]) -> Tuple[int, int]:
    """
    Calculates the field coordinates based on the provided screen coordinates.

    Args:
        info: A dictionary containing information about the gameboard dimensions and settings.
        coords: A tuple representing the screen coordinates.

    Returns:
        A tuple representing the field coordinates (x, y) on the gameboard.

    The 'info' dictionary should contain the following keys:
    - 'RECT_X' (int): The x-coordinate of the top-left corner of the gameboard rectangle.
    - 'RECT_Y' (int): The y-coordinate of the top-left corner of the gameboard rectangle.
    - 'N_FIELD' (int): The number of fields in each row/column of the gameboard.
    - 'SIZE' (int): The size (width/height) of each gameboard cell.

    The 'coords' tuple should contain the screen coordinates (x, y) to be converted.

    The function performs the following tasks:
    1. Checks if the provided screen coordinates are within the gameboard boundaries.
    2. If the coordinates are valid, calculates the corresponding field coordinates on the gameboard.
    3. If the coordinates are not valid, returns (-1, -1) to indicate an invalid field.
    """
    # Calculate the field coordinates
    if info["RECT_X"] < coords[0] <= info["RECT_X"] + info["N_FIELD"]*info["SIZE"] and info["RECT_Y"] < coords[1] <= info["RECT_Y"] + info["N_FIELD"]*info["SIZE"]:
        field_x = (coords[0] - info["RECT_X"]) // info["SIZE"]
        field_y = (coords[1] - info["RECT_Y"]) // info["SIZE"]
    else:
        field_x, field_y = -1, -1

    return (int(field_x), int(field_y))


def get_image(inds: List[int], ind: int, size: int) -> Tuple[pygame.Surface, str]:
    """
    Load the image of a car based on its size and index.

    Args:
        inds: A list of indices representing the current image index for each car size.
        ind: The index of the car.
        size: The size of the car.

    Returns:
        A tuple containing the loaded image and its filename.

    The 'inds' list should contain the current image index for each car size.
    The 'ind' parameter represents the index of the car.
    The 'size' parameter represents the size of the car.

    The function performs the following tasks:
    1. Determines the appropriate filename based on the car's size and index.
    2. Loads the corresponding image using Pygame.
    3. Returns the loaded image and its filename.
    """
    if ind == 0:
        file = "../cliparts/main.png"
        image = pygame.image.load(file)
    else:
        if size == 2:
            file = f"../cliparts/car{size}_{inds[0]}.png"
            image = pygame.image.load(file)
            inds[0] += 1
        else:
            file = f"../cliparts/car{size}_{inds[1]}.png"
            image = pygame.image.load(file)
            inds[1] += 1

    return image, file


def update_car_dict(cars: Dict[int, Dict[str, Any]], ind: int, image_coords: Tuple[int, int], info: Dict[str, int], size: int) -> None:
    """
    Updates the car dictionary with the coordinates of a car.

    Args:
        cars (Dict[int, Dict[str, Any]]): A dictionary containing car information with car IDs as keys and their corresponding properties as values.
        ind (int): The ID of the car to update.
        image_coords (Tuple[int, int]): The pixel coordinates (x, y) of the car image.
        info (Dict[str, int]): A dictionary containing information about the gameboard dimensions and settings.
        size (int): The size of the car.

    The 'info' dictionary should contain the following keys:
    - 'SIZE': The size (width/height) of each gameboard cell.

    The function updates the 'coords' key of the specified car in the 'cars' dictionary.
    The 'coords' key is a list of coordinate tuples representing the occupied cells by the car on the gameboard.
    """
    image_x, image_y = image_coords
    c = []
    for i in range(size):
        x = image_x + info["SIZE"]/2
        y = image_y + info["SIZE"]/2
        if cars[ind]["dir"] == "H":
            x = x + i*info["SIZE"]
        else:
            y = y + i*info["SIZE"]
        c.append(get_coords(info, (x, y)))

    cars[ind]["coords"] = c


def plant_cars(info: list, level: list, screen):
    """
    Plants and displays cars on the gameboard for the Parking Panic game.

    Args:
        info (dict): A dictionary containing information about the gameboard dimensions and settings.
        level (list): A list representing the level layout.
        screen : The Pygame screen object on which to draw the cars.

    The 'info' dictionary should contain the following keys:
    - 'RECT_X': The x-coordinate of the top-left corner of the gameboard rectangle.
    - 'RECT_Y': The y-coordinate of the top-left corner of the gameboard rectangle.
    - 'SIZE': The size (width/height) of each gameboard cell.

    The 'level' list should contain a representation of the cars layout.

    The function performs the following tasks:
    1. Loads the cars layout and converts it into a dictionary format using the graphicalMatrix function.
    2. Iterates over the cars and loads their corresponding images based on their size and index.
    3. Sets the position of each image on the screen based on the car's block position.
    4. Draws and displays each car image on the screen, scaling and rotating them as needed.
    """
    # Load cars layout
    cars = graphicalMatrix(level)
    inds = [0, 0]
    for ind, car in cars.items():
        size = car["size"]
        image, file = get_image(inds, ind, size)
        car["file"] = file

        # Set the position of the image
        image_x = info["RECT_X"] + car["block_pos"][0]*info["SIZE"]
        image_y = info["RECT_Y"] + car["block_pos"][1]*info["SIZE"]

        car["xy"] = (image_x, image_y)

        # Draw the image
        upd_image = pygame.transform.scale(
            image, (size*info["SIZE"], info["SIZE"]))
        upd_image = pygame.transform.rotate(upd_image, car["rot"])

        screen.blit(upd_image, (image_x, image_y))

        update_car_dict(cars, ind, (image_x, image_y), info, size)

    # Update the display
    # pygame.display.update()

    return cars


def redraw_board(info: Dict[str, int], cars: Dict[int, Dict[str, Any]], screen: pygame.Surface) -> None:
    """
    Redraws the gameboard with the updated positions of cars.

    Args:
        info (Dict[str, int]): A dictionary containing information about the gameboard dimensions and settings.
        cars (Dict[int, Dict[str, Any]]): A dictionary containing car information with car IDs as keys and their corresponding properties as values.
        screen (pygame.Surface): The Pygame screen object on which to redraw the cars.

    The 'info' dictionary should contain the following keys:
    - 'RECT_X': The x-coordinate of the top-left corner of the gameboard rectangle.
    - 'RECT_Y': The y-coordinate of the top-left corner of the gameboard rectangle.
    - 'SIZE': The size (width/height) of each gameboard cell.

    The 'cars' dictionary should contain car information with the following keys for each car ID:
    - 'file': The filename of the car image.
    - 'block_pos': The block position of the car (x, y).
    - 'size': The size of the car.
    - 'rot': The rotation angle of the car.

    The function performs the following tasks:
    1. Calls the 'gameboard_base' function to redraw the base gameboard.
    2. Iterates over the cars and loads their corresponding images.
    3. Sets the position of each image on the screen based on the car's block position.
    4. Draws and displays each car image on the screen, scaling and rotating them as needed.
    """

    gameboard_base(info, screen)

    for car in cars.values():
        image = pygame.image.load(car["file"])

        # Set the position of the image
        image_x = info["RECT_X"] + car["block_pos"][0]*info["SIZE"]
        image_y = info["RECT_Y"] + car["block_pos"][1]*info["SIZE"]

        # Draw the image
        rescaled_image = pygame.transform.scale(
            image, (car["size"]*info["SIZE"], info["SIZE"]))
        rotated_image = pygame.transform.rotate(rescaled_image, car["rot"])

        screen.blit(rotated_image, (image_x, image_y))

    # Update the display
    # pygame.display.update()


def redraw_motion(info: Dict[str, int], cars: Dict[int, Dict[str, Any]], screen: pygame.Surface) -> None:
    """
    Redraws the gameboard with the updated positions of cars.

    Args:
        info (Dict[str, int]): A dictionary containing information about the gameboard dimensions and settings.
        cars (Dict[int, Dict[str, Any]]): A dictionary containing car information with car IDs as keys and their corresponding properties as values.
        screen (pygame.Surface): The Pygame screen object on which to redraw the cars.

    The 'info' dictionary should contain the following keys:
    - 'RECT_X': The x-coordinate of the top-left corner of the gameboard rectangle.
    - 'RECT_Y': The y-coordinate of the top-left corner of the gameboard rectangle.
    - 'SIZE': The size (width/height) of each gameboard cell.

    The 'cars' dictionary should contain car information with the following keys for each car ID:
    - 'file': The filename of the car image.
    - 'xy': The x and y coordinates of the car's top-left corner.
    - 'size': The size of the car.
    - 'rot': The rotation angle of the car.

    The function performs the following tasks:
    1. Calls the 'gameboard_base' function to redraw the base gameboard.
    2. Iterates over the cars and loads their corresponding images.
    3. Sets the position of each image on the screen based on the car's xy coordinates.
    4. Draws and displays each car image on the screen, scaling and rotating them as needed.
    """

    gameboard_base(info, screen)

    for car in cars.values():
        image = pygame.image.load(car["file"])

        # Set the position of the image
        image_x = car["xy"][0]
        image_y = car["xy"][1]

        # Draw the image
        rescaled_image = pygame.transform.scale(
            image, (car["size"]*info["SIZE"], info["SIZE"]))
        rotated_image = pygame.transform.rotate(rescaled_image, car["rot"])
        screen.blit(rotated_image, (image_x, image_y))
    # pygame.display.update()


def find_car(cars: Dict[int, Dict[str, Any]], coords: Tuple[int, int]) -> Union[int, None]:
    """
    Finds the ID of the car occupying the specified field coordinates.

    Args:
        cars (Dict[int, Dict[str, Any]]): A dictionary containing car information with car IDs as keys and their corresponding coordinates as values.
        coords (Tuple[int, int]): The field coordinates (x, y) to search for.

    Returns:
        Union[int, None]: The ID of the car occupying the specified field coordinates.
        If no car is found, None is returned.
    """

    for car in cars.items():
        for c in car[1]["coords"]:
            if c == coords:
                return car[0]

    return None


def shift_car(coords: List[Tuple[int, int]], direction: str) -> List[Tuple[int, int]]:
    """
    Shifts the coordinates of a car in the specified direction.

    Args:
        coords (List[Tuple[int, int]]): A list of coordinate tuples representing the current positions of the car.
        direction (str): The direction in which to shift the car. Possible values are: "x+", "x-", "y+", "y-".

    Returns:
        List[Tuple[int, int]]: A list of coordinate tuples representing the new positions of the car after shifting.
    """

    new_coords = []
    if direction == "x+":
        for c in coords:
            new_coords.append((c[0]+1, c[1]))
    elif direction == "x-":
        for c in coords:
            new_coords.append((c[0]-1, c[1]))
    elif direction == "y+":
        for c in coords:
            new_coords.append((c[0], c[1]+1))
    elif direction == "y-":
        for c in coords:
            new_coords.append((c[0], c[1]-1))

    return new_coords


def render_counter_and_level(counter: int, info: Dict[str, int], level: int, max_moves: int, screen: pygame.Surface) -> None:
    """
    Renders and displays the move counter and level number on the game screen.

    Args:
        counter (int): The current move counter.
        info (Dict[str, int]): A dictionary containing information about the game window dimensions and settings.
        level (int): The current level number.
        max_moves (int): The maximum number of moves allowed for the level.
        screen (pygame.Surface): The Pygame screen object on which to render the counter and level.

    The 'info' dictionary should contain the following keys:
    - 'WINDOW': A tuple representing the dimensions (width, height) of the game window.

    The function performs the following tasks:
    1. Sets the font and text color for rendering.
    2. Renders and displays the move counter on the top-left corner of the screen.
    3. Renders and displays the level number on the top-right corner of the screen.
    """

    font = pygame.font.Font(None, 28)
    text_color = (255, 255, 255)

    # Render and display the counter on the left corner
    space = (4 - len(str(counter)))*" "
    counter_text = font.render(
        f"Moves: {str(counter)}{space}(Record: {max_moves})", True, text_color)
    screen.blit(counter_text, (10, 8))

    # Render and display the level number on the right corner
    level_text = font.render("Level: " + str(level), True, text_color)
    screen.blit(level_text, (info["WINDOW"][0]-190, 8))

    # pygame.display.update()


def get_xy_from_pos(info: Dict[str, int], car: Dict[str, Any]) -> Tuple[int, int]:
    """
    Calculate the pixel coordinates from the block position.

    Args:
        info (Dict[str, int]): A dictionary containing the size of the block and the starting x and y positions.
        car (Dict[str, Any]): A dictionary of car properties including its block position.

    Returns:
        Tuple[int, int]: The pixel coordinates corresponding to the block position of the car.
    """
    image_x = info["RECT_X"] + car["block_pos"][0] * info["SIZE"]
    image_y = info["RECT_Y"] + car["block_pos"][1] * info["SIZE"]

    return image_x, image_y
