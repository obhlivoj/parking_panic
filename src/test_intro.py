import pytest
from intro_screen import *

def test_display_text(mocker):
    # Initialize mocks
    mock_screen = mocker.patch('intro_screen.pygame.display.set_mode')
    mock_font = mocker.patch('intro_screen.pygame.font.Font').return_value
    mock_surface = mocker.patch('intro_screen.pygame.Surface').return_value
    mock_rect = mock_surface.get_rect.return_value

    mock_font.render.return_value = mock_surface

    # Call function
    display_text("test", (0, 0), mock_screen)

    # Check calls
    mock_font.render.assert_called_once_with("test", True, (255, 255, 255))
    mock_surface.get_rect.assert_called_once_with(center=(0, 0))
    mock_screen.blit.assert_called_once_with(mock_surface, mock_rect)

def test_handle_button_click_no_action_params(mocker):
    # Initialize mocks
    mock_get_pressed = mocker.patch('intro_screen.pygame.mouse.get_pressed')
    mock_get_pos = mocker.patch('intro_screen.pygame.mouse.get_pos')
    mock_get_pressed.return_value = [1]
    mock_get_pos.return_value = (1, 1)

    mock_button_rect = mocker.patch('intro_screen.pygame.Rect')
    mock_button_rect.collidepoint.return_value = True

    mock_action = mocker.MagicMock()
    mock_action.return_value = "action_result"

    result = handle_button_click(mock_button_rect, mock_action)

    assert result == "action_result"