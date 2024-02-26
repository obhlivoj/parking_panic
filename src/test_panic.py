import pytest
from pygame_module import graphicalMatrix, get_coords, get_image, update_car_dict, shift_car, get_xy_from_pos

SIZE = 100
RECT_X = 10
RECT_Y = 10
N_FIELD = 6
EXIT_SIZE = 80
EXIT_N = 2
window_size = (N_FIELD*SIZE + 2*RECT_X + EXIT_SIZE, N_FIELD*SIZE + 2*RECT_Y)

info = {
    "SIZE": SIZE,
    "RECT_X": RECT_X,
    "RECT_Y": RECT_Y,
    "N_FIELD": N_FIELD,
    "EXIT_SIZE": EXIT_SIZE,
    "EXIT_N": EXIT_N,
    "WINDOW": window_size,
}

def test_graphicalMatrix():
    cars = ['H122', 'V233']
    car_info = graphicalMatrix(cars)
    assert isinstance(car_info, dict)
    assert len(car_info) == len(cars)

@pytest.mark.parametrize("coords, expected_result", [
((20, 20), (0, 0)),
((1000, 400), (-1, -1)),
((280, 420), (2, 4))])
def test_get_coords(coords, expected_result):
    assert get_coords(info, coords) == expected_result

def test_get_image(mocker):
    inds = [0, 0]
    ind = 1
    size = 2
    mocker.patch('pygame.image.load')
    _, file = get_image(inds, ind, size)
    assert inds[0] == 1
    assert file == '../cliparts/car2_0.png'

def test_update_car_dict(mocker):
    cars = {
        0: {
            "id": "A",
            "dir": "H",
            "rot": 0,
            "size": 2,
        }
    }
    ind = 0
    image_coords = (110, 110)
    size = 2
    update_car_dict(cars, ind, image_coords, info, size)
    assert cars[ind]["coords"] == [(1, 1), (2, 1)]

@pytest.mark.parametrize("coords, direction, expected_result", [
    ([(1, 2), (1, 3)], "x+", [(2, 2), (2, 3)]),
    ([(2, 2), (2, 3)], "x-", [(1, 2), (1, 3)]),
    ([(2, 2), (2, 3)], "y+", [(2, 3), (2, 4)]),])
def test_shift_car(coords, direction, expected_result):
    assert shift_car(coords, direction) == expected_result

@pytest.mark.parametrize("car, expected_result", [
    ({"block_pos": (0, 0)}, (10, 10)),
    ({"block_pos": (1, 2)}, (110, 210)),
    ({"block_pos": (4, 4)}, (410, 410)),])
def test_get_xy_from_pos(car, expected_result):
    assert get_xy_from_pos(info, car) == expected_result
