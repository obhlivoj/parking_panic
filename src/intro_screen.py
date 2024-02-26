"""
intro_screen.py
This module contains the implementation of the Parking Panic screens using Pygame.

Functions:
- display_text(text: str, position: Tuple[int, int], screen) -> None:
    Display text on the screen.

- handle_button_click(button_rect: pygame.Rect, action, params: Optional[list] = None) -> Any:
    Handle button clicks.

- show_intro_screen(info: Dict[str, Any], recs: Dict[str, Any], screen) -> int:
    Show the intro screen of the game.

- show_level_selection_screen(info: Dict[str, Any], recs: Dict[str, Any], screen) -> int:
    Show the level selection screen.

- return_level(level: int) -> int:
    Start the game with the selected level.

- congratulate(info: Dict[str, Any], screen) -> None:
    Display the "Congratulations" message on the screen for a few seconds.

Author: Vojtech Obhlidal
Year: 2023
"""

import sys
import time
from typing import Dict, Any, Tuple, Optional

import pygame
# pylint: disable=no-member

def display_text(text: str, position: Tuple[int, int], screen) -> None:
    """
    Display text on the screen.

    Args:
        text: The text to be displayed.
        position: The position (x, y) of the text on the screen.
        screen: The Pygame screen object on which to display the text.
    """
    # Define font settings
    font = pygame.font.Font(None, 36)
    text_color = (255, 255, 255)

    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=position)
    screen.blit(text_surface, text_rect)

def handle_button_click(button_rect: pygame.Rect, action, params: Optional[list] = None):
    """
    Handle button clicks.

    Args:
        button_rect: The rectangle representing the button.
        action: The function to be executed when the button is clicked.
        params: Optional parameters to be passed to the action function.

    Returns:
        The result of the action function or None if the button was not clicked.
    """
    if pygame.mouse.get_pressed()[0]:
        mouse_pos = pygame.mouse.get_pos()
        if button_rect.collidepoint(mouse_pos):
            if params:
                res = action(*params)
            else:
                if action == pygame.quit:
                    res = True
                else:
                    res = action()
            return res
    return None

def show_intro_screen(info: dict, recs: dict, screen) -> int:
    """
    Show the intro screen of the game.

    Args:
        info: A dictionary containing information about the game window dimensions and settings.
        recs: A dictionary containing information about the game levels and records.
        screen: The Pygame screen object on which to display the intro screen.

    Returns:
        The selected level number.
    """
    # Draw the image
    file = "../cliparts/background.jpg"
    background = pygame.image.load(file)
    rescaled_background = pygame.transform.scale(background, info["WINDOW"])
    screen.blit(rescaled_background, (0, 0))

    start_button = pygame.Rect(200, 300, info["WINDOW"][0]-2*200, 50)
    quit_button = pygame.Rect(200, 400, info["WINDOW"][0]-2*200, 50)

    display_text("Welcome to Parking Panic!", (info["WINDOW"][0] // 2, 200), screen)
    pygame.draw.rect(screen, (0, 255, 0), start_button)
    display_text("START", (info["WINDOW"][0] // 2, 325), screen)
    pygame.draw.rect(screen, (255, 0, 0), quit_button)
    display_text("QUIT", (info["WINDOW"][0] // 2, 425), screen)

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            n_level = handle_button_click(start_button, show_level_selection_screen, [info, recs, screen])
            q = handle_button_click(quit_button, pygame.quit)
            if q:
                pygame.quit()
                sys.exit()

            if n_level:
                return n_level

def show_level_selection_screen(info: Dict[str, Any], recs: Dict[str, Any], screen) -> int:
    """
    Show the level selection screen.

    Args:
        info: A dictionary containing information about the game window dimensions and settings.
        recs: A dictionary containing information about the game levels and records.
        screen: The Pygame screen object on which to display the level selection screen.

    Returns:
        The selected level number.
    """
    screen.fill((0, 0, 0))
    display_text("Select Level", (info["WINDOW"][0] // 2, 100), screen)

    level_buttons = []
    for i in range(1, len(recs)+1):
        button_rect = pygame.Rect(80 + ((i-1)//7)*(140+80), 125 + ((i-1)%7) * 75, 140, 50)
        level_buttons.append(button_rect)
        pygame.draw.rect(screen, (0, 0, 255), button_rect)
        display_text("Level " + str(i), button_rect.center, screen)

    cont = False
    while not cont:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                cont = True

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        for i, button_rect in enumerate(level_buttons):
            n_level = handle_button_click(button_rect, lambda level = i+1: return_level(level))
            if n_level:
                return n_level

        pygame.display.update()

def return_level(level: int) -> int:
    """
    Start the game with the selected level.

    Args:
        level: The selected level number.

    Returns:
        The selected level number.
    """
    return level

def congratulate(info: Dict[str, Any], screen) -> None:
    """
    Display the "Congratulations" message on the screen for a few seconds.

    Args:
        info: A dictionary containing information about the game window dimensions and settings.
        screen: The Pygame screen object on which to display the message.
    """
    timer_duration = 3  # Pause for 3 seconds
    timer_start = None

    font = pygame.font.Font(None, 48)
    text_color = (255, 25, 25)

    # Start the game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Check if the timer has started
        if timer_start is None:
            # Display the text on the screen
            congratulations_text = font.render("CONGRATULATIONS", True, text_color)
            text_rect = congratulations_text.get_rect(center=(info["WINDOW"][0]/2,info["WINDOW"][1]/2))
            screen.blit(congratulations_text, text_rect)

            # Start the timer
            timer_start = time.time()

        # Check if the timer has expired
        if timer_start is not None and time.time() - timer_start >= timer_duration:
            break

        # Update the display
        pygame.display.update()
